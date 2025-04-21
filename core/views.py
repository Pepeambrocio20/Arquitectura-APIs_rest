from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializers import *

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

    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            return Mascota.objects.filter(usuario_id=usuario_id)
        return Mascota.objects.none()

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id)
        serializer.save(usuario=usuario)

# CRUD de reseñas
class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            return Reseña.objects.filter(usuario_id=usuario_id)
        return Reseña.objects.none()

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id)
        serializer.save(usuario=usuario)

# CRUD de historial médico
class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer

    def get_queryset(self):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            return HistorialMedico.objects.filter(mascota_id=mascota_id)
        return HistorialMedico.objects.none()

    def perform_create(self, serializer):
        mascota_id = self.request.data.get('mascota')
        mascota = Mascota.objects.get(id=mascota_id)
        serializer.save(mascota=mascota)

# CRUD de recordatorios
class RecordatorioViewSet(viewsets.ModelViewSet):
    queryset = Recordatorio.objects.all()
    serializer_class = RecordatorioSerializer

    def get_queryset(self):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            return Recordatorio.objects.filter(mascota_id=mascota_id)
        return Recordatorio.objects.none()

    def perform_create(self, serializer):
        mascota_id = self.request.data.get('mascota')
        mascota = Mascota.objects.get(id=mascota_id)
        serializer.save(mascota=mascota)

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
