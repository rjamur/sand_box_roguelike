#!/usr/bin/python
import random
import pgzrun
import os

from pgzero.keyboard import keys, keyboard

from game_entities import ActiveHero
from chess_pieces import Piece, ActivePiece, ThinkingPiece
from fight_manager import Fight
from menu import Menu
import config

# Inicializa o menu
menu = Menu()
game_active = False  # Variável para indicar que o jogo está ativo
WIDTH = 800
HEIGHT = 600
TITLE = "Automatic Alternated Turn"
config.current_fight = None

# -----------------------------
# OBJECT INSTANCES
# -----------------------------
active_pieces = [
    ActivePiece(WIDTH // 2, HEIGHT // 2 + 270, 'pawn'),
    ActivePiece(WIDTH // 2 + 270, HEIGHT // 2, 'rook'),
    #ActivePiece(WIDTH // 2 - 30, HEIGHT // 2, 'queen'),
    #ActivePiece(WIDTH // 2, HEIGHT // 2 - 30, 'knight')
]

pieces = [
    ThinkingPiece(WIDTH // 2, HEIGHT // 2 - 270, 'pawn'),
    ThinkingPiece(WIDTH // 2 - 270, HEIGHT // 2, 'rook'),
    #Piece(WIDTH // 2 - 90, HEIGHT // 2, 'queen'),
    #Piece(WIDTH // 2, HEIGHT // 2 - 60, 'knight')
]

active_piece_index = 0
active_piece = active_pieces[active_piece_index]

switch_delay = 0

peao = active_pieces[0]
torre = active_pieces[1]
current_fight = Fight(peao,torre)

# ------------ Fight ---------------------
#
# -----------------------------
# Detecta colisão e inicia luta
# -----------------------------
def check_collisions():
    for piece in pieces:
        if active_piece.actor.colliderect(piece.actor):  # Verifica se há colisão
            start_fight(active_piece, piece)

# -----------------------------
# Atualiza o estado global no update()
# -----------------------------
def update():
    global active_piece, active_piece_index, switch_delay

    dt = 1/60

    if keyboard.tab and switch_delay <= 0:
        active_piece_index = (active_piece_index + 1) % len(active_pieces)
        active_piece = active_pieces[active_piece_index]
        switch_delay = 0.3
    if switch_delay > 0:
        switch_delay -= dt

    if current_fight.active:
        current_fight.update()

    active_piece.update_position(speed=2)

    # Atualizações automáticas para as peças não controladas
    for piece in pieces:
        piece.animate_sprite()
    
    def animate_sprite(self):
        """Anima o sprite da peça durante o movimento."""
        if self.moving:  # Verifica se está se movendo
            self.current_frame = (
                self.current_frame + 1
            ) % len(self.sprites[self.current_direction])  # Loop nos frames
            self.actor.image = self.sprites[self.current_direction][self.current_frame]

# -----------------------------
# Scheduled functions using clock.schedule_interval.
# Chamam periodicamente os métodos de animação, turno e timer para todas as peças.
# -----------------------------
def animate_all():
    for piece in active_pieces:
        piece.animate_sprite()

    for piece in pieces:
        piece.animate_sprite()

def turn_all():
    for piece in active_pieces:
        piece.update_turn()

    for piece in pieces:
        piece.update_turn()

def timer_all():
    for piece in active_pieces:
        piece.check_turn_timer()

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

    # Informações na tela
    screen.draw.text(f"Ativo: {active_piece.kind}", center=(400, 50), fontsize=30, color="yellow")

    # Desenha as peças ativas
    for piece in active_pieces:
        piece.draw()

    # Desenha as peças não controladas
    for piece in pieces:
        piece.draw()

    # Desenha a luta, se houver
    if current_fight.active:
        current_fight.draw()

pgzrun.go()
