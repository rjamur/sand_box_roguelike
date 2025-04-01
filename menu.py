"""Menu Principal"""
from pygame import Rect

class Button:
    """Botões do Menu"""
    def __init__(self, x, y, width, height, text, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback

    def draw(self, screen):
        """Desenha os botões"""
        rect = Rect((self.x, self.y), (self.width, self.height))
        # O 'screen' será chamado diretamente dentro do método draw()
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

class Menu:
    """Estrutura do Menu, com os botões"""
    def __init__(self, music):
        self.active = True
        self.music_on = True
        self.buttons = []
        self.initialize_buttons()
        self.music = music

        # Toca a música de fundo em loop
        self.music.play('background.wav')  # 'background.ogg' deve estar na pasta 'music/'

    def initialize_buttons(self):
        button_width = 300
        button_height = 50
        start_x = (800 - button_width) // 2
        start_y = 200
        gap = 20

        start_button = Button(start_x, start_y, button_width, button_height,
                              "Começar o jogo", self.start_game)
        music_button = Button(start_x, start_y + button_height + gap, button_width, button_height,
                              "Música e sons: ligados", self.toggle_music)
        exit_button = Button(start_x, start_y + 2 * (button_height + gap), button_width, button_height,
                             "Saída", self.exit_game)

        self.buttons = [start_button, music_button, exit_button]

    def draw(self, screen):
        """Função chamada no draw do main.py do PGZero
            é chamada, portanto, constantemente (60x por segundo)"""
        # 'screen' é utilizado dentro desta função, que será chamada no loop principal
        screen.clear()
        screen.draw.text("Menu Principal", center=(400, 100), fontsize=50, color="yellow")
        for btn in self.buttons:
            btn.draw(screen)

    def update(self):
        pass

    def on_mouse_down(self, pos):
        for btn in self.buttons:
            if btn.is_hovered(pos):
                btn.callback()

    def start_game(self):
        self.active = False

    def toggle_music(self):
        """Liga e desliga a música"""
        self.music_on = not self.music_on
        if self.music_on:
            self.music.unpause()
            self.buttons[1].text = "Música e sons: ligados"
        else:
            self.music.pause()
            self.buttons[1].text = "Música e sons: desligados"

    def exit_game(self):
        """Para a música ao sair do jogo"""
        self.music.stop()
        exit()
