#!/usr/bin/python
import random
import pgzrun
from pgzero.keyboard import keys, keyboard
from menu import Menu
from game_entities import ActiveHero
from chess_pieces import Pawn, Rook, Queen, Knight

# Inicializa o menu
menu = Menu()
game_active = False  # Variável para indicar que o jogo está ativo

WIDTH = 800
HEIGHT = 600
TITLE = "Automatic Alternated Turn"

# -----------------------------
# OBJECT INSTANCES
# -----------------------------
pieces = [
    Pawn(WIDTH // 2, HEIGHT // 2),
    Rook(WIDTH // 2 + 30, HEIGHT // 2),
    Queen(WIDTH // 2 - 30, HEIGHT // 2),
    Knight(WIDTH // 2, HEIGHT // 2 - 30)
]

active_piece_index = 0
active_piece = pieces[active_piece_index]

switch_delay = 0

# -----------------------------
# GLOBAL FUNCTION: update()
# Called automatically by pgzrun every frame.
# -----------------------------
def update():
    global active_piece, active_piece_index, switch_delay
    dt = 1/60

    if keyboard.tab and switch_delay <= 0:
        active_piece_index = (active_piece_index + 1) % len(pieces)
        active_piece = pieces[active_piece_index]
        switch_delay = 0.3
    if switch_delay > 0:
        switch_delay -= dt

    active_piece.update(dt)

    speed = 3
    for piece in pieces:
        piece.update_position(speed)

# -----------------------------
# Scheduled functions using clock.schedule_interval.
# Chamam periodicamente os métodos de animação, turno e timer para todas as peças.
# -----------------------------
def animate_all():
    for piece in pieces:
        piece.animate_sprite()

def turn_all():
    for piece in pieces:
        piece.update_turn()

def timer_all():
    for piece in pieces:
        piece.check_turn_timer()

# Agendamento único para todas as peças
clock.schedule_interval(animate_all, 0.1)
clock.schedule_interval(turn_all, 0.1)
clock.schedule_interval(timer_all, 0.1)

# -----------------------------
# GLOBAL FUNCTION: draw()
# Draws all objects on the screen.
# -----------------------------
def draw():
    screen.clear()
    active_piece.draw()
    #
    screen.draw.text(f"Ativo: {active_piece.name}", center=(400, 50), fontsize=30, color="yellow")
    for piece in pieces:
        piece.draw()



pgzrun.go()
