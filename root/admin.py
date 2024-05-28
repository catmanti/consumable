from django.contrib import admin
from .models import Unit, Stock, Item, Supplier, OrderDetail, Order, Employee


admin.site.site_header = "Accunting Unit"
admin.site.site_title = "Consumeble Database - Accunting Unit"
admin.site.index_title = "Welcome to the Accunting Unit"


class IdAdmin(admin.ModelAdmin):
    readonly_fields = [
        "id",
    ]


admin.site.register(Unit, IdAdmin)
admin.site.register(Stock, IdAdmin)
admin.site.register(Item)
admin.site.register(Supplier)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(Employee)
