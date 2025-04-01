import random

class MapGenerator:
    def __init__(self, size=20, num_rooms=5):
        self.size = size  # Tamanho do mapa
        self.num_rooms = num_rooms  # Número de salas no mapa
        self.map = [['.' for _ in range(size)] for _ in range(size)]  # Inicializa o mapa vazio
        self.rooms = []  # Lista de salas criadas

    def generate_rooms(self):
        # Cria salas no mapa
        for _ in range(self.num_rooms):
            while True:
                x = random.randint(0, self.size - 6)
                y = random.randint(0, self.size - 6)
                room = self.create_room(x, y)
                if room:
                    break
        return self.rooms

    def create_room(self, x, y):
        # Cria uma sala na posição x, y (com tamanho fixo 5x5 para simplificar)
        width, height = 5, 5
        if self._room_fits(x, y, width, height):
            for i in range(y, y + height):
                for j in range(x, x + width):
                    self.map[i][j] = 'S'
            # Adiciona a sala com sua posição e portas
            room = {"x": x, "y": y, "width": width, "height": height}
            room["doors"] = {
                "north": (x + width // 2, y - 1),
                "south": (x + width // 2, y + height),
                "west": (x - 1, y + height // 2),
                "east": (x + width, y + height // 2)
            }
            self.rooms.append(room)
            return room
        return None

    def _room_fits(self, x, y, width, height):
        # Verifica se a sala cabe no mapa sem sobreposição
        if x < 0 or y < 0 or x + width > self.size or y + height > self.size:
            return False
        for i in range(y, y + height):
            for j in range(x, x + width):
                if self.map[i][j] != '.':
                    return False
        return True

    def create_corridor(self, start, end):
        # Cria um corredor entre duas posições (start e end)
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            # Corredor vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map[y][x1] = 'C'
        elif y1 == y2:
            # Corredor horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map[y1][x] = 'C'
        else:
            # Corredor em L (primeiro vertical, depois horizontal)
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map[y][x1] = 'C'
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map[y2][x] = 'C'

    def connect_rooms(self):
        # Conecta salas com corredores
        for i in range(len(self.rooms) - 1):
            start = self.rooms[i]["doors"]["south"]  # Porta sul da sala atual
            end = self.rooms[i + 1]["doors"]["north"]  # Porta norte da próxima sala
            self.create_corridor(start, end)

    def enhance_dead_ends(self):
        # Adiciona interatividade aos becos sem saída
        for room in self.rooms:
            for direction, door in room["doors"].items():
                if self.map[door[1]][door[0]] == 'C' and random.choice([True, False]):
                    if random.choice([True, False]):
                        self.map[door[1]][door[0]] = 'T'  # Tesouro
                    else:
                        self.map[door[1]][door[0]] = 'X'  # Armadilha

    def display_map(self):
        # Exibe o mapa no console
        for row in self.map:
            print(' '.join(row))

# Exemplo de uso:
generator = MapGenerator(size=20, num_rooms=8)
generator.generate_rooms()
generator.connect_rooms()
generator.enhance_dead_ends()
generator.display_map()
