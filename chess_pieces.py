"""Implementa peças de xadrez que se movimentam"""
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from game_entities import Player
import config

import os

def load_direction_sprites(kind, direction):
    """
    Procura uma subpasta em 'images/<kind>' cujo nome contenha o 'direction'
    (ex.: "left", "right", "up" ou "down") e carrega todos os arquivos .png
    dessa pasta, ordenados alfabeticamente.
    Retorna uma lista de caminhos relativos (ex.: "bishop/bishop_left/00.png").
    """
    # Define o caminho base para a pasta de sprites da peça
    base_dir = os.path.join("images", kind)
    
    if not os.path.exists(base_dir):
        print(f"A pasta base {base_dir} não existe!")
        return []
    
    # Lista todas as subpastas que contenham a string direction (ignorando maiúsculas/minúsculas)
    subdirs = [
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and (direction.lower() in d.lower())
    ]
    print(subdirs)
    
    if not subdirs:
        print(f"Nenhuma subpasta encontrada para a direção '{direction}' em '{kind}'.")
        return []
    
    # Escolhe a primeira subpasta encontrada (ou pode ser feita uma seleção mais sofisticada)
    chosen_subdir = subdirs[0]
    sprites_folder = os.path.join(base_dir, chosen_subdir)
    print(sprites_folder)
    
    # Lista todos os arquivos .png em sprites_folder e ordena-os alfabeticamente
    files = sorted([f for f in os.listdir(sprites_folder) if f.lower().endswith(".png")])
    print(files)
    
    # Monta os caminhos relativos (por exemplo, "bishop/bishop_left/00.png")
    sprite_paths = [os.path.join(kind, chosen_subdir, f) for f in files]
    print(sprite_paths)
    return sprite_paths


class Piece(Player):
    """Classe base para outras classes de peças/personagens"""
    def __init__(self, x, y, kind, initial_direction="down"):
        self.x = x
        self.y = y
        self.kind = kind
        self.current_direction = initial_direction
        self.current_frame = 0
        self.moving = False
        self.active = True

        # 'kind' determina a pasta em images e usamos a função auxiliar para cada direção.
        self.sprites = {}
        for d in ["down", "left", "right", "up"]:
            self.sprites[d] = load_direction_sprites(kind, d)
            if not self.sprites[d]:
                print(f"Atenção: Nenhum sprite encontrado para a direção '{d}' de '{kind}'.")
        
        # Define o sprite inicial; caso não haja sprites para a direção inicial, define como uma string vazia.
        initial_sprite = self.sprites[initial_direction][0] if self.sprites.get(initial_direction) else ""
        self.actor = Actor(initial_sprite, center=(x, y))

        self.actor = Actor(self.sprites[initial_direction][0], center=(x, y))

        # Configura uma sequência idle mais dinâmica – use os 2 últimos frames (por exemplo)
        self.idle_sprites = {
            d: self.sprites[d][-2:] for d in ["down", "left", "right", "up"]
        }
        # Contador e índice para a animação ociosa
        self.idle_counter = 0
        self.idle_frame_index = 0

    def draw(self):
        """
        Desenha a peça no tabuleiro.
            
        Deve ser chamada em draw() do main.py
        Na prática é chamada constantemente para redesenhar a peça

        """
        if self.active:
            self.actor.draw()

    def update_position(self, speed):
        """Método base, implementado pelas subclasses."""
        pass


    def animate_sprite(self):
        """Anima o sprite da peça durante o movimento."""
        if not hasattr(self, "animation_counter"):
            self.animation_counter = 0  # Inicializa contador de frames

        self.animation_counter += 1
        if self.animation_counter % 10 == 0:  # Altere '5' para ajustar a velocidade
            if self.moving:  # Verifica se está se movendo
                self.current_frame = (
                    self.current_frame + 1
                ) % len(self.sprites[self.current_direction])  # Loop nos frames
                self.actor.image = self.sprites[self.current_direction][self.current_frame]

    def update_idle(self):
        """
        Atualiza o sprite para o estado ocioso com animação dinâmica.
        Aqui, o idle alterna entre os sprites definidos em self.idle_sprites.
        Pode simular respiração, piscar ou outro efeito sutil.
        """
        # Incrementa o contador de frames para animação idle
        self.idle_counter += 1
        # Por exemplo, a cada 20 frames o idle troca de sprite
        if self.idle_counter % 20 == 0:
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sprites[self.current_direction])
        # Atualiza a imagem para o frame idle corrente
        self.actor.image = self.idle_sprites[self.current_direction][self.idle_frame_index]     

# As demais classes herdam de Piece e podem ou usar update_idle conforme necessário:
class StaticPiece(Piece):
    """Peça que não se mexe quando está parada"""
    def update_position(self, speed):
        """Peça parada, usa apenas o update_idle para animação ociosa dinâmica."""
        self.moving = False
        self.update_idle()

