import json, time

import requests

import secrets

requests.patch(
  'https://repo-quality.firebaseio.com/.json?auth={}'.format(secrets.firebase_token),
  data=json.dumps({'mean_stars_per_issue': 20}))

resp = requests.get(
  'https://repo-quality.firebaseio.com/.json?auth={}'.format(secrets.firebase_token))
print 'content:', resp.content