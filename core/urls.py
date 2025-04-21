from django.urls import path, include
from .estadisticas import TotalEventosView
from .views import promedio_recorrido_diario
from .views import total_vacunas_por_rango
from .estadisticas import VisitasVeterinarioView
from .estadisticas import ConsolidadoHistorialView
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
    path('estadisticas/total_eventos/', TotalEventosView.as_view(), name='total_eventos'),
    path('estadisticas/promedio_recorrido/', promedio_recorrido_diario),
    path('estadisticas/total_vacunas/', total_vacunas_por_rango),
    path('estadisticas/visitas_veterinario/', VisitasVeterinarioView.as_view(), name='visitas_veterinario'),
    path('estadisticas/consolidado_historial/', ConsolidadoHistorialView.as_view(), name='consolidado_historial'),
    
]
