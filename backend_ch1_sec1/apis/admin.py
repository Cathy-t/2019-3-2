import hashlib

from django.contrib import admin

# Register your models here.
from apis.models import App

# admin.site.register(App)


@admin.register(App)
class ApisAppAdmin(admin.ModelAdmin):
    # 指定admin模块，显示哪些信息
    fields = ['name', 'application', 'category', 'url', 'publish_date', 'desc']
    pass

    def save_model(self, request, obj, form, change):
        src = obj.category + obj.application
        appid = hashlib.md5(src.encode('utf-8').hexdigest())
        obj.appid = appid
        super().save_model(request, obj, form, change)