import random
from hall_manager import Hall

class MapManager:
    def __init__(self, grid_rows=4, grid_cols=4):
        """
        Parâmetros:
          grid_rows, grid_cols: quantidade de salas na vertical e horizontal (a grade completa do labirinto).
          
        Todas as salas terão as mesmas dimensões (tamanho da tela do jogo) e as portas estarão centralizadas.
        """
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        # Inicializa uma grade com configuração padrão para as portas.
        self.door_grid = [
            [{"up": False, "down": False, "left": False, "right": False} for _ in range(grid_cols)]
            for _ in range(grid_rows)
        ]

    def generate_rooms(self):
        """
        Gera a configuração de portas para cada sala na grade.
        - As portas 'up' e 'left' são herdadas dos vizinhos.
        - As portas 'right' e 'down' são decididas aleatoriamente (desde que exista sala adjacente).
        - Garante que toda sala possua pelo menos uma porta, forçando uma escolha se necessário.
        """
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                # Herda a porta "up", se houver sala acima.
                if r > 0:
                    self.door_grid[r][c]["up"] = self.door_grid[r - 1][c]["down"]
                # Herda a porta "left", se houver sala à esquerda.
                if c > 0:
                    self.door_grid[r][c]["left"] = self.door_grid[r][c - 1]["right"]

                # Define porta "right" aleatoriamente se houver sala à direita.
                if c < self.grid_cols - 1:
                    self.door_grid[r][c]["right"] = random.choice([True, False])
                else:
                    self.door_grid[r][c]["right"] = False

                # Define porta "down" aleatoriamente se houver sala abaixo.
                if r < self.grid_rows - 1:
                    self.door_grid[r][c]["down"] = random.choice([True, False])
                else:
                    self.door_grid[r][c]["down"] = False

                # Garante que a sala tenha pelo menos uma porta.
                if not any(self.door_grid[r][c].values()):
                    possible = []
                    if r > 0:
                        possible.append("up")
                    if r < self.grid_rows - 1:
                        possible.append("down")
                    if c > 0:
                        possible.append("left")
                    if c < self.grid_cols - 1:
                        possible.append("right")
                    if possible:
                        forced = random.choice(possible)
                        self.door_grid[r][c][forced] = True
                        # Atualiza o vizinho se a porta for herdada.
                        if forced == "up" and r > 0:
                            self.door_grid[r - 1][c]["down"] = True
                        if forced == "left" and c > 0:
                            self.door_grid[r][c - 1]["right"] = True

    def build_halls(self):
        """
        Gera e retorna um dicionário de salas (instâncias de Hall) com chave "room_r_c" para cada sala.
        Cada sala é construída com os parâmetros fixos (dimensões, configurações de portas, piso, muro e ornamentos).
        """
        self.generate_rooms()
        halls = {}
        floor_types = ["chess", "clay", "grass", "marble", "musg"]
        wall_types = ["brick", "rock"]

        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                doors = self.door_grid[r][c]
                hall = Hall(
                    width=20,    # 16 tiles horizontais
                    height=11,   # 12 tiles verticais
                    floor_type=random.choice(floor_types),
                    wall_type=random.choice(wall_types),
                    doors=doors,
                    wall_ornaments=["baum_tile"],
                    hall_type="room"
                )
                hall.generate()
                key = f"room_{r}_{c}"
                halls[key] = hall

        return halls
