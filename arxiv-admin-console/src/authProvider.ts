import { AuthProvider } from 'react-admin';
import {useEffect, useState, useContext} from "react";
import {RuntimeProps} from "./RuntimeContext";

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!;
    return null;
}

export const createAuthProvider = (runtimeProps: RuntimeProps): AuthProvider => ({

    // called when the user attempts to log in
    login: () => {
        console.log("auth: /login");
        window.location.href = `${runtimeProps.AAA_URL}/login`;
        return Promise.resolve();
    },
    // called when the user clicks on the logout button
    logout: () => {
        console.log("auth: /logout");
        /* document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`; */
        return fetch(`${runtimeProps.AAA_URL}/logout?next=${runtimeProps.ADMIN_APP_ROOT}`, {
            method: "GET",
            credentials: "include",
        }).then(response => {
            console.log("auth: response");
            if (response.ok) {
                console.log("auth: response ok");
                window.location.href = '/';
                return Promise.resolve();
            } else {
                console.log("auth: response ng");
                return Promise.reject();
            }
        }).catch(error => {
            console.error(`error auth logout ${error}`);
        });
    },
    // called when the API returns an error
    checkError: ({ status }: { status: number }) => {
        console.log(`auth: checkError status=${status}`);
        if (status === 401 || status === 403) {
            console.log("auth: checkError bad");
            /* document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`; */
            return Promise.reject();
        }
        console.log("auth: checkError good");
        return Promise.resolve();
    },
    // called when the user navigates to a new location, to check for authentication
    checkAuth: () => {
        const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
        return Promise.resolve();
        return token ? Promise.resolve() : Promise.reject();
    },
    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => Promise.resolve(),
});
