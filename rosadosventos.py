import pgzrun

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Movimentação e Animação do Peão"

# Criação do dicionário com os nomes dos frames para cada direção
# Usamos f-strings para montar os nomes conforme o padrão "XX_pawn_direction"
sprites = {}
directions = ["down", "left", "right", "up"]
for direction in directions:
    frame_list = []
    for i in range(7):  # 0 a 6
        frame_list.append(f"pawn/pawn_{direction}/{i:02d}_pawn_{direction}")
    sprites[direction] = frame_list

# Variáveis globais para controle da animação
current_direction = "down"
current_frame = 0
moving = False

# Cria o ator com o frame inicial (posição central na tela)
pawn = Actor(sprites[current_direction][0], center=(WIDTH // 2, HEIGHT // 2))

# Função de atualização do movimento
def update():
    global current_direction, moving, current_frame, pawn
    speed = 3
    moving = False  # reinicia o flag de movimentação a cada frame

    # Verifica as teclas de direção (prioridade: esquerda > direita > cima > baixo)
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

    # Se o personagem não estiver se movendo, reseta para o frame 0 (sprite parado)
    if not moving:
        current_frame = 0
        pawn.image = sprites[current_direction][0]

# Função para atualizar a animação periodicamente
def animate_sprite():
    global current_frame, pawn
    if moving:  # Só avança a animação se o personagem estiver em movimento
        # Atualiza o frame de animação (ciclo com 7 frames)
        current_frame = (current_frame + 1) % len(sprites[current_direction])
        pawn.image = sprites[current_direction][current_frame]

# Agenda a atualização da animação a cada 0.1 segundo
clock.schedule_interval(animate_sprite, 0.1)

# Função de renderização
def draw():
    screen.clear()
    pawn.draw()

pgzrun.go()
