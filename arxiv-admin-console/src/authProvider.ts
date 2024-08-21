import { AuthProvider } from 'react-admin';

const apiUrl = 'http://127.0.0.1:5000/api';

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!;
    return null;
}

const cookie_name: string = "token";

export const authProvider: AuthProvider = {
    // called when the user attempts to log in
    login: () => {
        console.log("auth: /login");
        window.location.href = `${apiUrl}/login`;
        return Promise.resolve();
    },
    // called when the user clicks on the logout button
    logout: () => {
        console.log("auth: /logout");
        /* document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`; */
        return fetch(`${apiUrl}/logout`, {
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
        })
            .catch(error => {
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
        console.log(`${cookie_name} -> ` + token);
        return Promise.resolve();
        return token ? Promise.resolve() : Promise.reject();
    },
    // called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => Promise.resolve(),
};
