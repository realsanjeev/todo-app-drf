from django.contrib import admin
from task_api.models import TodoTask


# Register your models here.
class TodoTaskAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "completed", "updated", "public")
    list_filter = ("completed", "public", "timestamp", "updated")
    search_fields = ("timestamp", "updated")

    exclude = ["timestamp", "updated"]

    # it contains the fields that can be changed by admin from admin ui
    fieldsets = (
        (None, {"fields": ("task", "desc", "completed", "public")}),
        ("Readonly Fields", {"fields": ("user",)}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(TodoTask, TodoTaskAdmin)
