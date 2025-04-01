import random
from pgzero.actor import Actor

class Hall:
    def __init__(self, width, height, floor_type, wall_type, doors, wall_ornaments):
        self.width = width  # Quantidade de tiles horizontalmente
        self.height = height  # Quantidade de tiles verticalmente
        self.floor_type = floor_type  # Tipo de chão (ex.: 'grass', 'chess')
        self.wall_type = wall_type  # Tipo de muro (ex.: 'brick', 'rock')
        self.doors = doors  # Dicionário com as portas (lados: cima, baixo, esquerda, direita)
        self.wall_ornaments = wall_ornaments  # Lista de ornamentos possíveis
        self.tiles = []  # Lista de tiles do chão
        self.walls = []  # Lista de tiles dos muros
        self.door_actors = []  # Objetos `Actor` para portas
        self.ornaments = []  # Lista de ornamentos aleatórios

    def generate(self):
        # Gera os tiles do chão
        for y in range(self.height):
            for x in range(self.width):
                position = (x * 64, y * 64)  # 64x64 pixels por tile
                self.tiles.append({"image": f"map/floors/{self.floor_type}.png", "position": position})

        # Gera os muros com portas no centro
        self._generate_walls()

        # Adiciona ornamentos nas paredes, evitando as portas
        self._generate_wall_ornaments()

    def _generate_walls(self):
        center_x = self.width // 2  # Centro horizontal
        center_y = self.height // 2  # Centro vertical

        for y in range(self.height):
            for x in range(self.width):
                # Paredes superiores e inferiores
                if y == 0 or y == self.height - 1:
                    self.walls.append({"image": f"map/walls/{self.wall_type}.png", "position": (x * 64, y * 64)})
                    if y == 0 and x == center_x and "up" in self.doors:
                        self._add_door("door_up", (x * 64 + 32, y * 64 + 32))
                    elif y == self.height - 1 and x == center_x and "down" in self.doors:
                        self._add_door("door_down", (x * 64 + 32, y * 64 + 32))

                # Paredes laterais
                if x == 0 or x == self.width - 1:
                    self.walls.append({"image": f"map/walls/{self.wall_type}.png", "position": (x * 64, y * 64)})
                    if x == 0 and y == center_y and "left" in self.doors:
                        self._add_door("door_left", (x * 64 + 32, y * 64 + 32))
                    elif x == self.width - 1 and y == center_y and "right" in self.doors:
                        self._add_door("door_right", (x * 64 + 32, y * 64 + 32))

    def _add_door(self, door_type, position):
        # Adiciona uma porta como um `Actor` para interatividade
        door = Actor(f"map/doors/{door_type}.png", position)
        # Altera o ponto de ancoragem
        door.anchor = ('left', 'top')
        self.door_actors.append(door)

    def _generate_wall_ornaments(self):
        for wall in self.walls:
            # Adiciona ornamentos aleatórios nas paredes (evita sobreposição com portas)
            if random.choice([True, False]):  # Chance de 50% de adicionar um ornamento
                x, y = wall["position"]
                if not any(door.x == x and door.y == y for door in self.door_actors):
                    ornament_type = random.choice(self.wall_ornaments)
                    self.ornaments.append({"image": f"map/wall_ornaments/{ornament_type}.png", "position": (x, y)})

    def draw(self, screen):
        # Desenha o chão
        for tile in self.tiles:
            screen.blit(tile["image"], tile["position"])

        # Desenha as paredes
        for wall in self.walls:
            screen.blit(wall["image"], wall["position"])

        # Desenha os ornamentos
        for ornament in self.ornaments:
            screen.blit(ornament["image"], ornament["position"])

        # Desenha as portas
        for door in self.door_actors:
            door.draw()
