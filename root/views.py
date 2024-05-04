from django.db.models import Sum, Q
from django.shortcuts import render
from .models import Unit, Item
from .models import Order
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


def new_order(request):
    """To Add New Orders
    todo:
    - get the list of items and add in the form
    """
    context = {}
    unit_id = 3
    if request.method == "POST":
        print("....at POST")
    else:
        last_order = Order.objects.filter(unit_id=unit_id).last()
        if last_order:
            items_with_amounts = Item.objects.annotate(
                amount=Sum(
                    "orderdetail__amount", filter=Q(orderdetail__order_id=last_order.id)
                )
            )
        else:
            items_with_amounts = Item.objects.all()
        context = {
            "item_list": items_with_amounts,
        }
    return render(request, "consume/new_order_form.html", context)
