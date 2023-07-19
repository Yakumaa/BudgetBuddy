from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
import json


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username error": "username should only contain alpha numeric characters"
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            messages.info(request, "username taken")
            return redirect("register")

        return JsonResponse({"username_valid": True})
