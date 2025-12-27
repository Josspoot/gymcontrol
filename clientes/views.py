from django.shortcuts import render
from django.utils import timezone
from .models import Cliente

def registrar_entrada(request):
    mensaje = None
    estado = None  # ok | vencido | error

    if request.method == "POST":
        matricula = request.POST.get("matricula")

        try:
            cliente = Cliente.objects.get(matricula=matricula)

            membresia = cliente.membresia_set.order_by("-fecha_fin").first()

            if not membresia or membresia.fecha_fin < timezone.now().date():
                estado = "vencido"
                mensaje = "❌ Membresía vencida. Pase a recepción."
            else:
                estado = "ok"
                mensaje = f"✅ Bienvenido {cliente.nombre}. Puede pasar."

        except Cliente.DoesNotExist:
            estado = "error"
            mensaje = "❌ Matrícula no encontrada."

    return render(request, "clientes/registro_entrada.html", {
        "mensaje": mensaje,
        "estado": estado
    })
