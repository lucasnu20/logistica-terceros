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
    # Sección: Materiales
    path('materiales/', views.menu_materiales, name='menu_materiales'),
    path('materiales/crear/', views.material_crear, name='material_crear'),
    path('materiales/listar/', views.material_listar, name='material_listar'),
    path('materiales/editar/', views.material_editar_menu, name='material_editar_menu'),
    path('materiales/editar/<int:pk>/', views.material_editar, name='material_editar'),
    path('materiales/carga_masiva/', views.material_carga_masiva, name='material_carga_masiva'),
]