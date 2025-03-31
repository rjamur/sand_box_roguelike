import os
from pgzero.actor import Actor
from pgzero.clock import schedule_interval, unschedule

# Pasta padrão se não existir a pasta dos lutadores desejada
DEFAULT_FIGHT_FOLDER = "fights/pawn_vs_rook"

def load_fight_frames(fight_folder):
    """
    Carrega os sprites da luta a partir da pasta de sprites.
    Se a pasta informada não existir, usa a pasta DEFAULT_FIGHT_FOLDER.
    """
    # Define o caminho base para a pasta "images"
    base_images_path = os.path.join("images")
    # Constrói o caminho completo para a pasta de lutas
    full_path = os.path.join(base_images_path, fight_folder)
    
    if not os.path.exists(full_path):
        print(f"Pasta '{fight_folder}' não encontrada. Usando '{DEFAULT_FIGHT_FOLDER}' como padrão.")
        fight_folder = DEFAULT_FIGHT_FOLDER
        full_path = os.path.join(base_images_path, fight_folder)
    
    # Lista e filtra os arquivos (assumindo extensão .png)
    all_files = os.listdir(full_path)
    fight_frames = sorted(
        [f"{fight_folder}/{file}" for file in all_files if file.endswith(".png")]
    )
    
    if not fight_frames:
        print("Nenhum sprite encontrado na pasta! Verifique os arquivos na pasta:", full_path)
    
    return fight_frames

class Fight:
    def __init__(self, winner, loser):
        """
        Inicializa uma luta entre winner e loser.
        Define a pasta de sprites com base nas peças e utiliza um fallback se necessário.
        """
        self.winner = winner
        self.loser = loser
        self.active = True
        self.current_frame = 0
        self.animation_counter = 0

        # Define o nome da pasta com base nos atributos dos lutadores.
        folder = f"fights/{winner.kind}_vs_{loser.kind}"
        self.frames = load_fight_frames(folder)
        
        # Define a posição central com base na posição dos atores.
        self.actor = Actor(self.frames[0], center=self._get_center_position())
        
        # Suporte para funcionalidades futuras:
        # Se o loser não tiver atributo "health", define um padrão (ex.: 100)
        if not hasattr(self.loser, "health"):
            self.loser.health = 100

    def _get_center_position(self):
        """Calcula a posição central entre os dois lutadores."""
        x = (self.winner.actor.x + self.loser.actor.x) // 2
        y = (self.winner.actor.y + self.loser.actor.y) // 2
        return (x, y)

    def animate_sprite(self):
        """
        Atualiza os sprites da luta.
        O método percorre os frames da animação, controlado por um contador.
        No final de cada ciclo, há espaço para aplicar efeitos (como dano gradual).
        """
        self.animation_counter += 1
        # Ajuste a velocidade da animação modificando o valor '5'
        if self.animation_counter % 5 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.actor.image = self.frames[self.current_frame]
            
            # Se atingiu o último frame, podemos aplicar efeitos adicionais.
            if self.current_frame == len(self.frames) - 1:
                self.apply_damage()
                self.check_fight_status()

    def apply_damage(self):
        """
        Aplica dano gradual à peça perdedora.
        Este método pode ser aprimorado com lógicas mais complexas futuramente.
        """
        damage = 10  # Valor de dano por ciclo (ajuste conforme necessário)
        self.loser.health -= damage
        print(f"{self.loser.kind} recebeu {damage} de dano. Energia restante: {self.loser.health}")

    def check_fight_status(self):
        """
        Verifica se a luta deve continuar ou terminar,
        baseado na energia (health) do perdedor.
        """
        if self.loser.health <= 0:
            print(f"{self.winner.kind} venceu a luta!")
            self.active = False
            self.resolve_fight()

    def resolve_fight(self):
        """
        Define o término da luta.
        Futuramente pode incluir remoção da peça, transição de estados, etc.
        """
        # Exemplo: removendo a peça perdedora de uma lista global 'pieces'
        try:
            pieces.remove(self.loser)
        except NameError:
            print("A variável global 'pieces' não está definida.")
        print(f"A luta terminou. {self.loser.kind} foi derrotado!")

    def update(self):
        """Atualiza a animação da luta se ela estiver ativa."""
        if self.active:
            self.animate_sprite()

    def draw(self):
        """Desenha a animação da luta na tela."""
        if self.active:
            self.actor.draw()
