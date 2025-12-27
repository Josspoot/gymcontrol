from django.core.management.base import BaseCommand
from django.utils import timezone
from clientes.models import Cliente, Membresia, RegistroEntrada



class Command(BaseCommand):
    help = "Registrar entrada de cliente por matrícula"

    def handle(self, *args, **kwargs):
        matricula = input("Ingrese su matrícula: ")

        try:
            cliente = Cliente.objects.get(matricula=matricula)
        except Cliente.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Matrícula no encontrada"))
            return

        membresia = (
            Membresia.objects
            .filter(cliente=cliente, activa=True)
            .order_by('-fecha_fin')
            .first()
        )

        if not membresia or membresia.dias_restantes() < 0:
            self.stdout.write(
                self.style.ERROR("🚫 Membresía vencida. Por favor acuda a recepción.")
            )
            return

        RegistroEntrada.objects.create(
            cliente=cliente,
            fecha_hora=timezone.now()
        )

        if membresia.esta_por_vencer():
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️ Bienvenido {cliente.nombre}. "
                    f"Su membresía vence en {membresia.dias_restantes()} día(s)."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Acceso permitido. Bienvenido {cliente.nombre}."
                )
            )