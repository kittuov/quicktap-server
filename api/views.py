import json

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


from game.sockets import *


# Create your views here.
def login(request):
    if request.method == "GET":
        if request.session.get("profile-id") is not None:
            try:
                profile = Profile.objects.get(pk=request.session.get("profile-id"))
                serializer = ProfileSerializer(profile)
                content = JSONRenderer().render(serializer.data)
                return HttpResponse(content=content, status=200)
            except Profile.DoesNotExist:
                return logout(request)
        content = JSONRenderer().render(
            [{"name": "username", "type": "text", "label": "Username"},
             {"name": "password", "type": "password", "label": "Password"}])
        return HttpResponse(content=content, status=401)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        form.clean()
        if not form.is_valid():
            content = JSONRenderer().render(form.errors)
            return HttpResponse(content=content, status=401)
        user = form.get_user()
        auth_login(request, user)
        profile = Profile.objects.get(user=user)
        profile.login(request)
        serializer = ProfileSerializer(profile)
        content = JSONRenderer().render(data=serializer.data)
        return HttpResponse(content=content, status=200)


def logout(request):
    auth_logout(request)
    request.session.flush()
    return HttpResponse(content=JSONRenderer().render({"logout": "success"}), status=200)


def guest_login(request):
    if request.method == "GET":
        content = JSONRenderer().render(
            [{"name": "firstName", "type": "text", "label": "First Name"},
             {"name": "lastName", "type": "password", "label": "Last Name"},
             {"name": "image", "type": "number", "label": "Avatar"}])
        return HttpResponse(content=content, status=400)

    if request.method == "POST":
        # try:
        #     request.POST = json.loads(request.body.decode("utf-8"))
        # except json.JSONDecodeError:
        #     pass
        data = JSONParser().parse(request)
        profile = Profile(firstName=data.get("firstName"), lastName=data.get("lastName"), image=data.get("image"))
        try:
            profile.save()
            profile.login(request)
            content = JSONRenderer().render(ProfileSerializer(profile).data)
            return HttpResponse(content)
        except Exception as e:
            return HttpResponse("", status=400)

