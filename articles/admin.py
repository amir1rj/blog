from django.contrib import admin
from .models import *
@admin.register(Article)
class ArticelAdmn(admin.ModelAdmin):
    list_display = ("__str__","status","title","showImages")
    list_editable = ("title","status",)
    list_filter = ("status",)
    search_fields = ("title","body")
# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
