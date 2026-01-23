from django.contrib import admin
from .models import Equipment, Task, Update

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
	list_display = ("name", "status", "location", "purchase_date", "created_at")
	search_fields = ("name", "location")
	list_filter = ("status",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("title", "equipment", "status", "due_date", "completed", "assignee")
	search_fields = ("title", "equipment__name", "assignee__username")
	list_filter = ("status", "completed", "recurrence", "assignee")

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
	list_display = ("equipment", "timestamp")
	search_fields = ("equipment__name", "content")
