from django.urls import path
from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("apiwork/", views.api_work, name="apiwork"),
	path("mail/", views.mail_view, name="mail"),
	path("events/", views.events_view, name="events"),
]