import random
from pgzero.actor import Actor

class Hall:
    def __init__(self, width, height, floor_type, wall_type, doors, wall_ornaments, hall_type="room"):
        """
        Parâmetros:
          width, height: dimensões da sala (em número de tiles). Todas as salas terão o mesmo tamanho, ou seja, o tamanho da tela.
          floor_type: nome do arquivo (sem extensão) para o piso (imagem em images/map/floors).
          wall_type: nome do arquivo (sem extensão) para o muro (imagem em images/map/walls).
          doors: dicionário com as direções em que há porta (ex.: {"up": True, "down": False, ...}).
          wall_ornaments: lista com nomes de ornamentos (ex.: ["baum_tile"]).
          hall_type: para este projeto, sempre "room".
        """
        self.width = width
        self.height = height
        self.floor_type = floor_type
        self.wall_type = wall_type
        self.doors = doors
        self.wall_ornaments = wall_ornaments
        self.hall_type = hall_type

        self.tiles = []         # Lista dos tiles do piso
        self.walls = []         # Lista dos tiles dos muros
        self.door_actors = []   # Objetos Actor para as portas
        self.ornaments = []     # Lista dos ornamentos

    def generate(self):
        # Gera os tiles do piso (cada tile tem 64x64 pixels)
        for y in range(self.height):
            for x in range(self.width):
                pos = (x * 64, y * 64)
                self.tiles.append({
                    "image": f"map/floors/{self.floor_type}.png",
                    "position": pos
                })
        # Gera os muros e portas
        self._generate_walls()
        # Adiciona ornamentos nas paredes onde não há porta
        self._generate_wall_ornaments()

    def _generate_walls(self):
        """
        Cria os muros na borda da sala. Se houver porta em alguma parede, ela é posicionada no centro.
        """
        cx = self.width // 2  # posição central horizontal (em tiles)
        cy = self.height // 2 # posição central vertical (em tiles)

        # Paredes superior e inferior
        for x in range(self.width):
            # Linha superior (y = 0)
            pos_top = (x * 64, 0)
            if x == cx and self.doors.get("up"):
                self._add_door("door_up", pos_top)
            else:
                self.walls.append({
                    "image": f"map/walls/{self.wall_type}.png",
                    "position": pos_top
                })
            # Linha inferior (y = height - 1)
            pos_bottom = (x * 64, (self.height - 1) * 64)
            if x == cx and self.doors.get("down"):
                self._add_door("door_down", pos_bottom)
            else:
                self.walls.append({
                    "image": f"map/walls/{self.wall_type}.png",
                    "position": pos_bottom
                })

        # Paredes laterais (excluindo os cantos já processados)
        for y in range(1, self.height - 1):
            # Coluna esquerda (x = 0)
            pos_left = (0, y * 64)
            if y == cy and self.doors.get("left"):
                self._add_door("door_left", pos_left)
            else:
                self.walls.append({
                    "image": f"map/walls/{self.wall_type}.png",
                    "position": pos_left
                })
            # Coluna direita (x = width - 1)
            pos_right = ((self.width - 1) * 64, y * 64)
            if y == cy and self.doors.get("right"):
                self._add_door("door_right", pos_right)
            else:
                self.walls.append({
                    "image": f"map/walls/{self.wall_type}.png",
                    "position": pos_right
                })

    def _add_door(self, door_type, position):
        """
        Cria um objeto Actor para a porta com a imagem correspondente e centraliza-o dentro do tile.
        Aqui adicionamos uma propriedade extra para guardar a direção (útil para detectar transição).
        """
        door = Actor(f"map/doors/{door_type}.png", (position[0] + 32, position[1] + 32))
        door.anchor = ('center', 'center')
        door.direction = door_type.split("_")[1]  # Obtém "up", "down", etc.
        self.door_actors.append(door)

    def _generate_wall_ornaments(self):
        """
        Adiciona ornamentos aleatórios aos muros onde não houver porta.
        """
        if not self.wall_ornaments:
            return

        for wall in self.walls:
            if random.choice([True, False]):
                x, y = wall["position"]
                # Confirma se não há porta nessa posição
                door_exists = any(
                    abs(door.x - (x + 32)) < 1 and abs(door.y - (y + 32)) < 1 
                    for door in self.door_actors
                )
                if not door_exists:
                    ornament = random.choice(self.wall_ornaments)
                    self.ornaments.append({
                        "image": f"map/wall_ornaments/{ornament}.png",
                        "position": (x, y)
                    })

    def draw(self, screen, offset=(0,0)):
        """
        Desenha a sala inteira com um deslocamento (offset).  
        O offset é usado no efeito de transição para posicionar a sala em uma posição deslocada.
        """
        # Desenha o piso
        for tile in self.tiles:
            pos = (tile["position"][0] + offset[0], tile["position"][1] + offset[1])
            screen.blit(tile["image"], pos)
        # Desenha os muros
        for wall in self.walls:
            pos = (wall["position"][0] + offset[0], wall["position"][1] + offset[1])
            screen.blit(wall["image"], pos)
        # Desenha os ornamentos
        for orn in self.ornaments:
            pos = (orn["position"][0] + offset[0], orn["position"][1] + offset[1])
            screen.blit(orn["image"], pos)
        # Desenha as portas
        for door in self.door_actors:
            door_pos = (door.x + offset[0] - door.width/2, door.y + offset[1] - door.height/2)
            screen.blit(door.image, door_pos)
