import pgzrun
import random

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Movimentação e Animação do Peão - Turn Automático e Random"

# === ANIMAÇÃO DE WALK (movimento) ===
# Para cada direção, os 7 frames estão em:
# images/pawn/pawn_down, pawn_left, pawn_right, pawn_up
sprites = {}
directions = ["down", "left", "right", "up"]
for direction in directions:
    # Cada lista contém os 7 frames, com nomes no padrão: 00_pawn_direction.png ... 06_pawn_direction.png
    sprites[direction] = [f"pawn/pawn_{direction}/{i:02d}_pawn_{direction}" for i in range(7)]

# === ANIMAÇÃO DE TURN ===
# Dois conjuntos:
#  "forward": frames 00 a 11 (normal: inicia em 00 e termina em 11 => olhando para frente)
#  "backward": frames 12 a 23 (normal: inicia em 12 e termina em 23 => olhando para trás)
turn_forward = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12)]
turn_backward = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12, 24)]

# Variáveis globais de controle:
current_direction = "down"   # direção para o walk
current_frame = 0            # frame atual do walk
moving = False               # flag: está se movendo?

# Variáveis de turn (virada)
turning = False              # flag: está executando a animação de turn?
turn_frame = 0               # índice do frame atual na animação de turn
turn_timer = 3               # tempo de inatividade para iniciar o automatic turn (em segundos)

# Variáveis para controlar a alternância do turn:
last_turn_type = None        # "forward" ou "backward" – último modo utilizado
current_turn_type = None     # modo (forward/backward) escolhido para o turn atual
current_turn_frames = None   # lista de frames escolhida para o turn atual

# Cria o ator com o sprite inicial da direção "down",
# posicionado no centro da tela.
pawn = Actor(sprites[current_direction][0], center=(WIDTH // 2, HEIGHT // 2))

# ---------------------------------------------------------------------------- #
# Função de animação de walk (movimento) – se estiver se movendo e não estiver turnando.
def animate_sprite():
    global current_frame, pawn
    if moving and not turning:
        current_frame = (current_frame + 1) % len(sprites[current_direction])
        pawn.image = sprites[current_direction][current_frame]

# ---------------------------------------------------------------------------- #
# Função que atualiza a animação de turn (quando estiver sendo executada).
def update_turn():
    global turning, turn_frame, pawn, turn_timer, last_turn_type, current_turn_frames, current_turn_type
    if turning:
        turn_frame += 1
        if turn_frame < len(current_turn_frames):
            pawn.image = current_turn_frames[turn_frame]
        else:
            # Turn finalizado – atualiza o último tipo
            last_turn_type = current_turn_type
            # Fim do turn; reinicia variáveis
            turning = False
            turn_frame = 0
            turn_timer = 3
            # Depois, mostra o frame "parado" de walk na direção atual.
            pawn.image = sprites[current_direction][0]

# ---------------------------------------------------------------------------- #
# Função que inicia o turn automaticamente, quando o personagem estiver parado.
def automatic_turn():
    global turning, turn_frame, current_turn_frames, current_turn_type, last_turn_type
    if not moving and not turning:
        turning = True
        turn_frame = 0
        # Decide o modo de turn: se last_turn_type == "forward", desta vez usará "backward",
        # senão, usará "forward". Se for a primeira vez, escolhe aleatoriamente.
        if last_turn_type is None:
            current_turn_type = random.choice(["forward", "backward"])
        else:
            current_turn_type = "backward" if last_turn_type == "forward" else "forward"
        # Seleciona os frames de acordo com o tipo
        if current_turn_type == "forward":
            frames_list = turn_forward[:]  # copia
        else:
            frames_list = turn_backward[:]
        # Randomicamente escolher se vai reproduzir em ordem ascendente ou descendente.
        if random.choice([True, False]):
            # Ordem ascendente (mantém)
            current_turn_frames = frames_list
        else:
            # Ordem descendente: porém, queremos que o frame final seja o mesmo que o normal.
            # Por exemplo, se for forward, normalmente termina em 11; se invertido, o primeiro elemento é 11.
            # Então, usamos a lista invertida.
            current_turn_frames = list(reversed(frames_list))
        # Define o sprite inicial do turn.
        pawn.image = current_turn_frames[0]

# ---------------------------------------------------------------------------- #
# Função que checa o timer para iniciar o turn automático.
def check_turn_timer():
    global turn_timer
    if not moving and not turning:
        turn_timer -= 0.1
        if turn_timer <= 0:
            automatic_turn()

# ---------------------------------------------------------------------------- #
# Função update: processa o input do teclado e atualiza a posição.
def update():
    global current_direction, moving, pawn, turn_timer, current_frame, turning
    speed = 3
    moving = False  # reinicia estado de movimento

    # Se não estiver no meio do turn, processa as setas:
    if not turning:
        if keyboard.left:
            current_direction = "left"
            pawn.x -= speed
            moving = True
        elif keyboard.right:
            current_direction = "right"
            pawn.x += speed
            moving = True
        elif keyboard.up:
            current_direction = "up"
            pawn.y -= speed
            moving = True
        elif keyboard.down:
            current_direction = "down"
            pawn.y += speed
            moving = True

    # Se estiver se movendo, reseta o turn_timer (caso esteja parado anteriormente)
    if moving:
        turn_timer = 3

    # Se estiver parado e não turnando, garante o sprite parado da direção atual.
    if not moving and not turning:
        current_frame = 0
        pawn.image = sprites[current_direction][0]

# ---------------------------------------------------------------------------- #
# Função draw: desenha o ator na tela.
def draw():
    screen.clear()
    pawn.draw()

# ---------------------------------------------------------------------------- #
# Agenda as funções de animação/checagem:
clock.schedule_interval(animate_sprite, 0.1)   # anima walk
clock.schedule_interval(update_turn, 0.1)      # atualiza turn (se ativo)
clock.schedule_interval(check_turn_timer, 0.1)   # checa o timer para turn automático

pgzrun.go()
