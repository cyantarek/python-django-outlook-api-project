from urllib.parse import quote, urlencode
import base64
import json
import time

import requests
from django.urls import reverse

app_id = "87c04110-2565-49b4-802c-3945dfcbeae3"
app_secret = "vqlLR8?()amizCGNPV6857("

token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"


def get_auth_url():
	params = {
		'client_id': app_id,
		'redirect_uri': "http://localhost:8000" + reverse("apiwork"),
		'response_type': 'code',
		'scope': "openid User.Read Mail.Read Calendars.Read"
	}
	print(params["redirect_uri"])
	auth_url = "https://login.microsoftonline.com//common/oauth2/v2.0/authorize?{0}".format(urlencode(params))
	return auth_url


def get_token_code(auth_code):
	post_data = {'grant_type': 'authorization_code',
				 'code': auth_code,
				 'redirect_uri': "http://localhost:8000" + reverse("apiwork"),
				 'scope': "openid User.Read Mail.Read",
				 'client_id': app_id,
				 'client_secret': app_secret
				 }

	r = requests.post(token_url, data=post_data)

	try:
		return r.json()
	except:
		return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)
