from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import jwt
from jwt.algorithms import RSAAlgorithm

app = Flask(__name__)
app.secret_key = 'secret'  # Replace with a secure secret key

# Keycloak configuration
KEYCLOAK_SERVER_URL = 'https://keycloak-service-6lhtms3oua-uc.a.run.app'
REALM_NAME = 'arxiv'
CLIENT_ID = 'arxiv-user'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'

# Keycloak endpoints
AUTH_URL = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth'
TOKEN_URL = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'
CERTS_URL = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs'


def get_public_key(kid):
    certs_response = requests.get(CERTS_URL)
    certs = certs_response.json()
    for key in certs['keys']:
        if key['kid'] == kid:
            return RSAAlgorithm.from_jwk(key)
    return None



# Function to validate token

def validate_token(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header['kid']
        algorithm = unverified_header['alg']
        public_key = get_public_key(kid)
        if public_key is None:
            return None
        decoded_token = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def home():
    session.clear()
    return redirect('/login')


@app.route('/login')
def login():
    # Redirect the user to the Keycloak login page
    return redirect(f'{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid')


@app.route('/callback')
def callback():
    # Get the authorization code from the callback URL
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }
    )

    if token_response.status_code != 200:
        session.clear()
        return 'Something is wrong'

    # Parse the token response
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    refresh_token = token_json.get('refresh_token')

    # Store tokens in session (for demonstration purposes)
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token

    print(validate_token(access_token))
    return 'Login successful!'


@app.route('/logout')
def logout():
    # Clear the session and redirect to home
    session.clear()
    return redirect(url_for('home'))

@app.route('/protected')
def protected():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Access token is missing'}), 401

    decoded_token = validate_token(access_token)
    if not decoded_token:
        return jsonify({'error': 'Invalid token'}), 401

    return jsonify({'message': 'Token is valid', 'token': decoded_token})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
