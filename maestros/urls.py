from django.urls import path
from . import views

urlpatterns = [
    # Menú principal del módulo "maestros"
    path('', views.menu_maestros, name='menu_maestros'),

    # Sección: Terceros
    path('terceros/', views.menu_terceros, name='menu_terceros'),
    path('terceros/nuevo/', views.crear_tercero, name='crear_tercero'),
    path('terceros/modificar/', views.modificar_tercero, name='modificar_tercero'),
    path('terceros/modificar/<int:pk>/', views.editar_tercero, name='editar_tercero'),
    path('terceros/visualizar/', views.visualizar_terceros, name='visualizar_terceros'),
]