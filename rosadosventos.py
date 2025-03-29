import pgzrun
import random

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Movimentação e Animação do Peão - Turn Automático"

# Monta as listas de sprites para a animação de caminhada (walk)
sprites = {}
directions = ["down", "left", "right", "up"]
for direction in directions:
    # Cada lista contém os 7 frames para a direção: 00 até 06.
    sprites[direction] = [f"pawn/pawn_{direction}/{i:02d}_pawn_{direction}" for i in range(7)]

# Monta os frames para a animação de turn:
# turn_forward usa os sprites 00 até 11 e turn_backward usa os sprites 12 até 23.
turn_forward = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12)]
turn_backward = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12, 24)]

# Variáveis de controle
current_direction = "down"  # direção atual do movimento (para walk)
current_frame = 0           # frame atual para a animação de walk
moving = False              # flag: está se movendo?
turning = False             # flag: está realizando a animação de turn?
turn_frame = 0              # frame atual da animação de turn
turn_timer = 3              # tempo (em segundos) de inatividade para iniciar o turn automático

current_turn_frames = None  # guarda a sequência de sprites escolhida para o turn

# Cria o ator (actor) com o primeiro sprite de caminhada na direção "down",
# posicionado no centro da tela.
pawn = Actor(sprites[current_direction][0], center=(WIDTH // 2, HEIGHT // 2))

#
# Função para atualizar a animação de "walk" (movimento):
#
def animate_sprite():
    global current_frame, pawn
    # Se o personagem estiver se movendo e NÃO estiver virando
    if moving and not turning:
        current_frame = (current_frame + 1) % len(sprites[current_direction])
        pawn.image = sprites[current_direction][current_frame]

#
# Função para atualizar a animação de "turn" (virada) enquanto ela estiver ativa.
#
def update_turn():
    global turning, turn_frame, pawn, turn_timer, current_turn_frames
    if turning:
        turn_frame += 1
        if turn_frame < len(current_turn_frames):
            pawn.image = current_turn_frames[turn_frame]
        else:
            # Terminou o turn; reseta variáveis
            turning = False
            turn_frame = 0
            turn_timer = 3  # reinicia o timer
            # Depois de virar, o personagem volta à animação parado (frame 0 da walk)
            pawn.image = sprites[current_direction][0]

#
# Função que checa o timer para o turn automático.
# Quando o personagem está parado (não moving e não turning), diminui o timer; se zerar, inicia o turn.
#
def check_turn_timer():
    global turn_timer
    if not moving and not turning:
        turn_timer -= 0.1
        if turn_timer <= 0:
            automatic_turn()

#
# Função que inicia a animação de turn automaticamente.
#
def automatic_turn():
    global turning, turn_frame, current_turn_frames, turn_timer
    # Apenas inicia se o personagem estiver parado e não estiver já virando.
    if not moving and not turning:
        turning = True
        turn_frame = 0
        # Escolhe aleatoriamente entre virada para frente e para trás.
        current_turn_frames = random.choice([turn_forward, turn_backward])
        pawn.image = current_turn_frames[0]

#
# Função update: processa input do teclado e movimentação.
#
def update():
    global current_direction, moving, turning, pawn, turn_timer, current_frame
    speed = 3
    moving = False  # Reinicia o estado de movimento

    # Se não estivermos virando, processa as teclas direcionais.
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

    # Se o personagem está se movendo, reseta o timer para o turn
    if moving:
        turn_timer = 3

    # Se estiver parado e não virando, garante que o frame exibido seja o inicial da direção.
    if not moving and not turning:
        current_frame = 0
        pawn.image = sprites[current_direction][0]

#
# Função draw: desenha o ator na tela.
#
def draw():
    screen.clear()
    pawn.draw()

#
# Agenda as funções (são chamadas automaticamente a cada 0.1 segundo)
#
clock.schedule_interval(animate_sprite, 0.1)   # Anima o walk se estiver se movendo
clock.schedule_interval(update_turn, 0.1)      # Atualiza a animação de turn (se ativa)
clock.schedule_interval(check_turn_timer, 0.1)   # Checa o timer de turn automático

pgzrun.go()
