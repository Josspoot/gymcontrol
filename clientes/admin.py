from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Cliente, Membresia, RegistroEntrada


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('tipo',)
    search_fields = ('cliente__nombre', 'cliente__matricula')

    def estado(self, obj):
        if obj.activa:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                'ACTIVA'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">{}</span>',
                'VENCIDA'
            )

    estado.short_description = "Estado"



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'matricula', 'telefono')
    search_fields = ('nombre', 'matricula')


@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_hora')
    list_filter = ('fecha_hora',)
