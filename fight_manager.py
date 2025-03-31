import os
from pgzero.actor import Actor
from pgzero.clock import schedule_interval, unschedule  # Para agendamento e cancelamento de tarefas

# Caminho base da pasta 'images'
BASE_PATH = os.path.abspath(os.path.dirname(__file__))  # Diretório do fight_manager.py
IMAGES_PATH = os.path.join(BASE_PATH, "images")  # Sobe um nível para encontrar 'images'

def load_fight_frames(fight_folder):
    # Define o caminho completo para a pasta de lutas
    path = os.path.join(IMAGES_PATH, fight_folder)
    if not os.path.exists(path):
        print(f"Pasta {fight_folder} não encontrada. Usando 'pawn_vs_rook' como padrão.")
        fight_folder = "fights/pawn_vs_rook"  # Define a pasta padrão
        path = os.path.join(IMAGES_PATH, fight_folder)

    # Lista os arquivos no diretório
    all_files = os.listdir(path)
    fight_frames = sorted(
        [f"{fight_folder}/{file}" for file in all_files if file.endswith(".png")]
    )

    return fight_frames

class Fight(Actor):
    def __init__(self, winner, loser, fight_folder):
        # Calcula a posição central entre os dois atores
        center_x = (winner.actor.x + loser.actor.x) // 2
        center_y = (winner.actor.y + loser.actor.y) // 2

        # Carrega os frames da luta
        self.frames = load_fight_frames(fight_folder)
        self.frame_index = 0
        self.active = True  # Indica que a luta está em andamento

        # Inicializa como um Actor no centro
        super().__init__(self.frames[0], center=(center_x, center_y))

        self.winner = winner
        self.loser = loser

    def update(self):
        """Atualiza os frames da luta."""
        if self.active:
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]  # Atualiza o frame
            else:
                self.active = False  # Termina a luta
                self.resolve_fight()

    def resolve_fight(self):
        """Define o vencedor e atualiza o estado do jogo."""
        pieces.remove(self.loser)  # Remove a peça derrotada
        self.winner.active = True  # Reativa o vencedor
        print(f"{self.winner.kind} venceu {self.loser.kind}!")

    def draw(self):
        """Desenha o Actor da luta."""
        if self.active:
            self.actor.draw()

def start_fight(piece1, piece2):
    global current_fight
    folder = f"fights/{piece1.kind}_vs_{piece2.kind}"

    current_fight = Fight(piece1, piece2, folder)

    #piece1.active = False
    #piece2.active = False

def animate_fight(fight_folder, winner, loser):
    fight_frames = load_fight_frames(fight_folder)
    frame_index = [0]

    def update_frame():
        if frame_index[0] < len(fight_frames):
            winner.actor.image = fight_frames[frame_index[0]]
            loser.actor.image = fight_frames[frame_index[0]]
            frame_index[0] += 1
        else:
            unschedule(update_frame)
            finalize_fight(winner, loser)

    schedule_interval(update_frame, 0.1)

def finalize_fight(piece1, piece2):
    global pieces

    piece1.active = True
    piece2.active = True
    #print(f"{winner.kind} venceu {loser.kind}!")

