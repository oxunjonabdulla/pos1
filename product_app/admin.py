from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportMixin
import os

from BOLT.settings import BASE_DIR
from .models import Maxsulot, OrderItems, Order, CartItems, Kategoriya, Department
from .resources import MaxsulotResource, OrderResource, OrderItemsResource, CartItemsResource


class MaxsulotAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MaxsulotResource



class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['nomi']

    def nomi(self, obj):
        return obj.name
    nomi.short_description = "Nomi"


admin.site.register(Department, DepartmentAdmin)

admin.site.register(Kategoriya)
admin.site.register(Maxsulot, MaxsulotAdmin)


class OrderItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderItemsResource


admin.site.register(OrderItems, OrderItemsAdmin)





class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderResource

    def export_orders_with_template(self, request, queryset):
        """
        Export orders using an XLSX template.
        """
        # Resolve the path to the template
        template_path = os.path.join(BASE_DIR, "static", "buyurtmalar1.xlsx")
        if not os.path.exists(template_path):
            self.message_user(request, f"Shablon topilmadi {template_path}", level='error')
            return

        queryset = queryset.filter(status='2')  # Example filter for status '2'

        resource = self.resource_class()
        xlsx_content = resource.export_to_template_xlsx(queryset, template_path)

        response = HttpResponse(
            xlsx_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response['Content-Disposition'] = 'attachment; filename="buyurtmalar1.xlsx"'
        return response

    export_orders_with_template.short_description = "Yetkazib berilgan mahsulotlarni yuklash"
    actions = ['export_orders_with_template']

admin.site.register(Order, OrderAdmin)


class CartItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CartItemsResource


admin.site.register(CartItems, CartItemsAdmin)
