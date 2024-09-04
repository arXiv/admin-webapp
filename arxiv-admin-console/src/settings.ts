// where the auth server is running.
export let authUrl = 'http://127.0.0.1:5000/aaa';
// where the backend is running
export let backendUrl = 'http://127.0.0.1:5000/adminapi/v1'
// and the UI is serving from
export let appUrl = 'http://127.0.0.1:5000/';

export const fetch_settings() => {
  return fetch('/env-config.json')
  .then(response => response.json())
  .then(config => {
    authUrl = config.AAA_URL || 'http://127.0.0.1:5000/aaa';
    backendUrl = config.ADMIN_API_BACKEND_URL || 'http://127.0.0.1:5000/adminapi';
    appUrl = config.ADMIN_APP_ROOT || 'http://127.0.0.1:5000/admin-console';
  })
  .catch(error => {
    console.error('Error loading configuration:', error);
  });
}
