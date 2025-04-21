import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petcare_project.settings")
django.setup()

from core.models import Usuario, Mascota, HistorialMedico, Recordatorio, Reseña

def separador(titulo):
    print(f"\n--------------- {titulo} ---------------")

def consultar_usuario():
    try:
        user_id = int(input("🔍 Ingrese el ID del usuario a consultar: "))
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        print("❌ Usuario no encontrado.")
        return

    separador("Información del usuario")
    print(f"🧍 ID: {usuario.id}")
    print(f"📛 Nombre completo: {usuario.nombre_completo}")
    print(f"👤 Usuario: {usuario.nombre_usuario}")
    print(f"📧 Correo: {usuario.correo}")
    print(f"🏠 Dirección: {usuario.direccion}")

    separador("Mascotas registradas")
    mascotas = Mascota.objects.filter(usuario=usuario)
    if not mascotas:
        print("🔸 No tiene mascotas registradas.")
    for mascota in mascotas:
        print(f"\n🐾 Nombre: {mascota.nombre} ({mascota.especie})")
        print(f"   📌 Raza: {mascota.raza}")
        print(f"   🎨 Color: {mascota.color}")
        print(f"   ⏳ Edad: {mascota.edad} años - ⚖️ Peso: {mascota.peso}kg")
        print(f"   🔄 Sexo: {mascota.sexo}")
        print(f"   📝 Descripción: {mascota.descripcion}")
        print(f"   💊 Enfermedades: {mascota.enfermedades}")

    separador("Historial Médico")
    historiales = HistorialMedico.objects.filter(mascota__usuario=usuario)
    if not historiales:
        print("🔸 No hay registros médicos.")
    for h in historiales:
        print(f"\n📋 Mascota: {h.mascota.nombre}")
        print(f"   🗓️ Fecha: {h.fecha}")
        print(f"   🧾 Título: {h.titulo}")
        print(f"   📝 Descripción: {h.descripcion}")

    separador("Recordatorios")
    recordatorios = Recordatorio.objects.filter(mascota__usuario=usuario)
    if not recordatorios:
        print("🔸 No hay recordatorios registrados.")
    for r in recordatorios:
        print(f"\n🕑 Mascota: {r.mascota.nombre}")
        print(f"   📅 Fecha: {r.fecha} - {r.hora}")
        print(f"   📍 Lugar: {r.lugar}")
        print(f"   📌 Título: {r.titulo}")
        print(f"   📝 Descripción: {r.descripcion}")

    separador("Reseñas")
    resenas = Reseña.objects.filter(usuario=usuario)
    if not resenas:
        print("🔸 No ha escrito reseñas.")
    for r in resenas:
        print(f"\n⭐ Calificación: {r.calificacion}/5")
        print(f"📝 Comentario: {r.comentario}")

if __name__ == '__main__':
    consultar_usuario()
