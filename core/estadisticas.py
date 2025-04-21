from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HistorialMedico
from datetime import datetime

class TotalEventosView(APIView):
    def get(self, request):
        mascota_id = request.query_params.get('mascota_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        eventos = HistorialMedico.objects.all()
        if mascota_id:
            eventos = eventos.filter(mascota_id=mascota_id)
        if fecha_inicio and fecha_fin:
            eventos = eventos.filter(fecha__range=[fecha_inicio, fecha_fin])

        total = eventos.count()

        return Response({
            "mascota_id": mascota_id,
            "total_eventos": total
        })

class VisitasVeterinarioView(APIView):
    def get(self, request):
        mascota_id = request.query_params.get('mascota_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        visitas = HistorialMedico.objects.all()

        if mascota_id:
            visitas = visitas.filter(mascota_id=mascota_id)
        if fecha_inicio and fecha_fin:
            visitas = visitas.filter(fecha__range=[fecha_inicio, fecha_fin])

        visitas = visitas.filter(titulo__icontains='veterinario')

        return Response({
            "mascota_id": mascota_id,
            "visitas_veterinario": visitas.count()
        })

class ConsolidadoHistorialView(APIView):
    def get(self, request):
        mascota_id = request.query_params.get('mascota_id')

        if not mascota_id:
            return Response({"error": "Debes especificar el ID de la mascota"}, status=400)

        historial = HistorialMedico.objects.filter(mascota_id=mascota_id).order_by('fecha')
        consolidado = []

        for evento in historial:
            consolidado.append({
                "fecha": evento.fecha,
                "titulo": evento.titulo,
                "descripcion": evento.descripcion
            })

        return Response({
            "mascota_id": mascota_id,
            "eventos": consolidado
        })
