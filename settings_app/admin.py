from django.contrib import admin

from .models import AdminParol, SiteSettings

admin.site.register(AdminParol)
admin.site.register(SiteSettings)
