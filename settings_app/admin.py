from django.contrib import admin

from .models import SiteSettings, AdminParol
admin.site.register(SiteSettings)
admin.site.register(AdminParol)
