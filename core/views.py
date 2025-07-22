from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo, GameOfLife
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from .game_of_life_services import update_game, stochastic_update
import json

def lista_todos(request):
    todos = ToDo.objects.all()
    return render(request, 'todos/todos.html', {'todos': todos})

@csrf_protect
def toggle_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(ToDo, id=todo_id)
        todo.completado = not todo.completado
        todo.save()
    return redirect('lista_todos')

@csrf_protect
def eliminar_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(ToDo, id=todo_id)
        todo.delete()
    return redirect('lista_todos')

@csrf_protect
def crear_todo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        if titulo:
            ToDo.objects.create(titulo=titulo, completado=False)
    return redirect('lista_todos')

def editar_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    if request.method == 'POST':
        nuevo_titulo = request.POST.get('titulo')
        if nuevo_titulo:
            todo.titulo = nuevo_titulo
            todo.save()
            return redirect('lista_todos')
    return render(request, 'todos/editar.html', {'todo': todo})

@csrf_exempt
def crear_juego(request):
    if request.method == "POST":
        data = json.loads(request.body)
        juego = GameOfLife.objects.create(
            titulo=data["titulo"],
            incertidumbre=data["incertidumbre"],
            descripcion=data["descripcion"],
            seconds_per_tick=data["seconds_per_tick"],
            dimension=data["dimension"],
            matriz=data["matriz"]
        )
        return JsonResponse({"id": juego.id, "mensaje": "Juego creado exitosamente."})

@csrf_exempt
def eliminar_juego(request, id):
    if request.method == "DELETE":
        juego = get_object_or_404(GameOfLife, id=id)
        juego.delete()
        return JsonResponse({"mensaje": "Juego eliminado exitosamente."})

@csrf_exempt
def cambiar_titulo_descripcion(request, id):
    if request.method == "PATCH":
        data = json.loads(request.body)
        juego = get_object_or_404(GameOfLife, id=id)
        if "titulo" in data:
            juego.titulo = data["titulo"]
        if "descripcion" in data:
            juego.descripcion = data["descripcion"]
        juego.save()
        return JsonResponse({"mensaje": "Título/Descripción actualizados."})

@csrf_exempt
def cambiar_seconds_per_tick(request, id):
    if request.method == "PATCH":
        data = json.loads(request.body)
        juego = get_object_or_404(GameOfLife, id=id)
        juego.seconds_per_tick = data["seconds_per_tick"]
        juego.save()
        return JsonResponse({"mensaje": "Tiempo por tick actualizado."})

@csrf_exempt
def cambiar_incertidumbre(request, id):
    if request.method == "PATCH":
        data = json.loads(request.body)
        juego = get_object_or_404(GameOfLife, id=id)
        juego.incertidumbre = data["incertidumbre"]
        juego.save()
        return JsonResponse({"mensaje": "Incertidumbre actualizada."})

@csrf_exempt
def toggle_matriz(request, id):
    if request.method == "PATCH":
        juego = get_object_or_404(GameOfLife, id=id)
        if not juego.matriz or not juego.matriz[0] or not isinstance(juego.matriz[0][0], bool):
            return JsonResponse({"error": "Matriz inválida o vacía."}, status=400)
        first_value = juego.matriz[0][0]
        new_value = not first_value
        juego.matriz = [[new_value for _ in row] for row in juego.matriz]
        juego.save()
        return JsonResponse({"mensaje": f"Matriz cambiada a todos {'True' if new_value else 'False'}."})
    
@csrf_exempt
def update_juego(request, game_id):
    juego = get_object_or_404(GameOfLife, id=game_id)
    update_game(juego)      
    stochastic_update(juego) 
    juego.save()
    return JsonResponse({'matriz': juego.matriz})

    
def lista_juegos(request):
    juegos = GameOfLife.objects.all()
    return render(request, 'vida/game_list.html', {'juegos': juegos})

def detalle_juego(request, game_id):
    juego = get_object_or_404(GameOfLife, id=game_id)
    return render(request, 'vida/game_detail.html', {'juego': juego})