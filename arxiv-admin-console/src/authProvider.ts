import { AuthProvider } from 'react-admin';
// import {useEffect, useState, useContext} from "react";
import {RuntimeProps} from "./RuntimeContext";
import {getRemainingTimeInSeconds} from "./helpers/timeDiff";

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!.replace(/\\(\d{3})/g, (_match, octalCode) => String.fromCharCode(parseInt(octalCode, 8)))!;
    return null;
}

let logoutInProgress = false;

export const createAuthProvider = (runtimeProps: RuntimeProps): AuthProvider => ({

    // called when the user attempts to log in
    login: () => {
        const currentUrl = window.location.href;
        window.location.href = `${runtimeProps.AAA_URL}/login?next_page=${encodeURIComponent(currentUrl)}`;
        return Promise.resolve();
    },
    // called when the user clicks on the logout button
    logout: () => {
        if (logoutInProgress) {
            console.log("auth: /logout in progress");
            return Promise.resolve();
        }
        logoutInProgress = true;
        console.log("auth: /logout started");

        return fetch(`${runtimeProps.AAA_URL}/logout?next_page=/`, {
            method: 'GET',
            credentials: 'include',
        }).then(() => {
            console.log("auth: logout fetch success");
            window.location.href = '/'; // Redirect to login page
        }).finally(() => {
            logoutInProgress = false;
        });
    },

    // called when the API returns an error
    checkError: async ({ status }: { status: number }) => {
        if (status === 401) {
            console.log("auth: checkError - token expired.");
            const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);

            if (token) {
                console.log("auth: checkError - old token exist, attempt refresh");
                try {
                    const refreshResponse = await fetch(`${runtimeProps.AAA_URL}/refresh`, {
                        method: 'GET',
                        credentials: 'include',
                    });

                    if (refreshResponse.ok) {
                        console.log("auth: Token refreshed successfully");
                        // Token refreshed successfully, retry the original request if needed
                        return Promise.resolve();
                    }
                } catch (error) {
                    console.error("auth: Error during token refresh", error);
                    // Handle fetch failure, logout the user
                    // await fetch(`${runtimeProps.AAA_URL}/logout`, { method: 'GET', credentials: 'include' });
                }
            }
            return Promise.reject();
        }
        else if (status === 403 || status === undefined) {
            console.log("auth: checkError 403");
            // await fetch(`${runtimeProps.AAA_URL}/logouf`, {method: 'GET', credentials: 'include'});
            return Promise.reject();
        }
        console.log(`auth: good - checkError status=${status} `);
        return Promise.resolve();
    },

    // called when the user navigates to a new location, to check for authentication
    checkAuth: async () => {
        const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
        return token ? Promise.resolve() : Promise.reject();
    },

    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: async () => Promise.resolve(),
});