class ThinkingPiece(Piece):
    """
    Essa peça, quando parada, fica fazendo movimentos
    Pode piscar, mecher a cabeça (uma peça com TDAH)
    """
    def __init__(self, x, y, kind, initial_direction="down"):
        super().__init__(x, y, kind, initial_direction)
        self.turning = False
        self.turn_frame = 0
        self.turn_timer = 3.0
        self.idle_turn = "forward"  # Padrão: "forward" ou "backward"
        self.current_turn_frames = []
        self.next_idle = None

        folder = kind
        self.forward_seq = [
            f"{folder}/{folder}_turn/{i:02d}_{folder}_turn" for i in range(3)
        ]
        self.backward_seq = [
            f"{folder}/{folder}_turn/{i:02d}_{folder}_turn" for i in range(4, 6)
        ]

    def update_turn(self):
        """Atualiza a animação de rotação."""
        if self.turning:
            self.turn_frame += 1
            if self.turn_frame < len(self.current_turn_frames):
                self.actor.image = self.current_turn_frames[self.turn_frame]
            else:
                self.turning = False
                self.turn_timer = 3.0
                self.idle_turn = self.next_idle
                if self.idle_turn == "forward":
                    self.actor.image = self.forward_seq[-1]
                else:
                    self.actor.image = self.backward_seq[-1]

    def automatic_turn(self):
        """Realiza a rotação automaticamente quando inativa."""
        if not self.moving and not self.turning:
            self.turning = True
            self.turn_frame = 0
            if self.idle_turn == "forward":
                self.current_turn_frames = (
                    self.backward_seq[:] if random.choice([True, False]) else list(reversed(self.backward_seq))
                )
                self.next_idle = "backward"
            else:
                self.current_turn_frames = (
                    self.forward_seq[:] if random.choice([True, False]) else list(reversed(self.forward_seq))
                )
                self.next_idle = "forward"
            self.actor.image = self.current_turn_frames[0]

    def check_turn_timer(self):
        """Reduz o tempo e dispara rotação automática."""
        if not self.moving and not self.turning:
            self.turn_timer -= 0.1
            if self.turn_timer <= 0:
                self.automatic_turn()

    def update_position(self, speed):
        """Não atualiza posição, apenas anima rotação."""
        self.check_turn_timer()
        self.update_turn()

    def animate_sprite(self):
        """Animate the walk if moving and not turning."""
        if self.moving and not self.turning:
            self.current_frame = (
                self.current_frame + 1
            ) % len(self.sprites[self.current_direction])
            self.actor.image = self.sprites[self.current_direction][
                self.current_frame
            ]

class MovingPiece(Piece):
    def __init__(self, x, y, kind, initial_direction="down"):
        super().__init__(x, y, kind, initial_direction)
        self.direction = "horizontal"  # Pode ser "horizontal" ou "vertical"
        self.moving_forward = True

    def update_position(self, speed):
        """Atualiza a posição com movimento simples."""
        if self.direction == "horizontal":
            if self.moving_forward:
                self.actor.x += speed
                if self.actor.x > 800:  # Limite da tela (ajustar conforme necessário)
                    self.moving_forward = False
            else:
                self.actor.x -= speed
                if self.actor.x < 0:
                    self.moving_forward = True
        elif self.direction == "vertical":
            if self.moving_forward:
                self.actor.y += speed
                if self.actor.y > 600:
                    self.moving_forward = False
            else:
                self.actor.y -= speed
                if self.actor.y < 0:
                    self.moving_forward = True

class PieceAndante(Piece):
    """Peça que anda de um lado para outro, ou de cima pra baixo"""
    def __init__(self, x, y, kind, initial_direction="left"):
        super().__init__(x, y, kind, initial_direction)
        if initial_direction in ("left", "right"):
            self.direction = "horizontal"  # Pode ser "horizontal" ou "vertical"
        else:
            self.direction = "vertical"
        self.moving_forward = True

    def update_position(self, speed):
        """Atualiza a posição da peça."""
        self.moving = True  # Indica que está em movimento
        if self.direction == "horizontal":
            if self.moving_forward:
                self.actor.x += speed
                self.current_direction = "right"   # Atualiza para 'right' se movendo para a direita
                if self.actor.x > 800:  # Limite à direita
                    self.moving_forward = False
            else:
                self.actor.x -= speed
                self.current_direction = "left"    # Atualiza para 'left' se movendo para a esquerda
                if self.actor.x < 0:  # Limite à esquerda
                    self.moving_forward = True
        elif self.direction == "vertical":
            if self.moving_forward:
                self.actor.y += speed
                self.current_direction = "down"   # Atualiza para 'down' se movendo para baixo
                if self.actor.y > 600:  # Limite inferior
                    self.moving_forward = False
            else:
                self.actor.y -= speed
                self.current_direction = "up"     # Atualiza para 'up' se movendo para cima
                if self.actor.y < 0:  # Limite superior
                    self.moving_forward = True

        if self.moving:
            self.animate_sprite()

class ActivePiece(Piece):
    """
    Peças/personagens ativos, isto é, que são movimentados pelo teclado
    """
    def update_position(self, speed):
        """Controla a posição com base nas teclas pressionadas."""
        self.moving = False
        if keyboard.left:
            self.current_direction = "left"
            self.actor.x = max(64, self.actor.x - speed)
            self.moving = True
        elif keyboard.right:
            self.current_direction = "right"
            self.actor.x += speed
            self.moving = True
        elif keyboard.up:
            self.current_direction = "up"
            self.actor.y -= speed
            self.moving = True
        elif keyboard.down:
            self.current_direction = "down"
            self.actor.y += speed
            self.moving = True

        if self.moving:
            self.animate_sprite()
        else:
            self.update_idle()

# Outras classes, como ThinkingPiece, MovingPiece e PieceAndante, podem manter ou sobrescrever se necessário.            