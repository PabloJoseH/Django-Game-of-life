from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ToDo(models.Model):
    titulo = models.CharField(max_length=200)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    
class GameOfLife(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    incertidumbre = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    segundos_por_tick = models.FloatField(validators=[MinValueValidator(0.001)])
    dimension = models.JSONField()  #lista dos enteros: [filas, columnas]
    matriz = models.JSONField()     # una matriz de booleanos

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.dimension[0]}x{self.dimension[1]})"