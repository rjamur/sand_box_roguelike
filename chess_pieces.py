import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from game_entities import Player

class Piece(Player):
    def __init__(self, x, y, kind, initial_direction="down"):
        self.x = x
        self.y = y
        self.kind = kind
        self.current_direction = initial_direction
        self.current_frame = 0
        self.moving = False
        self.active = True

        folder = kind
        self.sprites = {
            d: [f"{folder}/{folder}_{d}/{i:02d}_{folder}_{d}" for i in range(7)]
            for d in ["down", "left", "right", "up"]
        }
        print(self.sprites)
        self.actor = Actor(self.sprites[initial_direction][0], center=(x, y))

    def draw(self):
        """Desenha a peça no tabuleiro."""
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
        """Atualiza o sprite para o estado ocioso."""
        idle_frame = self.sprites[self.current_direction][-1]  # Último frame da direção
        self.actor.image = idle_frame


class StaticPiece(Piece):
    def update_position(self, speed):
        """Peça parada, não atualiza posição nem animação."""
        pass

class ThinkingPiece(Piece):
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
    def __init__(self, x, y, kind, initial_direction="left"):
        super().__init__(x, y, kind, initial_direction)
        self.direction = "horizontal"  # Pode ser "horizontal" ou "vertical"
        self.moving_forward = True

    def update_position(self, speed):
        """Atualiza a posição da peça."""
        self.moving = True  # Indica que está em movimento
        if self.direction == "horizontal":
            if self.moving_forward:
                self.actor.x += speed
                if self.actor.x > 800:  # Limite à direita
                    self.moving_forward = False
            else:
                self.actor.x -= speed
                if self.actor.x < 0:  # Limite à esquerda
                    self.moving_forward = True
        elif self.direction == "vertical":
            if self.moving_forward:
                self.actor.y += speed
                if self.actor.y > 600:  # Limite inferior
                    self.moving_forward = False
            else:
                self.actor.y -= speed
                if self.actor.y < 0:  # Limite superior
                    self.moving_forward = True

        if self.moving:
            self.animate_sprite()

class ActivePiece(Piece):
    def update_position(self, speed):
        """Controla a posição com base nas teclas pressionadas."""
        self.moving = False
        if keyboard.left:
            self.current_direction = "left"
            self.actor.x -= speed
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