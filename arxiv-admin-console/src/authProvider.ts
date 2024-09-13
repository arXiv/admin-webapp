import { AuthProvider } from 'react-admin';
import {useEffect, useState, useContext} from "react";
import {RuntimeProps} from "./RuntimeContext";

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!;
    return null;
}

let logoutInProgress = false;

export const createAuthProvider = (runtimeProps: RuntimeProps): AuthProvider => ({

    // called when the user attempts to log in
    login: () => {
        console.log("auth: /login");
        window.location.href = `${runtimeProps.AAA_URL}/login`;
        return Promise.resolve();
    },
    // called when the user clicks on the logout button
    logout: () => {
        if (logoutInProgress) {
            console.log("auth: /logout in progress");
            return Promise.resolve();
        }
        logoutInProgress = true;
        console.log("auth: /logout");
        return fetch(`${runtimeProps.AAA_URL}/logout`, {
            method: 'GET',
            credentials: 'include',
        }).then(() => {
            window.location.href = '/'; // Redirect to login page
        }).finally(() => {
            logoutInProgress = false;
        });
    },
    // called when the API returns an error
    checkError: ({ status }: { status: number }) => {
        if (status === 401 || status === 403) {
            console.log("auth: checkError bad");
            /* document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`; */
            return Promise.reject();
        }
        console.log(`auth: good - checkError status=${status} `);
        return Promise.resolve();
    },
    // called when the user navigates to a new location, to check for authentication
    checkAuth: () => {
        const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
        console.log(`checkAuth: ${token?.length}`);
        return token ? Promise.resolve() : Promise.reject();
    },
    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => Promise.resolve(),
});
