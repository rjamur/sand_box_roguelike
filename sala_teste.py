import pgzrun
from hall_manager import Hall

# Configurações do jogo
WIDTH, HEIGHT = 1280, 800

# Lista de ornamentos disponíveis para muros
wall_ornaments = ["baum_tile"]

# Configura a primeira sala
first_hall = Hall(
    width=16, height=10,  # Tamanho da sala em tiles
    floor_type="grass",
    wall_type="brick",
    doors={"up": True, "down": True, "left": True, "right": True},  # Portas em todos os lados
    wall_ornaments=wall_ornaments
)

first_hall.generate()

def draw():
    screen.clear()
    first_hall.draw(screen)

pgzrun.go()
