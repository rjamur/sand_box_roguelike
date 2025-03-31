#!/usr/bin/python
import random
import pgzrun
from pgzero.keyboard import keys
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
pawn = Pawn(WIDTH // 2, HEIGHT // 2)
rook = Rook(WIDTH // 2 + 30, HEIGHT // 2)

# -----------------------------
# GLOBAL FUNCTION: update()
# Called automatically by pgzrun every frame.
# -----------------------------
def update():
    speed = 3
    pawn.update_position(speed)
    rook.update_position(speed)


# -----------------------------
# Scheduled functions using clock.schedule_interval.
# They periodically call animation, turn, and timer methods.
# -----------------------------
def pawn_animate():
    pawn.animate_sprite()

def pawn_turn():
    pawn.update_turn()

def pawn_timer():
    pawn.check_turn_timer()

def rook_animate():
    rook.animate_sprite()

def rook_turn():
    rook.update_turn()

def rook_timer():
    rook.check_turn_timer()


# Scheduling for the active hero.
clock.schedule_interval(pawn_animate, 0.1)   # animate hero's walk
clock.schedule_interval(pawn_turn, 0.1)      # update hero's turn if active
clock.schedule_interval(pawn_timer, 0.1)     # check timer for hero's turn

clock.schedule_interval(rook_animate, 0.1)   # animate hero's walk
clock.schedule_interval(rook_turn, 0.1)      # update hero's turn if active
clock.schedule_interval(rook_timer, 0.1)     # check timer for hero's turn


# -----------------------------
# GLOBAL FUNCTION: draw()
# Draws all objects on the screen.
# -----------------------------
def draw():
    screen.clear()
    pawn.draw()
    rook.draw()

    #adversary.draw()
    #queen_piece.draw()


pgzrun.go()
