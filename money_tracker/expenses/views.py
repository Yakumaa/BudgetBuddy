from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages


# Create your views here.
# TODO: make login_required work
@login_required(login_url="/authentication/login")
def index(request):
    catergories = Category.objects.all()
    return render(request, "expenses/index.html")


def add_expense(request):
    catergories = Category.objects.all()
    context = {"categories": catergories, "values": request.POST}

    if request.method == "GET":
        return render(request, "expenses/add_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expense.html", context)

        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
        )
        messages.success(request, "Expense saved succesfully")

        return redirect("expenses")
