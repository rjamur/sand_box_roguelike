import pgzrun

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Movimentação e Animação do Peão - Turn e Walk"

# Criação do dicionário com os nomes dos frames de animação das direções
sprites = {}
directions = ["down", "left", "right", "up"]
for direction in directions:
    sprites[direction] = [f"pawn/pawn_{direction}/{i:02d}_pawn_{direction}" for i in range(7)]

# Frames da animação "turn"
turn_sprites = [f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(24)]

# Variáveis globais
current_direction = "down"
current_frame = 0
moving = False
turning = False  # Flag para controlar se a animação "turn" está em execução
turn_frame = 0  # Frame atual da animação "turn"

# Criação do ator com o primeiro frame inicial (posição central na tela)
pawn = Actor(sprites[current_direction][0], center=(WIDTH // 2, HEIGHT // 2))

# Função para atualizar a animação "walk"
def animate_sprite():
    global current_frame, pawn
    if moving and not turning:  # Apenas animação de movimento se não estiver virando
        current_frame = (current_frame + 1) % len(sprites[current_direction])
        pawn.image = sprites[current_direction][current_frame]

# Função para animar "turn"
def animate_turn():
    global turning, turn_frame, pawn
    if turning:
        turn_frame += 1
        if turn_frame < len(turn_sprites):  # Continua enquanto houver frames
            pawn.image = turn_sprites[turn_frame]
        else:
            turning = False  # Termina a animação "turn"
            turn_frame = 0

# Agenda a atualização da animação de movimento e turn
clock.schedule_interval(animate_sprite, 0.1)
clock.schedule_interval(animate_turn, 0.1)

# Função para atualizar o estado do jogo
def update():
    global current_direction, moving, pawn, turning
    speed = 3
    moving = False  # Reinicia o estado de movimentação

    # Controle de movimento (ignora se estiver virando)
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

    # Controle da tecla "t" para iniciar a animação "turn"
    if keyboard.t and not turning:
        turning = True
        turn_frame = 0
        pawn.image = turn_sprites[0]  # Define o primeiro frame da animação "turn"

    # Reseta o frame de movimento se parado
    if not moving and not turning:
        current_frame = 0
        pawn.image = sprites[current_direction][0]

# Função de renderização
def draw():
    screen.clear()
    pawn.draw()

pgzrun.go()
