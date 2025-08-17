from django.contrib import admin
from .models import Tercero

@admin.register(Tercero)
class TerceroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuit', 'contacto_principal', 'region')
    search_fields = ('nombre', 'cuit')
