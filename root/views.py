from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render
from .models import Unit, Item
from .models import Order, OrderDetail
from .forms import ContactForm


def index(request):
    """The Home Page"""
    if request.method == "POST":
        print("at POST")
        form = ContactForm(request.POST)
        form_data = {}
        if form.is_valid():
            form_data.update({"subject": form.cleaned_data["subject"]})
            form_data.update({"message": form.cleaned_data["message"]})
            form_data.update({"sender": form.cleaned_data["sender"]})

        context = {
            "form_data": form_data,
        }
        print("Form_Data", form_data)
        return render(request, "home.html", context)

    else:
        print("at Get")
        items = Item.objects.all()
        form = ContactForm()
        context = {
            "catman": items,
            "form": form,
        }
        return render(request, "consume/home.html", context)


def order(request):
    """To Select Orders in Drop down"""
    units = Unit.objects.all()
    selected_item = request.GET.get("item")

    if selected_item:
        orders = Order.objects.filter(unit_id=selected_item)
    else:
        orders = Order.objects.all()

    context = {
        "orders": orders,  # For The list
        "selected_item ": selected_item,  # For DropDown
        "units": units,  # For DropDown
    }
    return render(request, "consume/order_form.html", context)


@login_required
def new_order(request):
    """This method is used to create new order with items and quantities
    in the form and save it in the database and return a success message
    todo:
    Need to make it work with multiple units in the future
    Get unit_id from the request.user
    """
    unit_id = request.user.employee.unit_id
    context = {}
    unit = Unit.objects.get(id=unit_id)
    if request.method == "POST":
        quantities = {}
        for key, value in request.POST.items():
            if key.startswith("quantity_") and value:
                item_id = int(key.split("_")[1])
                quantities[item_id] = int(value)

        new_order = Order.objects.create(order_date=date.today(), unit_id=unit_id)
        for item_id, quantity in quantities.items():
            order_detail = OrderDetail(
                order=new_order, item_id=item_id, amount=quantity
            )
            order_detail.save()
        return HttpResponse("Order submitted successfully!")

    else:  # get the last order from the database related to unit_id
        last_order = Order.objects.filter(unit_id=unit_id).last()
        if last_order:
            items_with_amounts = Item.objects.annotate(
                amount=Sum(
                    "orderdetail__amount", filter=Q(orderdetail__order_id=last_order.id)
                )
            )
        else:  # get an empty item list
            items_with_amounts = Item.objects.all()
        context = {
            "item_list": items_with_amounts,
            "unit_name": unit,
        }
    return render(request, "consume/new_order_form.html", context)
