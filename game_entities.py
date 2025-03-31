# game_entities.py
"""
Este módulo define a hierarquia básica de entidades para um jogo,
incluindo personagens (Characters) e itens (Items).

A hierarquia proposta é a seguinte:

              Entity
                 │
    ┌────────────┴─────────────┐
    │                          │
Character                  Item
    │                          │
    ├────────────┐             ├─────────────┐
    │            │             │             │
Player       NPC/Enemy     Equipable     Consumable
                              │
                        ┌─────┴─────┐
                        Weapon    Armor
"""

# Classe base para tudo que existe no jogo.
class Entity:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def update(self, dt: float):
        """
        Atualiza a entidade.
        
        :param dt: Delta time (tempo decorrido) desde a última atualização.
        """
        pass

    def draw(self):
        """
        Desenha a entidade na tela.
        """
        pass


# Classe base para personagens (personagens, inimigos, NPCs)
class Character(Entity):
    def __init__(self, x: int, y: int, health: int = 100, speed: float = 1.0):
        super().__init__(x, y)
        self.health = health
        self.speed = speed

    def move(self, dx: float, dy: float):
        """
        Move o personagem de acordo com os vetores de deslocamento (dx, dy).
        """
        self.x += dx * self.speed
        self.y += dy * self.speed

    def attack(self, target: 'Character'):
        """
        Ataque simples: lógica para atacar outro personagem.
        
        :param target: Instância de Character que será atacada.
        """
        pass  # Implementar lógica de ataque


# Personagem controlado pelo jogador
class Player(Character):
    def __init__(self, x: int, y: int, health: int = 100, speed: float = 1.0):
        super().__init__(x, y, health, speed)
        self.inventory = []  # Lista para armazenar itens

    def add_item(self, item: 'Item'):
        """
        Adiciona um item ao inventário do jogador.
        """
        self.inventory.append(item)

# CLASSE: ActiveHero (Herói Ativo)
class ActiveHero(Player):
    def __init__(self, x: int, y: int, name: str = "Hero", initial_direction="down"):
        super().__init__(x, y, initial_direction)
        self.name = name

    def update(self, dt: float):
        # Aqui é onde capturamos o input do teclado para movimentar o herói ativo.
        # Lembre-se: estas funções (keyboard.<key>) estão disponíveis no ambiente do PGZero.
        if keyboard.left:
            self.move(-2, 0)
            self.current_direction = "left"
        elif keyboard.right:
            self.move(2, 0)
            self.current_direction = "right"
        elif keyboard.up:
            self.move(0, -2)
            self.current_direction = "up"
        elif keyboard.down:
            self.move(0, 2)
            self.current_direction = "down"
        # Chama o update da classe base para atualizar a animação e sincronizar a posição
        super().update(dt)

# Personagens não jogáveis (inimigos ou NPCs)
class NPC(Character):
    def __init__(self, x: int, y: int, health: int = 100, speed: float = 1.0):
        super().__init__(x, y, health, speed)
        self.dialogue = None  # Pode ser uma string ou objeto de diálogo

    def interact(self, player: Player):
        """
        Define a interação com o jogador.
        """
        pass


# Classe base para itens do jogo
class Item(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def use(self, target: Character):
        """
        Aplica o efeito do item sobre um target.
        """
        pass
"""
    Passo 1: Mova a implementação atual da classe Character para o módulo game_entities.py.

    Passo 2: Crie subclasses (como ActiveHero) que herdam de Character para implementar funcionalidades específicas (como input do teclado para o herói).

    Passo 3: No main.py, importe essas classes e utilize os métodos update() e draw() para refletir as mudanças em tela.
"""
# Itens que podem ser equipados para melhorar atributos do personagem
class Equipable(Item):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        # Atributos de bônus, por exemplo, de ataque ou defesa.
        self.attack_bonus = 0
        self.defense_bonus = 0


# Itens consumíveis que podem ser usados uma vez
class Consumable(Item):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.healing_amount = 0  # Valor para cura, por exemplo

    def use(self, target: Character):
        """
        Consome o item, aplicando um efeito (como recuperar saúde).
        """
        # Exemplo: aumenta a saúde do target
        target.health += self.healing_amount
        # Talvez remover o item do inventário, etc.
        pass


# subclasses específicas de equipamentos:
class Weapon(Equipable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.attack_bonus = 10  # Exemplo de valor para ataque


class Armor(Equipable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.defense_bonus = 5  # Exemplo de valor para defesa
