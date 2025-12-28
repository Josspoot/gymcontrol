from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Cliente, Membresia, RegistroEntrada


# =========================
# ADMIN MEMBRESÍA
# =========================
@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'tipo',
        'fecha_inicio',
        'fecha_fin',
        'estado',
        'dias_restantes',
    )
    list_filter = ('tipo', 'fecha_fin')
    search_fields = ('cliente__nombre', 'cliente__matricula')

    def estado(self, obj):
        if obj.fecha_fin and obj.fecha_fin < timezone.now().date():
            return format_html(
                '<span style="color: red; font-weight: bold;">{}</span>',
                'VENCIDA'
            )
        return format_html(
            '<span style="color: green; font-weight: bold;">{}</span>',
            'ACTIVA'
        )

    estado.short_description = "Estado"

    def dias_restantes(self, obj):
        if not obj.fecha_fin:
            return "-"

        dias = (obj.fecha_fin - timezone.now().date()).days

        if dias <= 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">{}</span>',
                0
            )

        if dias <= 3:
            return format_html(
                '<span style="color: orange; font-weight: bold;">{}</span>',
                dias
            )

        return dias

    dias_restantes.short_description = "Días restantes"


# =========================
# ADMIN CLIENTE
# =========================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'matricula', 'telefono', 'ultima_entrada')
    search_fields = ('nombre', 'matricula')
    ordering = ('nombre',)

    def ultima_entrada(self, obj):
        entrada = obj.registroentrada_set.order_by('-fecha_hora').first()
        if entrada:
            return entrada.fecha_hora.strftime('%Y-%m-%d %H:%M')
        return "Nunca"

    ultima_entrada.short_description = "Última entrada"


# =========================
# ADMIN REGISTRO DE ENTRADAS
# =========================
@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_hora')
    list_filter = ('fecha_hora',)
    search_fields = ('cliente__nombre', 'cliente__matricula')
    ordering = ('-fecha_hora',)
