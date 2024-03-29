from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# from django.core.validators import validate_email
from validate_email import validate_email
import json


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # messages.success(request, "Success")
        # messages.warning(request, "Warning")
        # messages.info(request, "Info")
        # messages.error(request, "Error")
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]

        context = {"fieldValues": request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if password == repeat_password:
                    if len(password) < 6:
                        messages.error(request, "Password too short!")
                        return render(request, "authentication/register.html", context)
                    else:
                        user = User.objects.create_user(username=username, email=email)
                        user.set_password(password)
                        user.is_active = False
                        user.save()

                        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                        domain = get_current_site(request).domain
                        link = reverse(
                            "activate",
                            kwargs={
                                "uidb64": uidb64,
                                "token": token_generator.make_token(user),
                            },
                        )
                        activate_url = "http://" + domain + link
                        email_subject = "Activate your account"
                        email_body = (
                            "Hi "
                            + user.username
                            + ". Use this link to verify your account\n"
                            + activate_url
                        )
                        # email = EmailMessage(
                        #     email_subject,
                        #     email_body,
                        #     settings.EMAIL_HOST_USER,
                        #     [email],
                        # )

                        # email.send(fail_silently=False)
                        send_mail(
                            email_subject,
                            email_body,
                            settings.EMAIL_HOST_USER,
                            [email],
                            fail_silently=True,
                        )
                        messages.success(request, "Account successfully created!")
                        return render(request, "authentication/register.html")
                else:
                    messages.error(request, "Password do not match!")
                    return render(request, "authentication/register.html", context)

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
            return JsonResponse({"username_error": "username taken"}, status=409)

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
            return JsonResponse({"email_error": "email already in use"}, status=409)

        return JsonResponse({"email_valid": True})


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, "authentication/reset-password.html")

    def post(self, request):
        email = request.POST["email"]

        context = {"values": request.POST}

        if not validate_email(email):
            messages.error(request, "Please enter a valid email")
            return render(request, "authentication/reset-password.html", context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                "user": user[0],
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
                "token": PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse(
                "reset-user-password",
                kwargs={
                    "uidb64": email_contents["uid"],
                    "token": email_contents["token"],
                },
            )

            email_subject = "Password Reset Instructions"
            active_url = "http://" + current_site.domain + link
            email_body = "Hi " + " Use this link to verify your account\n" + active_url
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.send(fail_silently=False)

        messages.success(request, "We have sent you a link to reset your password")
        return render(request, "authentication/reset-password.html")


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        return render(request, "authentication/set-new-password.html")

    def post(self, request, uidb64, token):
        return render(request, "authentication/set-new-password.html")


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")

            if user.is_active:
                return redirect("login")

            user.is_active = True
            user.save()

            messages.success(request, "Account activated Successfully")
            return redirect("login")

        except Exception as ex:
            pass

        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, "Welcome, " + user.username + " you are now logged in"
                    )
                    return redirect("expenses")

                messages.error(
                    request, "Account is not active, Please check your email"
                )
                return render(request, "authentication/login.html")

            messages.error(request, "Invalid Credentials, Please try again")
            return render(request, "authentication/login.html")

        messages.error(request, "Please fill all the fields")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect("login")
