from django.contrib import admin
from .models import Unit, Stock, Item, Supplier, OrderDetail, Order


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
