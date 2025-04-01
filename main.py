#!/usr/bin/python
import random
import pgzrun

from pgzero.keyboard import keys, keyboard

from game_entities import ActiveHero
from chess_pieces import Piece, ActivePiece, ThinkingPiece, MovingPiece, PieceAndante
from fight_manager import Fight
from menu import Menu
import config

# Inicializa o menu
menu = Menu(music)

game_active = False  # Variável para indicar que o jogo está ativo
WIDTH = 800
HEIGHT = 600
TITLE = "Correr ou Lutar"
config.current_fight = None
#music.play('background')

# -----------------------------
# OBJECT INSTANCES
# -----------------------------
active_pieces = [
    ActivePiece(WIDTH // 2, HEIGHT // 2 + 270, 'pawn'),
    ActivePiece(WIDTH // 2 + 270, HEIGHT // 2, 'rook'),
    ActivePiece(WIDTH // 2 - 30, HEIGHT // 2, 'queen'),
    ActivePiece(WIDTH // 2, HEIGHT // 2 - 30, 'knight'),
    #ActivePiece(WIDTH // 2, HEIGHT // 2 - 30, 'bishop'),
]

pieces = [
    ThinkingPiece(WIDTH // 2, HEIGHT // 2 - 270, 'pawn'),
    ThinkingPiece(WIDTH // 2 - 270, HEIGHT // 2, 'rook'),
    PieceAndante(WIDTH // 2 - 90, HEIGHT // 2, 'queen'),
    PieceAndante(WIDTH // 2, HEIGHT // 2 - 60, 'knight', 'down'),
    #Piece(WIDTH // 2, HEIGHT // 2 - 80, 'bishop'),
]

active_piece_index = 0
active_piece = active_pieces[active_piece_index]

switch_delay = 0

peao = active_pieces[0]
torre = pieces[1]
#bispo1 = active_pieces[4]
#bispo2 = pieces[4]
current_fight = Fight(peao,torre)

# -----------------------------
# Atualiza o estado global no update()
# -----------------------------
def update():
    screen.clear()
    global active_piece, active_piece_index, switch_delay

    dt = 1/60

    # Enquanto o menu estiver ativo, ele controla as atualizações
    if menu.active:
        menu.update()
    else:
        # Aqui você pode chamar as atualizações do jogo principal, por exemplo:
        if keyboard.tab and switch_delay <= 0:
            active_piece_index = (active_piece_index + 1) % len(active_pieces)
            active_piece = active_pieces[active_piece_index]
            switch_delay = 0.3
        if switch_delay > 0:
            switch_delay -= dt

        if current_fight.active:
            current_fight.update()

        active_piece.update_position(speed=2)
        # Atualizações das peças controladas
        for piece in active_pieces:
            if piece != active_piece:
                piece.update_idle()

        # Atualizações automáticas para as peças não controladas
        for piece in pieces:
            piece.update_position(speed=2)
            piece.animate_sprite()
    
# -----------------------------
# GLOBAL FUNCTION: draw()
# Draws all objects on the screen.
# -----------------------------
def draw():
    screen.clear()

    if menu.active:
        # Desenha o menu
        menu.draw(screen)
    else:
        # Desenha o jogo principal
        
        # Informações na tela
        screen.draw.text(f"Ativo: {active_piece.kind} - TAB muda para outro - ESC para voltar", center=(400, 50), fontsize=30, color="yellow")

        # Desenha as peças ativas
        for piece in active_pieces:
            piece.draw()

        # Desenha as peças não controladas
        for piece in pieces:
            piece.draw()

        # Desenha a luta, se houver
        if current_fight.active:
            current_fight.draw()

def on_mouse_down(pos):
    # Passa o clique do mouse para o menu, caso ele esteja ativo
    if menu.active:
        menu.on_mouse_down(pos)

def on_key_down(key):
    # Pressionar ESC retorna ao menu
    if not menu.active and key == keys.ESCAPE:
        menu.active = True  # Retorna ao menu
    elif menu.active and key == keys.ESCAPE:
        menu.active = False  # Sai do menu para o jogo principal

pgzrun.go()
