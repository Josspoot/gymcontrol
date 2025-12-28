from django.shortcuts import render
from django.utils import timezone
from .models import Cliente, RegistroEntrada


def registrar_entrada(request):
    mensaje = None
    estado = None  # ok | vencido | error | duplicado

    if request.method == "POST":
        matricula = request.POST.get("matricula")
        hoy = timezone.localdate()

        try:
            cliente = Cliente.objects.get(matricula=matricula)

            # 🔍 Verificar membresía
            membresia = cliente.membresia_set.order_by("-fecha_fin").first()

            if not membresia or membresia.fecha_fin < hoy:
                estado = "vencido"
                mensaje = "❌ Membresía vencida. Pase a recepción."
                return render(request, "clientes/registro_entrada.html", {
                    "mensaje": mensaje,
                    "estado": estado
                })

            # 🔒 Verificar si ya ingresó hoy
            ya_ingreso = RegistroEntrada.objects.filter(
                cliente=cliente,
                fecha_hora__date=hoy
            ).exists()

            if ya_ingreso:
                estado = "error"
                mensaje = "⚠️ Acceso ya registrado el día de hoy."
            else:
                # ✅ Registrar entrada
                RegistroEntrada.objects.create(
                    cliente=cliente,
                    membresia_activa=True
                )
                estado = "ok"
                mensaje = f"✅ Bienvenido {cliente.nombre}. Puede pasar."

        except Cliente.DoesNotExist:
            estado = "error"
            mensaje = "❌ Matrícula no encontrada."

    return render(request, "clientes/registro_entrada.html", {
        "mensaje": mensaje,
        "estado": estado
    })
