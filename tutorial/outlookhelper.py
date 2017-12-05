import requests
import uuid
import json

api_endpoint = "https://graph.microsoft.com/v1.0/"

def api_call(method, end_point_url, token, user_mail, payload=None, parameters=None):
	req_id = str(uuid.uuid4())
	headers = {
		'User-Agent': 'python_tutorial/1.0',
		'Authorization': 'Bearer {0}'.format(token),
		'Accept': 'application/json',
		'X-AnchorMailbox': user_mail,
		'client-request-id': req_id,
		'return-client-request-id': 'true',
	}

	if method.upper() == 'GET':
		response = requests.get(end_point_url, headers=headers, params=parameters)
	elif method.upper() == 'DELETE':
		response = requests.delete(end_point_url, headers=headers, params=parameters)
	elif method.upper() == 'PATCH':
		headers.update({'Content-Type': 'application/json'})
		response = requests.patch(end_point_url, headers=headers, data=json.dumps(payload), params=parameters)
	elif method.upper() == 'POST':
		headers.update({'Content-Type': 'application/json'})
		response = requests.post(end_point_url, headers=headers, data=json.dumps(payload), params=parameters)

	return response

def get_user(token):
	user_url = api_endpoint + "me"
	query_parameters = {
		'$select': 'displayName,mail'
	}
	r = api_call('GET', user_url, token, "", parameters=query_parameters)

	return r.json()

def get_user_messages(token, user_email):
	mail_url = api_endpoint + "me/mailfolders/inbox/messages"
	params = {
		'$top': '10',
		'$select': 'receivedDateTime,subject,from,body',
		'$orderby': 'receivedDateTime DESC',
	}

	r = api_call("GET", mail_url, token=token, user_mail="cyantarek@bigidea.onmicrosoft.com", parameters=params)

	return r.json()

def get_user_events(token, user_email):
	event_url = api_endpoint + "me/events"
	params = {
		'$top': '10',
		'$select': 'subject,start,end',
		'$orderby': 'start/dateTime ASC'
	}

	r = api_call("GET", event_url, token=token, user_mail="cyantarek@bigidea.onmicrosoft.com", parameters=params)

	return r.json()