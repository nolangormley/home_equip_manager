from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('equip/', views.dashboard, name='dashboard'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/delete/', views.delete_equipment, name='delete_equipment'),
    path('equipment/<int:pk>/add_task/', views.add_task, name='add_task'),
    path('task/<int:pk>/toggle/', views.toggle_task, name='toggle_task'),
    path('equipment/<int:pk>/add_update/', views.add_update, name='add_update'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('task/<int:pk>/status/', views.update_task_status, name='update_task_status'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
]
