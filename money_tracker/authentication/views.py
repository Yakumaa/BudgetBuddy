from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

# from django.core.validators import validate_email
from validate_email import validate_email
import json


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        messages.success(request, "Success")
        messages.warning(request, "Warning")
        messages.info(request, "Info")
        messages.error(request, "Error")
        return render(request, "authentication/register.html")


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "username should only contain alpha numeric characters"
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            messages.info(request, "username taken")
            return redirect("register")

        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse(
                {"email_error": "email is invalid"},
                status=400,
            )

        if User.objects.filter(email=email).exists():
            messages.info(request, "email already in use")
            return redirect("register")

        return JsonResponse({"email_valid": True})
