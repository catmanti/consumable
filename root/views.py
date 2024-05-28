from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q, F, OuterRef, Subquery, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Order, OrderDetail, Item, Stock, Unit


def index(request):
    """The Home Page"""
    context = {
        "institute_name": "PDHS Office NorthWestern Province",
        "db_name": "Consumeble Database",
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
    """
    if Order item amount exceed Stock_available Go to get method with error Messege
    else make New order,
    update Stock Db redusing the order amount
    add items to order just created.
    redirected to the page order just created
    """
    unit_id = request.user.employee.unit_id
    unit_name = request.user.employee.unit
    unit = get_object_or_404(Unit, id=unit_id)
    context = {"unit_name": unit}

    if request.method == "POST":
        quantities = {}
        error_message = None

        for key, value in request.POST.items():
            if key.startswith("quantity_") and value:
                item_id = int(key.split("_")[1])
                quantities[item_id] = int(value)

        # Check if any order quantity exceeds stock availability using form data
        stock = get_object_or_404(Stock, item__id=item_id)
        for item_id, quantity in quantities.items():
            stock_available = get_object_or_404(Stock, item__id=item_id)
            if quantity > stock_available.stock_available:
                error_message = (
                    f"Order quantity for item with ID {item_id}"
                    + "exceeds stock available ({stock_available})."
                )
                context["error_message"] = error_message
                break

        if error_message:
            # Re-render the form with an error message
            last_order = Order.objects.filter(unit_id=unit_id).last()
            if last_order:
                items_with_amounts = Item.objects.annotate(
                    amount=Sum(
                        "orderdetail__amount",
                        filter=Q(orderdetail__order_id=last_order.id),
                    )
                )
            else:
                items_with_amounts = Item.objects.all()

            context["item_list"] = items_with_amounts
            return render(request, "consume/new_order_form.html", context)

        # Create a new order and update stock
        new_order = Order.objects.create(order_date=date.today(), unit=unit)
        for item_id, quantity in quantities.items():
            print("D_quantitty item_id", item_id, "quantity", quantity)
            OrderDetail.objects.create(
                order=new_order, item_id=item_id, amount=quantity
            )
            stock = Stock.objects.get(item_id=item_id)
            stock.stock_available -= quantity
            stock.save()

        return redirect("order_detail", pk=new_order.pk)

    else:  # Get Method
        # if the user has previous order get item_name, stock_available & amount
        last_order = Order.objects.filter(unit_id=unit_id).last()
        if last_order:

            def get_combined_stock_order_details(last_order_id):
                # Define a subquery to get the amount from OrderDetail
                order_details_subquery = OrderDetail.objects.filter(
                    order_id=last_order_id, item_id=OuterRef("item_id")
                ).values("amount")[:1]

                # Query Stock and annotate with item_name, amount, and id
                queryset = Stock.objects.annotate(
                    item_name=F("item__item_name"),
                    amount=Subquery(
                        order_details_subquery, output_field=IntegerField()
                    ),
                    item_id_annotated=F("item__id"),
                ).values("item_name", "stock_available", "amount", "item_id_annotated")
                return queryset

            combined_queryset = get_combined_stock_order_details(last_order)
        else:
            combined_queryset = Stock.objects.annotate(
                item_name=F("item__item_name"), item_id_annotated=F("item__id")
            ).values("item_name", "stock_available", "item_id_annotated")
        # if no previous oreders get the item_name, stock_available
        context = {
            "item_list": combined_queryset,
            "unit_name": unit_name,
        }
    return render(request, "consume/new_order_form.html", context)


class StockView(LoginRequiredMixin, ListView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unit_name"] = Unit.objects.get(id=self.request.user.employee.unit_id)
        return context


class OrderView(DetailView):
    model = Order
