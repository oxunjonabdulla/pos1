import os
from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages
from import_export.admin import ImportExportMixin
from modeltranslation.admin import TranslationAdmin
from datetime import datetime

from BOLT.settings import BASE_DIR
from .models import Maxsulot, OrderItems, Order, CartItems, Kategoriya, Department
from .resources import MaxsulotResource, OrderResource, OrderItemsResource, CartItemsResource


# Base Admin for Reusability
class BaseModelAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = []
    list_filter = []
    ordering = ['id']
    date_hierarchy = None


@admin.register(Department)
class DepartmentAdmin(BaseModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = []


@admin.register(Kategoriya)
class KategoriyaAdmin(BaseModelAdmin, TranslationAdmin):
    list_display = ['nomi', 'image', 'department']
    search_fields = ['nomi', 'department__name']
    list_filter = ['department']
    fieldsets = (
        (None, {'fields': ('nomi', 'image', 'department')}),)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Maxsulot)
class MaxsulotAdmin(BaseModelAdmin, TranslationAdmin):
    resource_class = MaxsulotResource
    list_display = ['id', 'nomi', 'kategoriya', 'department', 'foydalanuvchi', 'razmer', 'ball']
    search_fields = ['nomi', 'foydalanuvchi__username', 'kategoriya__nomi', 'department__name']
    list_filter = ['kategoriya', 'department', 'foydalanuvchi']
    fieldsets = (
        (None, {'fields': ('nomi', 'rasm', 'kategoriya', 'department', 'foydalanuvchi', 'razmer', 'qoshimcha', 'ball')}),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CartItems)
class CartItemsAdmin(BaseModelAdmin):
    resource_class = CartItemsResource
    list_display = ['id', 'foydalanuvchi', 'maxsulot', 'soni']
    search_fields = ['foydalanuvchi__username', 'maxsulot__nomi']
    list_filter = ['foydalanuvchi']
    fieldsets = (
        (None, {'fields': ('foydalanuvchi', 'maxsulot', 'soni')}),
    )


@admin.register(OrderItems)
class OrderItemsAdmin(BaseModelAdmin):
    resource_class = OrderItemsResource
    list_display = ['id', 'foydalanuvchi', 'maxsulot', 'soni']
    search_fields = ['foydalanuvchi__username', 'maxsulot__nomi']
    list_filter = ['foydalanuvchi']
    fieldsets = (
        (None, {'fields': ('foydalanuvchi', 'maxsulot', 'soni')}),
    )


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    resource_class = OrderResource
    list_display = ['id', 'foydalanuvchi', 'status', 'jami_maxsulot', 'created_at', 'updated_at']
    search_fields = ['foydalanuvchi__username', 'maxsulotlar__maxsulot__nomi']
    list_filter = ['status', 'created_at', 'kimga']
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('foydalanuvchi', 'maxsulotlar', 'jami_maxsulot', 'status', 'bekor_qilish_sababi')}),
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('qoshimcha_rasm', 'qoshimcha_matn', 'kimga')}),
    )
    filter_horizontal = ['maxsulotlar']

    # Export orders using an XLSX template
    def export_orders_with_template(self, request, queryset):
        template_path = os.path.join(BASE_DIR, "static", "buyurtmalar1.xlsx")

        if not os.path.exists(template_path):
            messages.error(request, f"Template not found: {template_path}")
            return

        filtered_queryset = queryset.filter(status='2')  # Example filter for status '2'

        if not filtered_queryset.exists():
            messages.warning(request, "No matching orders found.")
            return

        resource = self.resource_class()
        try:
            xlsx_content = resource.export_to_template_xlsx(filtered_queryset, template_path)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"buyurtmalar_{timestamp}.xlsx"

            response = HttpResponse(
                xlsx_content,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            messages.error(request, f"Error exporting orders: {str(e)}")

    export_orders_with_template.short_description = "Export Delivered Orders"
    actions = ['export_orders_with_template']
