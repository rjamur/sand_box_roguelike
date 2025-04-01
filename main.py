#!/usr/bin/python
"""
    Módulo principal usado pelo PGZero

    Aqui as funções update() e draw() são executadas constantemente
    Cerca de 60x por segundo

"""
import random
import pgzrun

from pgzero.keyboard import keys, keyboard

from game_entities import ActiveHero
from chess_pieces import Piece, ActivePiece, ThinkingPiece, MovingPiece, PieceAndante
from fight_manager import Fight
from menu import Menu
import config
from hall_manager import Hall
from map_manager import MapManager

# Inicializa o menu
menu = Menu(music)

game_active = False  # Variável para indicar que o jogo está ativo

# Configurações do jogo
WIDTH, HEIGHT = 1280, 704

TITLE = "Correr ou Lutar"

# Definindo as dimensões da tela com base no tamanho das salas (16 tiles de 64 pixels = 1024, 12 tiles de 64 pixels = 768)
#WIDTH = 16 * 64   # 1024 pixels
#HEIGHT = 11 * 64  # 704 pixels

# Instancia o MapManager e gera o dicionário de halls (salas)
map_manager = MapManager(grid_rows=4, grid_cols=4)
halls = map_manager.build_halls()

# Seleciona uma sala inicial aleatória
initial_key = random.choice(list(halls.keys()))
parts = initial_key.split("_")  # Exemplo: "room_1_2"
current_r, current_c = int(parts[1]), int(parts[2])
current_room = halls[initial_key]
print("Sala inicial escolhida:", initial_key)

