from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet,
    MascotaViewSet,
    ReseñaViewSet,
    HistorialMedicoViewSet,
    RecordatorioViewSet,
    LoginUsuarioView  # 👈 Importación del login personalizado
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'resenas', ReseñaViewSet)
router.register(r'historial', HistorialMedicoViewSet)
router.register(r'recordatorios', RecordatorioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginUsuarioView.as_view(), name='login_usuario'),  # 👈 Nuevo login
]
