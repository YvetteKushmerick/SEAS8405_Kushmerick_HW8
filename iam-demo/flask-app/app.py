from flask import Flask, request, jsonify
from jose import jwt
import requests

app = Flask(__name__)

KEYCLOAK_URL = 'http://keycloak:8080'
REALM = 'demo-realm'
CLIENT_ID = 'flask-client'

def get_public_key():
    jwks_url = f'{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs'
    response = requests.get(jwks_url)
    return response.json()['keys'][0]

@app.route('/public')
def public():
    return jsonify(message="Public route - no auth needed")

@app.route('/protected')
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify(error="Missing Authorization header"), 401
    token = auth_header.split(" ")[1]
    key = get_public_key()
    try:
        payload = jwt.decode(token, key, algorithms=['RS256'], audience=CLIENT_ID)
        return jsonify(message=f"Protected route - welcome {payload['preferred_username']}")
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
