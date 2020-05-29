from django.contrib import admin

# Register your models here.
from authorization.models import User

# admin.site.register(User)


@admin.register(User)
class AuthorizationUserAdmin(admin.ModelAdmin):
    # 设置需要被屏蔽的属性
    exclude = ['open_id']
    pass