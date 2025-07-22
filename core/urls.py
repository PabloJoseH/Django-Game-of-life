from django.urls import path
from . import views

urlpatterns = [
    path('todos', views.lista_todos, name='lista_todos'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('crear/', views.crear_todo, name='crear_todo'),
    path('editar/<int:todo_id>/', views.editar_todo, name='editar_todo'),
    path('eliminar/<int:todo_id>/', views.eliminar_todo, name='eliminar_todo'),

    path('vida/update/<int:game_id>/', views.update_juego, name='update_juego'),
    path('vida/', views.lista_juegos, name='lista_juegos'),
    path('vida/<int:game_id>/', views.detalle_juego, name='detalle_juego'),
    path("vida/crear/", views.crear_juego, name="crear_juego"),
    path("vida/eliminar/<int:id>/", views.eliminar_juego, name="eliminar_juego"),
    path("vida/modificar/<int:id>/", views.cambiar_titulo_descripcion, name="cambiar_titulo_descripcion"),
    path("vida/tick/<int:id>/", views.cambiar_seconds_per_tick, name="cambiar_seconds_per_tick"),
    path("vida/incertidumbre/<int:id>/", views.cambiar_incertidumbre, name="cambiar_incertidumbre"),
    path("vida/toggle/<int:id>/", views.toggle_matriz, name="toggle_matriz"),
]