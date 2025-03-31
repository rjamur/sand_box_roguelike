# menu.py
import pgzrun  # Apenas se você usar funções do pgzero, mas normalmente o main já inicia o pgzrun.
from pygame import Rect
from pgzero.keyboard import keys  # Se for necessário em callbacks
# Obs.: No pgzero o ambiente já fornece a variável "screen" global.

# Classe para representar um botão
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback

    def draw(self):
        rect = Rect((self.x, self.y), (self.width, self.height))
        # Desenha um retângulo com borda e texto centralizado
        screen.draw.filled_rect(rect, "darkblue")
        screen.draw.rect(rect, "white")
        screen.draw.text(
            self.text,
            center=rect.center,
            fontsize=24,
            color="white"
        )

    def is_hovered(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)


# Classe Menu que gerencia o menu principal
class Menu:
    def __init__(self):
        self.active = True  # Menu ativo enquanto True; quando falso, o jogo entra.
        self.music_on = True  # Estado da música
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        # Define as posições e dimensões dos botões
        button_width = 300
        button_height = 50
        start_x = (800 - button_width) // 2  # Largura da tela: 800 (ajuste conforme sua janela)
        start_y = 200
        gap = 20

        # Cria os botões e associa suas callbacks
        start_button = Button(start_x, start_y, button_width, button_height,
                              "Começar o jogo", self.start_game)
        music_button = Button(start_x, start_y + button_height + gap, button_width, button_height,
                              "Música e sons: ligados", self.toggle_music)
        exit_button = Button(start_x, start_y + 2 * (button_height + gap), button_width, button_height,
                             "Saída", self.exit_game)

        self.buttons = [start_button, music_button, exit_button]

    def draw(self):
        screen.clear()
        screen.draw.text("Menu Principal", center=(400, 100), fontsize=50, color="yellow")
        for btn in self.buttons:
            btn.draw()

    def update(self):
        # Se necessário, você pode adicionar atualizações ao menu aqui
        pass

    def on_mouse_down(self, pos):
        for btn in self.buttons:
            if btn.is_hovered(pos):
                btn.callback()

    # Callbacks dos botões
    def start_game(self):
        self.active = False  # Quando o jogo iniciar, o menu é desativado

    def toggle_music(self):
        self.music_on = not self.music_on
        # Atualiza o texto do botão de música. Estamos assumindo que ele é o segundo da lista.
        if self.music_on:
            self.buttons[1].text = "Música e sons: ligados"
        else:
            self.buttons[1].text = "Música e sons: desligados"

    def exit_game(self):
        exit()
