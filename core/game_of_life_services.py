from django.core.exceptions import ValidationError
from core.models import GameOfLife
import random

def crear_juego(titulo: str, descripcion: str, incertidumbre: float, segundos_por_tick: float, dimension: list[int], matriz: list[list[bool]]) -> GameOfLife:
    if not (0.0 <= incertidumbre <= 1.0):
        raise ValidationError("La incertidumbre debe estar entre 0.0 y 1.0")
    if segundos_por_tick <= 0:
        raise ValidationError("El tiempo por tick debe ser mayor a 0")
    if len(dimension) != 2 or not all(isinstance(x, int) and x > 0 for x in dimension):
        raise ValidationError("La dimensión debe ser una lista de dos enteros positivos")
    
    return GameOfLife.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        incertidumbre=incertidumbre,
        segundos_por_tick=segundos_por_tick,
        dimension=dimension,
        matriz=matriz
    )

def toggle_matriz(juego: GameOfLife) -> None:
    if not juego.matriz or not juego.matriz[0]:
        raise ValidationError("La matriz está vacía o mal formada")

    primera = juego.matriz[0][0]
    nuevo_valor = not primera
    filas, columnas = juego.dimension
    juego.matriz = [[nuevo_valor for _ in range(columnas)] for _ in range(filas)]
    juego.save()

def cambiar_tick(juego: GameOfLife, nuevo_tick: float) -> None:
    if nuevo_tick <= 0:
        raise ValidationError("El tiempo por tick debe ser mayor a 0")
    juego.segundos_por_tick = nuevo_tick
    juego.save()

def cambiar_titulo_descripcion(juego: GameOfLife, nuevo_titulo: str, nueva_descripcion: str) -> None:
    juego.titulo = nuevo_titulo
    juego.descripcion = nueva_descripcion
    juego.save()

def update_game(juego: GameOfLife) -> None:
    """
    Avanza una generación según las reglas de Conway:
      - Célula viva con 2 o 3 vecinas vivas sobrevive.
      - Célula muerta con exactamente 3 vecinas vivas nace.
      - En otro caso la célula muere o permanece muerta.
    """
    filas, columnas = juego.dimension
    vieja = juego.matriz
    nueva = [[False]*columnas for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            vivas = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < filas and 0 <= nj < columnas and vieja[ni][nj]:
                        vivas += 1

            if vieja[i][j]:
                nueva[i][j] = vivas in (2, 3)
            else:
                nueva[i][j] = (vivas == 3)

    juego.matriz = nueva
    juego.save()

def cambiar_incertidumbre(juego: GameOfLife, nueva_incertidumbre: float) -> None:
    if not 0.0 <= nueva_incertidumbre <= 1.0:
        raise ValidationError("La incertidumbre debe estar entre 0 y 1")
    juego.incertidumbre = nueva_incertidumbre
    juego.save()

def eliminar_juego(juego: GameOfLife) -> None:
    juego.delete()

def stochastic_update(juego: GameOfLife) -> None:
    """
    Aplica una actualización estocástica donde cada celda tiene probabilidad
    'incertidumbre' de cambiar su estado (de viva a muerta o viceversa).
    """
    filas, columnas = juego.dimension
    actual = juego.matriz
    nueva = [[actual[i][j] for j in range(columnas)] for i in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            if random.random() < juego.incertidumbre:
                nueva[i][j] = not actual[i][j]
    
    juego.matriz = nueva
    juego.save()