# --------------------------------
# Cria personagens/peças de xadrez
# --------------------------------
active_pieces = [
    ActivePiece(WIDTH // 2, HEIGHT // 2 + 170, 'pawn'),
    #ActivePiece(WIDTH // 2 + 270, HEIGHT // 2, 'rook'),
    #ActivePiece(WIDTH // 2 - 30, HEIGHT // 2, 'queen'),
    #ActivePiece(WIDTH // 2, HEIGHT // 2 - 30, 'knight'),
    #ActivePiece(WIDTH // 2, HEIGHT // 2 - 70, 'bishop'),
]

pieces = [
    #ThinkingPiece(WIDTH // 2 - 30, HEIGHT // 2 - 170, 'pawn'),
    #ThinkingPiece(WIDTH // 2 - 270, HEIGHT // 2, 'rook'),
    PieceAndante(WIDTH // 2 - 90, HEIGHT // 2, 'queen'),
    #PieceAndante(WIDTH // 2, HEIGHT // 2 - 60, 'knight', 'down'),
    #Piece(WIDTH // 2, HEIGHT // 2 + 40, 'bishop'),
]

active_piece_index = 0
active_piece = active_pieces[active_piece_index]
switch_delay = 0

#peao = active_pieces[0]
#torre = pieces[1]
#bispo1 = active_pieces[4]
#bispo2 = pieces[4]
#current_fight = Fight(peao,torre)

# --- Variáveis de transição ---
transition_active = False      # Flag indicando se uma transição está em andamento
transition_direction = None    # "up", "down", "left" ou "right"
transition_progress = 0        # Acumulador de pixels deslocados na animação
transition_speed = 20          # Velocidade de transição (pixels por update)
target_room = None
target_r = None
target_c = None



def initiate_transition(direction):
    """
    Configura os parâmetros iniciais para iniciar a transição entre salas.
    """
    global transition_active, transition_direction, transition_progress
    global target_room, current_r, current_c, target_r, target_c

    transition_active = True
    transition_direction = direction
    transition_progress = 0

    # Calcula as coordenadas da sala destino com base na direção
    target_r, target_c = current_r, current_c
    if direction == "up":
        target_r -= 1
    elif direction == "down":
        target_r += 1
    elif direction == "left":
        target_c -= 1
    elif direction == "right":
        target_c += 1

    new_key = f"room_{target_r}_{target_c}"
    if new_key in halls:
        target_room = halls[new_key]
    else:
        # Se não existir sala na direção desejada, cancela a transição
        transition_active = False

def finish_transition():
    """
    Conclui a transição, definindo a nova sala atual e reposicionando o jogador.
    """
    global transition_active, current_room, current_r, current_c, active_piece, transition_progress
    global target_room, target_r, target_c, transition_direction, new_pos

    transition_active = False
    transition_progress = 0
    current_room = target_room
    current_r, current_c = target_r, target_c

    # Posiciona o active_piece na nova sala – um pouco distante da porta oposta àquela que foi usada
    if transition_direction == "up":
        new_pos = (WIDTH // 2, HEIGHT - 60)
    elif transition_direction == "down":
        new_pos = (WIDTH // 2, 60)
    elif transition_direction == "left":
        new_pos = (WIDTH - 60, HEIGHT // 2)
    elif transition_direction == "right":
        new_pos = (60, HEIGHT // 2)

    active_piece.pos = new_pos
    print(f"Transição concluída. Nova sala: room_{current_r}_{current_c}. Nova posição do active_piece: {active_piece.pos}")

    # Recria o Actor para garantir que não haja estado residual
    #active_piece.pos = new_pos
    #print(f"Transição concluída. Nova sala: room_{current_r}_{current_c}. Nova posição do active_piece: {active_piece.pos}")

    #active_piece = ActivePiece(new_pos[0], new_pos[1],"pawn")

    print(f"(Force) Transição concluída. Nova sala: room_{current_r}_{current_c}. Nova posição do active_piece: {active_piece.pos}")


# -----------------------------
# Atualiza o estado global no update()
# -----------------------------
def update():
    """
    Função parte do PGZero que é executada constantemente
    """
    global current_room, current_r, current_c, active_piece, transition_active, transition_progress
    global active_piece, active_piece_index, switch_delay


    # Se não estamos em transição, permitimos movimentação e verificamos colisões com portas
    if not transition_active:

        #
        # (Aqui você provavelmente já tem sua lógica de movimentação do active_piece via setas.)
        #

        screen.clear()

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

            #if keyboard.b:
            #    bispo1 = active_pieces[4]
            #    bispo2 = pieces[4]
            #    current_fight = Fight(bispo1, bispo2)

            #if current_fight.active:
            #    current_fight.update()

            active_piece.update_position(speed=3)

            #active_piece.active = True

            # Atualizações das peças ccurrent_fight = Fight(peao,torre)ontroladas
            for piece in active_pieces:
                if piece != active_piece:
                    piece.update_idle()

            # Atualizações automáticas para as peças não controladas
            for piece in pieces:
                piece.update_position(speed=2)
                piece.animate_sprite()



        #
        #
        # Verifica a colisão do active_piece com as portas da sala atual
        for door in current_room.door_actors:
            if active_piece.actor.colliderect(door):
                # A direção já está armazenada em door.direction
                initiate_transition(door.direction)
                break
        #
        #
        #


    else:
        #
        # Atualiza a animação de transição
        #
        transition_progress += transition_speed
        total_distance = HEIGHT if transition_direction in ("up", "down") else WIDTH
        if transition_progress >= total_distance:
            finish_transition()
   
    
# -----------------------------
# GLOBAL FUNCTION: draw()
# Draws all objects on the screen.
# -----------------------------
def draw():
    """
    Desenha e constantemente atualiza tudo na tela
    """
    screen.clear()

    if transition_active:
        # Calcula os deslocamentos para o efeito de slide
        if transition_direction == "up":
            current_offset = (0, transition_progress)
            target_offset = (0, transition_progress - HEIGHT)
        elif transition_direction == "down":
            current_offset = (0, -transition_progress)
            target_offset = (0, HEIGHT - transition_progress)
        elif transition_direction == "left":
            current_offset = (transition_progress, 0)
            target_offset = (transition_progress - WIDTH, 0)
        elif transition_direction == "right":
            current_offset = (-transition_progress, 0)
            target_offset = (WIDTH - transition_progress, 0)
        else:
            current_offset = (0, 0)
            target_offset = (0, 0)

        # Desenha as duas salas com seus respectivos offsets
        current_room.draw(screen, offset=current_offset)
        target_room.draw(screen, offset=target_offset)
    else:

        #
        # transição terminou, desenha a tela normal (mito)
        #

        if menu.active:
            # Desenha o menu
            menu.draw(screen)
        else:
            # Desenha o jogo principal
            current_room.draw(screen)
            
            # Informações na tela
            screen.draw.text(f"Ativo: {active_piece.kind} - TAB muda para outro - ESC para voltar", center=(400, 50), fontsize=30, color="yellow")

            # Desenha as peças ativas
            for piece in active_pieces:
                piece.draw()

            # Desenha as peças não controladas
            for piece in pieces:
                piece.draw()

            # Desenha a luta, se houver
            #if current_fight.active:
            #    current_fight.draw()
            #if config.transition_finishing:
            #    active_piece.pos = config.new_pos
            #    config.transition_finishing=False
            #    print('active_piece.pos=', active_piece.pos)
            #    active_piece.draw()

def on_mouse_down(pos):
    """
    Passa o clique do mouse para o menu, caso ele esteja ativo
    """
    if menu.active:
        menu.on_mouse_down(pos)

def on_key_down(key):
    """
    Pressionar ESC retorna ao menu
    """

    # Se houver transição ativa, ignoramos novos comandos de movimentação
    if transition_active:
        return

    # Tecla ESC - vai pro menu
    if not menu.active and key == keys.ESCAPE:
        menu.active = True  # Retorna ao menu
    elif menu.active and key == keys.ESCAPE:
        menu.active = False  # Sai do menu para o jogo principal

    """
    # Lógica simples para movimentar o active_piece
    move_speed = 10
    if key == keys.UP:
        active_piece.y -= move_speed
    elif key == keys.DOWN:
        active_piece.y += move_speed
    elif key == keys.LEFT:
        active_piece.x -= move_speed
    elif key == keys.RIGHT:
        active_piece.x += move_speed    

    """

pgzrun.go()
