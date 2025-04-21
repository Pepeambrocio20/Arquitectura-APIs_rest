from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
import re

# CRUD de usuarios con contraseña cifrada
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# CRUD de mascotas
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

    def list(self, request, *args, **kwargs):
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            queryset = Mascota.objects.filter(usuario_id=usuario_id)
        else:
            queryset = Mascota.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id)
        serializer.save(usuario=usuario)

    def update(self, request, *args, **kwargs):
        mascota = self.get_object()
        usuario_id = request.data.get('usuario')
        if str(mascota.usuario.id) != str(usuario_id):
            raise PermissionDenied("🚫 No tienes permiso para modificar esta mascota.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        mascota = self.get_object()
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id and str(mascota.usuario.id) != str(usuario_id):
            raise PermissionDenied("🚫 No tienes permiso para eliminar esta mascota.")
        return super().destroy(request, *args, **kwargs)

# CRUD de reseñas
class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

    def list(self, request, *args, **kwargs):
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            queryset = Reseña.objects.filter(usuario_id=usuario_id)
        else:
            queryset = Reseña.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id)
        serializer.save(usuario=usuario)

    def update(self, request, *args, **kwargs):
        resena = self.get_object()
        usuario_id = request.data.get('usuario')
        if str(resena.usuario.id) != str(usuario_id):
            raise PermissionDenied("🚫 No tienes permiso para modificar esta reseña.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        resena = self.get_object()
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id and str(resena.usuario.id) != str(usuario_id):
            raise PermissionDenied("🚫 No tienes permiso para eliminar esta reseña.")
        return super().destroy(request, *args, **kwargs)

# CRUD de historial médico
class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer

    def list(self, request, *args, **kwargs):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            queryset = HistorialMedico.objects.filter(mascota_id=mascota_id)
        else:
            queryset = HistorialMedico.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        mascota_id = self.request.data.get('mascota')
        mascota = Mascota.objects.get(id=mascota_id)
        serializer.save(mascota=mascota)

    def update(self, request, *args, **kwargs):
        historial = self.get_object()
        mascota_id = request.data.get('mascota')
        if str(historial.mascota.id) != str(mascota_id):
            raise PermissionDenied("🚫 No puedes modificar un historial de otra mascota.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        historial = self.get_object()
        mascota_id = request.query_params.get('mascota_id')
        if mascota_id and str(historial.mascota.id) != str(mascota_id):
            raise PermissionDenied("🚫 No puedes eliminar un historial de otra mascota.")
        return super().destroy(request, *args, **kwargs)

# CRUD de recordatorios
class RecordatorioViewSet(viewsets.ModelViewSet):
    queryset = Recordatorio.objects.all()
    serializer_class = RecordatorioSerializer

    def list(self, request, *args, **kwargs):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            queryset = Recordatorio.objects.filter(mascota_id=mascota_id)
        else:
            queryset = Recordatorio.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        mascota_id = self.request.data.get('mascota')
        mascota = Mascota.objects.get(id=mascota_id)
        serializer.save(mascota=mascota)

    def update(self, request, *args, **kwargs):
        recordatorio = self.get_object()
        mascota_id = request.data.get('mascota')
        if str(recordatorio.mascota.id) != str(mascota_id):
            raise PermissionDenied("🚫 No puedes modificar un recordatorio de otra mascota.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        recordatorio = self.get_object()
        mascota_id = request.query_params.get('mascota_id')
        if mascota_id and str(recordatorio.mascota.id) != str(mascota_id):
            raise PermissionDenied("🚫 No puedes eliminar un recordatorio de otra mascota.")
        return super().destroy(request, *args, **kwargs)

# Login personalizado
class LoginUsuarioView(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        password = request.data.get("password")

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "Correo no registrado"}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, usuario.password):
            return Response({
                "id": usuario.id,
                "nombre_completo": usuario.nombre_completo,
                "nombre_usuario": usuario.nombre_usuario,
                "correo": usuario.correo,
                "direccion": usuario.direccion
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def promedio_recorrido_diario(request):
    mascota_id = request.query_params.get('mascota_id')
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    if not (mascota_id and fecha_inicio and fecha_fin):
        return Response({"error": "Se requieren los parámetros: mascota_id, fecha_inicio, fecha_fin."}, status=400)

    eventos = HistorialMedico.objects.filter(
        mascota_id=mascota_id,
        fecha__range=[fecha_inicio, fecha_fin]
    )

    total_km = 0
    total_dias = set()

    for evento in eventos:
        match = re.search(r"(\d+(\.\d+)?)\s*km", evento.descripcion.lower())
        if match:
            km = float(match.group(1))
            total_km += km
            total_dias.add(evento.fecha)

    promedio = total_km / len(total_dias) if total_dias else 0

    return Response({
        "mascota_id": mascota_id,
        "total_kilometros": total_km,
        "dias_registrados": len(total_dias),
        "promedio_diario_km": round(promedio, 2)
    })

@api_view(['GET'])
def total_vacunas_por_rango(request):
    mascota_id = request.query_params.get('mascota_id')
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    if not (mascota_id and fecha_inicio and fecha_fin):
        return Response({"error": "Faltan parámetros."}, status=400)

    eventos = HistorialMedico.objects.filter(
        mascota_id=mascota_id,
        fecha__range=[fecha_inicio, fecha_fin]
    ).filter(
        Q(titulo__icontains="vacuna") | Q(descripcion__icontains="vacuna")
    )

    return Response({
        "mascota_id": mascota_id,
        "total_vacunas": eventos.count()
    })

