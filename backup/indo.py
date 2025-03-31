import pgzrun
import random
import math
from pygame import Rect

# Configurações gerais
WIDTH = 800
HEIGHT = 600
TITLE = "Simple Roguelike"

# Variáveis globais
game_state = "menu"  # 'menu' ou 'game'
music_on = True

# Funções de música
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("background_music")
    else:
        music.stop()

# Menu principal
def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, HEIGHT // 4), fontsize=40, color="white")
    screen.draw.text("1. Start Game", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=30, color="white")
    screen.draw.text("2. Toggle Music", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")
    screen.draw.text("3. Exit", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

# Inicializando música
if music_on:
    music.play("background_music")

class Character:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = Rect(x, y, 32, 32)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))


class Enemy(Character):
    def __init__(self, x, y, sprite, territory):
        super().__init__(x, y, sprite)
        self.territory = territory

    def patrol(self):
        self.x = random.randint(self.territory.left, self.territory.right)
        self.y = random.randint(self.territory.top, self.territory.bottom)


#Lógica principal do jogo
hero = Character(WIDTH // 2, HEIGHT // 2, "hero")
enemies = [
    Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT), "enemy", Rect(100, 100, 200, 200)),
    Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT), "enemy", Rect(500, 100, 200, 200)),
]

def draw_game():
    screen.clear()
    hero.draw()
    for enemy in enemies:
        enemy.draw()

def update_game():
    for enemy in enemies:
        enemy.patrol()
    # Movimento do herói
    if keyboard.left:
        hero.move(-5, 0)
    if keyboard.right:
        hero.move(5, 0)
    if keyboard.up:
        hero.move(0, -5)
    if keyboard.down:
        hero.move(0, 5)

#Navegação entre o menu e o jogo
def on_key_down(key):
    global game_state
    if game_state == "menu":
        if key == keys.K_1:
            game_state = "game"
        elif key == keys.K_2:
            toggle_music()
        elif key == keys.K_3:
            exit()

def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()

def update():
    if game_state == "game":
        update_game()

pgzrun.go()