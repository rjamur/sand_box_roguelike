import pgzrun
import pygame  # Importa pygame para usar a função de transformação

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Animação do Peão - Walk Up (Escalado 10x)"

# Lista dos nomes das imagens (PGZero carrega automaticamente da pasta "images")
frames = [
    "pawn_up_1",
    "pawn_up_2",
    "pawn_up_3",
    "pawn_up_4",
    "pawn_up_5",
    "pawn_up_6",
    "pawn_up_7"
]

# Fator de escala
SCALE_FACTOR = 5

# Pré-processa e escala todos os frames
# PGZero já carrega as imagens da pasta "images" e as disponibiliza como atributos do objeto "images"
scaled_surfaces = []
for frame_name in frames:
    original_surf = getattr(images, frame_name)  # Obtém a superfície original
    new_width = original_surf.get_width() * SCALE_FACTOR
    new_height = original_surf.get_height() * SCALE_FACTOR
    scaled_surf = pygame.transform.scale(original_surf, (new_width, new_height))
    scaled_surfaces.append(scaled_surf)

# Cria um Actor com o primeiro frame (a string ainda serve para referência, mas iremos sobrepor a superfície)
pawn = Actor(frames[0], center=(WIDTH // 2, HEIGHT // 2))
pawn._surf = scaled_surfaces[0]  # Substitui a superfície do Actor pela versão escalada

# Variável para controlar o frame atual da animação
current_frame = 0

# Define o tempo de exibição de cada frame, em segundos
animation_delay = 0.1

def animate_sprite():
    """Atualiza a superfície do sprite para a próxima frame (em loop)."""
    global current_frame, pawn
    current_frame = (current_frame + 1) % len(scaled_surfaces)
    pawn._surf = scaled_surfaces[current_frame]

# Agenda a função de animação para ser chamada a cada 'animation_delay' segundos
clock.schedule_interval(animate_sprite, animation_delay)

def draw():
    screen.clear()
    pawn.draw()

pgzrun.go()
