// where the auth server is running.
export const authUrl = process.env.AAA_URL || 'http://127.0.0.1:5000/aaa';
// where the backend is running
export const backendUrl = process.env.ADMIN_API_BACKEND_URL || 'http://127.0.0.1:5000/api/v1'
// and the UI is serving from
export const appUrl = process.env.ADMIN_APP_ROOT || 'http://127.0.0.1:5000/';
