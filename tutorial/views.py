from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . authhelper import get_auth_url, get_token_code
from . outlookhelper import get_user, get_user_messages, get_user_events
import json


def home(request):
	try:
		user_email = request.session["user_mail"]
		user = user_email.split("@")[0]
		context = {"message": "Thanks {0} for signing up. Enjoy the app".format(user)}
	except KeyError:
		auth_url = get_auth_url()
		context = {"signin_url": auth_url}
	return render(request, "home.html", context)

def api_work(request):
	auth_code = request.GET["code"]
	token_code = get_token_code(auth_code)["access_token"]
	request.session["token"] = token_code
	user = get_user(token_code)
	with open("token.json", "w") as f:
		json.dump({"token": token_code}, f)
	user_email = request.session["user_mail"]
	request.session["user_mail"] = user_email
	return HttpResponseRedirect(reverse("home"))

def mail_view(request):
	try:
		with open("token.json", "r") as f:
			jsn = json.load(f)
			token = jsn["token"]
		token = request.session["token"]
		user_email = request.session["user_mail"]
		messages = get_user_messages(token=token, user_email=user_email)
		context = {"messages": messages["value"], "mail": user_email}
	except KeyError:
		context = {"error_message": "Please signup to outlook before viewing your emails"}
	return render(request, "mail.html", context)

def events_view(request):
	try:
		with open("token.json", "r") as f:
			jsn = json.load(f)
			token = jsn["token"]
		token = request.session["token"]
		user_email = request.session["user_mail"]
		events = get_user_events(token, user_email)
		context = {"events": events["value"], }
	except KeyError:
		context = {"error_message": "Please signup to outlook before viewing your events"}
	return render(request, "event.html", context)