// where the auth server is running.
export let authUrl = 'http://127.0.0.1:5000/aaa';
// where the backend is running
export let backendUrl = 'http://127.0.0.1:5000/adminapi/v1'
// and the UI is serving from
export let appUrl = 'http://127.0.0.1:5000/admin-console/';

export async function fetch_settings(): Promise<any> {
    try {
        const response = await fetch('/admin-console/env-config.json');
        const config = await response.json();
        authUrl = config.AAA_URL || authUrl;
        backendUrl = config.ADMIN_API_BACKEND_URL || backendUrl;
        appUrl = config.ADMIN_APP_ROOT || appUrl;
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}
