import { AuthProvider } from 'react-admin';
import {useEffect, useState} from "react";

const authUrl = 'http://127.0.0.1:5000';

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!;
    return null;
}

let cookie_name = "arxiv_session_cookie";
const fetchCookieName = async() => {
    const res = await fetch(`${authUrl}/token-names`);
    if (res.ok) {
        try {
            const data = await res.json();
            cookie_name = data.session;
        }
        catch (e) {
            console.error(e);
        }
    }
    else {
        console.log(`cookie name is default ${cookie_name}`);
    }
}
fetchCookieName();

export const authProvider: AuthProvider = {
    // called when the user attempts to log in
    login: () => {
        console.log("auth: /login");
        window.location.href = `${authUrl}/login`;
        return Promise.resolve();
    },
    // called when the user clicks on the logout button
    logout: () => {
        console.log("auth: /logout");
        /* document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`; */
        return fetch(`${authUrl}/logout?next=http://127.0.0.1:5000/`, {
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
        const token = getCookie(cookie_name);
        return Promise.resolve();
        return token ? Promise.resolve() : Promise.reject();
    },
    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => Promise.resolve(),
};
