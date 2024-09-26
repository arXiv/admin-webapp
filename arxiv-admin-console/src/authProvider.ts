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
    login: (props) => {
        const {refresh} = props;
        console.log("auth: /login " + JSON.stringify(props));
        if (refresh) {
            fetch(`${runtimeProps.AAA_URL}/refresh?next_page=`,
                {
                    method: "GET",
                    credentials: "include",
                }
                ).then(
                () => {
                    console.log("login Did it work?");
                }
                ).finally(() => {
                    console.log("login finallly ");
            });
            return Promise.resolve();
        }
        else {
            window.location.href = `${runtimeProps.AAA_URL}/login`;
            return Promise.resolve();
        }
    },
    // called when the user clicks on the logout button
    logout: () => {
        if (logoutInProgress) {
            console.log("auth: /logout in progress");
            return Promise.resolve();
        }
        logoutInProgress = true;
        console.log("auth: /logout in progress");

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
    checkError: ({ status }: { status: number }) => {
        if (status === 401 || status === 403 || status === undefined) {
            console.log("auth: checkError bad");
            const nextPage = encodeURIComponent(window.location.href);
            const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
            const action = token && token.length > 0 ? "refresh" : "login";
            window.location.href = `${runtimeProps.AAA_URL}/${action}?next_page=${nextPage}`;
            return Promise.reject();
        }
        console.log(`auth: good - checkError status=${status} `);
        return Promise.resolve();
    },
    // called when the user navigates to a new location, to check for authentication
    checkAuth: () => {
        const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
        const utc_expire = token?.split(",")[1];
        if (utc_expire) {
            const timeLeft = getRemainingTimeInSeconds(utc_expire);
            if (timeLeft < 120) {
                console.log("refresh token started " + token?.slice(0,40) )
                fetch(`${runtimeProps.AAA_URL}/refresh`, {
                    method: 'GET',
                    credentials: 'include',
                }).then(() => {
                    const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
                    console.log("auth: logout refresh success: " + token?.slice(0,40) );
                }).finally(() => {
                    console.log("auth: logout refresh ended" );
                    }
                );

            }
        }
        return token ? Promise.resolve() : Promise.reject();
    },

    refreshToken: () => {
        fetch(`${runtimeProps.AAA_URL}/refresh`, {
            method: 'GET',
            credentials: 'include',
        }).then(() => {
            const token = getCookie(runtimeProps.ARXIV_COOKIE_NAME);
            console.log("auth: logout refresh success: " + token?.slice(0,40) );
        });

        return;
    },
    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => Promise.resolve(),
});
