from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, default="Sin dirección")
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre_usuario

class Mascota(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_propietario = models.CharField(max_length=100, default="Sin nombre")
    direccion = models.CharField(max_length=255, default="Sin dirección")
    telefono = models.CharField(max_length=15, default="0000000000")
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField(default=0)
    especie = models.CharField(max_length=50, default="Desconocida")
    raza = models.CharField(max_length=50, default="Desconocida")
    fecha_nacimiento = models.DateField(default=timezone.now)
    color = models.CharField(max_length=30, default="Sin definir")
    peso = models.FloatField(default=0.0)
    descripcion = models.TextField(default="Ninguna")
    enfermedades = models.TextField(default="Ninguna")
    sexo = models.CharField(max_length=10, choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')], default='Macho')

    def __str__(self):
        return self.nombre

class Reseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField(default="")
    calificacion = models.IntegerField(default=5)  # 1 a 5

    def __str__(self):
        return f"Reseña de {self.usuario.nombre_usuario}"

class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="Registro")
    descripcion = models.TextField(default="Ninguna")
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Recordatorio(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="Recordatorio")
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    lugar = models.CharField(max_length=100, default="Lugar no definido")
    descripcion = models.TextField(default="Ninguna")

    def __str__(self):
        return self.titulo
