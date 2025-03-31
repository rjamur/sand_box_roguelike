#!/usr/bin/python
import pgzrun
import random

# -----------------------------
# CONFIGURAÇÃO DA JANELA
# -----------------------------
WIDTH = 800
HEIGHT = 600
TITLE = "Turn Automático Alternado"

# -----------------------------
# ANIMAÇÃO DE WALK
# (Pastas: images/pawn/pawn_down, pawn_left, pawn_right, pawn_up)
# Cada uma com 7 frames (00 a 06)
# -----------------------------
sprites = {}
directions = ["down", "left", "right", "up"]
for d in directions:
    sprites[d] = [f"pawn/pawn_{d}/{i:02d}_pawn_{d}" for i in range(7)]

# -----------------------------
# ANIMAÇÃO DE TURN
# (Pasta: images/pawn/pawn_turn)
# Conjunto forward: frames 00 a 11 (idle ideal: frame 11)
# Conjunto backward: frames 12 a 23 (idle ideal: frame 23)
# -----------------------------
forward_seq = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(0, 12)]
backward_seq = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12, 24)]

# Variáveis de controle do walk:
current_direction = "down"
current_frame = 0
moving = False

# Variáveis de controle do turn:
turning = False     # True enquanto a animação turn estiver ativa
turn_frame = 0      # índice atual na sequência de turn
turn_timer = 3      # tempo de inatividade (em s) para disparar o turn automático

# Orientação idle atual:
# "forward" significa que, idle, o personagem usa o forward_seq (idle = frame 11)
# "backward" significa idle = frame 23
idle_turn = "forward"  
# Durante a animação, usaremos current_turn_frames e armazenaremos em next_idle o novo estado
current_turn_frames = []
next_idle = None

# Cria o ator com o sprite inicial do walk da direção "down"
pawn = Actor(sprites[current_direction][0], center=(WIDTH // 2, HEIGHT // 2))

# -----------------------------
# FUNÇÃO: animação do walk (quando se move)
# -----------------------------
def animate_sprite():
    global current_frame, pawn
    if moving and not turning:
        current_frame = (current_frame + 1) % len(sprites[current_direction])
        pawn.image = sprites[current_direction][current_frame]

# -----------------------------
# FUNÇÃO: atualiza o turn (avança a sequência de turn)
# -----------------------------
def update_turn():
    global turning, turn_frame, pawn, turn_timer, idle_turn, current_turn_frames, next_idle
    if turning:
        turn_frame += 1
        if turn_frame < len(current_turn_frames):
            pawn.image = current_turn_frames[turn_frame]
        else:
            # O turn terminou; atualiza o estado idle com base na escolha
            turning = False
            turn_frame = 0
            turn_timer = 3
            idle_turn = next_idle
            # Define o sprite idle conforme o novo estado:
            if idle_turn == "forward":
                pawn.image = forward_seq[-1]  # último frame (frame 11)
            else:
                pawn.image = backward_seq[-1] # último frame (frame 23)

# -----------------------------
# FUNÇÃO: dispara o turn automático
# -----------------------------
def automatic_turn():
    global turning, turn_frame, current_turn_frames, idle_turn, next_idle, pawn
    if not moving and not turning:
        turning = True
        turn_frame = 0
        # Se o estado atual idle for "forward", queremos mudar para "backward"
        if idle_turn == "forward":
            # Escolhe aleatoriamente ordem ascendente ou descendente para os backward:
            if random.choice([True, False]):
                current_turn_frames = backward_seq[:]       # ordem ascendente: 12, 13, ..., 23
            else:
                current_turn_frames = list(reversed(backward_seq))  # ordem descendente: 23, 22, ..., 12
            next_idle = "backward"
        else:
            # idle_turn == "backward": queremos mudar para "forward"
            if random.choice([True, False]):
                current_turn_frames = forward_seq[:]        # 0, 1, ..., 11
            else:
                current_turn_frames = list(reversed(forward_seq))   # 11, 10, ..., 0
            next_idle = "forward"
        pawn.image = current_turn_frames[0]

# -----------------------------
# FUNÇÃO: checa o timer para turn automático
# -----------------------------
def check_turn_timer():
    global turn_timer
    if not moving and not turning:
        turn_timer -= 0.1
        if turn_timer <= 0:
            automatic_turn()

# -----------------------------
# FUNÇÃO update(): processa o input e movimentação
# -----------------------------
def update():
    global current_direction, moving, pawn, turn_timer, current_frame, turning
    speed = 3
    moving = False
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
    # Se houver movimento, reinicia o timer do turn
    if moving:
        turn_timer = 3
    # Se estiver parado e não turnando, mostra o sprite idle de walk.
    if not moving and not turning:
        # Aqui escolhemos o idle conforme o estado atual
        if idle_turn == "forward":
            pawn.image = forward_seq[-1]  # frame 11
        else:
            pawn.image = backward_seq[-1] # frame 23

# -----------------------------
# FUNÇÃO draw(): desenha o ator na tela
# -----------------------------
def draw():
    screen.clear()
    pawn.draw()

# -----------------------------
# Agenda as funções com clock.schedule_interval
# -----------------------------
clock.schedule_interval(animate_sprite, 0.1)   # anima o walk
clock.schedule_interval(update_turn, 0.1)      # atualiza o turn se estiver ativo
clock.schedule_interval(check_turn_timer, 0.1)   # verifica o timer para iniciar o turn

pgzrun.go()
