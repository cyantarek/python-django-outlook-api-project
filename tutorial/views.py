from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . authhelper import get_auth_url, get_token_code
from . outlookhelper import get_user, get_user_messages, get_user_events
import json


def home(request):
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
	user_mail = user["mail"]
	request.session["user_mail"] = user_mail
	return HttpResponseRedirect(reverse("mail"))

def mail(request):
	with open("token.json", "r") as f:
		jsn = json.load(f)
		token = jsn["token"]

	token = request.session["token"]
	user_email = request.session["user_mail"]
	messages = get_user_messages(token=token, user_email=user_email)
	with open("response.json", "w") as f:
		json.dump(messages, f)
	context = {"messages": messages["value"], "mail": user_email}
	# return HttpResponse("Messages: {0}".format(messages))
	return render(request, "mail.html", context)

def events(request):
	with open("token.json", "r") as f:
		jsn = json.load(f)
		token = jsn["token"]

	token = request.session["token"]
	user_email = request.session["user_mail"]
	events = get_user_events(token, user_email)
	context = {"events": events["value"],}
	return render(request, "event.html", context)