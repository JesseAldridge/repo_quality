from firebase_token_generator import create_token

import secrets

auth_payload = { "uid": "admin" }
token = create_token(secrets.firebase_secret, auth_payload)
print 'token:', token
