#!/usr/bin/python
import pgzrun
import random
from menu import Menu
from pgzero.keyboard import keys

# Inicializa o menu
menu = Menu()
game_active = False  # Variável para indicar que o jogo está ativo

# -----------------------------
# WINDOW CONFIGURATION
# -----------------------------
WIDTH = 800
HEIGHT = 600
TITLE = "Automatic Alternated Turn"

# -----------------------------
# BASE CLASS: Character
# This class includes common walk and turn animations.
# -----------------------------
class Character:
    def __init__(self, x, y, initial_direction="down"):
        # Walk animation: each direction has 7 frames.
        self.directions = ["down", "left", "right", "up"]
        self.sprites = {
            d: [f"pawn/pawn_{d}/{i:02d}_pawn_{d}" for i in range(7)]
            for d in self.directions
        }
        self.current_direction = initial_direction
        self.current_frame = 0
        self.actor = Actor(self.sprites[initial_direction][0], center=(x, y))
        self.moving = False

        # Turn animation configuration.
        self.turning = False        # True while turn animation is active.
        self.turn_frame = 0         # Current index in the turn sequence.
        self.turn_timer = 3.0       # Inactivity time (in seconds) to trigger automatic turn.
        self.idle_turn = "forward"  # Current idle state: "forward" or "backward".
        self.current_turn_frames = []  # Sequence of frames used during turn.
        self.next_idle = None          # Next idle state after turning.

        # Turn sequences:
        # forward: frames 00 to 11 (idle frame is 11).
        self.forward_seq = [
            f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(0, 12)
        ]
        # backward: frames 12 to 23 (idle frame is 23).
        self.backward_seq = [
            f"pawn/pawn_turn/{i:02d}_pawn_turn" for i in range(12, 24)
        ]

    def animate_sprite(self):
        """Animate the walk if moving and not turning."""
        if self.moving and not self.turning:
            self.current_frame = (
                self.current_frame + 1
            ) % len(self.sprites[self.current_direction])
            self.actor.image = self.sprites[self.current_direction][
                self.current_frame
            ]

    def update_turn(self):
        """Update the turn animation if it is active."""
        if self.turning:
            self.turn_frame += 1
            if self.turn_frame < len(self.current_turn_frames):
                self.actor.image = self.current_turn_frames[self.turn_frame]
            else:
                # Turn finished; return to idle state.
                self.turning = False
                self.turn_frame = 0
                self.turn_timer = 3.0
                self.idle_turn = self.next_idle
                if self.idle_turn == "forward":
                    self.actor.image = self.forward_seq[-1]  # frame 11
                else:
                    self.actor.image = self.backward_seq[-1]  # frame 23

    def automatic_turn(self):
        """Trigger an automatic turn if the character is idle and not turning."""
        if not self.moving and not self.turning:
            self.turning = True
            self.turn_frame = 0
            if self.idle_turn == "forward":
                # Change from forward to backward.
                if random.choice([True, False]):
                    self.current_turn_frames = self.backward_seq[:]
                else:
                    self.current_turn_frames = list(reversed(self.backward_seq))
                self.next_idle = "backward"
            else:
                # idle_turn == "backward": change to forward.
                if random.choice([True, False]):
                    self.current_turn_frames = self.forward_seq[:]
                else:
                    self.current_turn_frames = list(reversed(self.forward_seq))
                self.next_idle = "forward"
            self.actor.image = self.current_turn_frames[0]

    def check_turn_timer(self):
        """Decrease the timer and trigger turn when time is up."""
        if not self.moving and not self.turning:
            self.turn_timer -= 0.1
            if self.turn_timer <= 0:
                self.automatic_turn()

    def update_idle(self):
        """Update the idle sprite based on the current turn state."""
        if not self.moving and not self.turning:
            if self.idle_turn == "forward":
                self.actor.image = self.forward_seq[-1]  # frame 11
            else:
                self.actor.image = self.backward_seq[-1]  # frame 23

    def update_position(self, speed):
        """Base method to update position.
        Should be overridden by subclasses.
        """
        pass

    def draw(self):
        self.actor.draw()


# -----------------------------
# CLASS: ActiveHero (controlled by keyboard)
# -----------------------------
class ActiveHero(Character):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update_position(self, speed):
        """Update the hero's position based on keyboard input if not turning."""
        if not self.turning:
            self.moving = False
            if keyboard.left:
                self.current_direction = "left"
                self.actor.x -= speed
                self.moving = True
            elif keyboard.right:
                self.current_direction = "right"
                self.actor.x += speed
                self.moving = True
            elif keyboard.up:
                self.current_direction = "up"
                self.actor.y -= speed
                self.moving = True
            elif keyboard.down:
                self.current_direction = "down"
                self.actor.y += speed
                self.moving = True

        if self.moving:
            self.turn_timer = 3.0
        else:
            self.update_idle()


# -----------------------------
# CLASS: Adversary (automated movement)
# -----------------------------
class Adversary(Character):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update_position(self, speed):
        """
        Simple example of automated movement:
        Moves the adversary randomly if not turning.
        """
        if not self.turning:
            # 50% chance to move on each update.
            if random.random() < 0.5:
                self.moving = True
                self.current_direction = random.choice(self.directions)
                if self.current_direction == "left":
                    self.actor.x -= speed
                elif self.current_direction == "right":
                    self.actor.x += speed
                elif self.current_direction == "up":
                    self.actor.y -= speed
                elif self.current_direction == "down":
                    self.actor.y += speed
                self.turn_timer = 3.0
            else:
                self.moving = False
                self.update_idle()


# -----------------------------
# CLASS: Piece (base class for Queen, Rook, Pawn)
# Pieces are static by default, but they can be animated when needed.
# -----------------------------
class Piece(Character):
    def __init__(self, x, y, initial_direction="down"):
        super().__init__(x, y, initial_direction)

    def update_position(self, speed):
        # Pieces are static by default.
        self.moving = False
        self.update_idle()


# Subclasses of Piece.
class Queen(Piece):
    pass


class Rook(Piece):
    pass


class Pawn(Piece):
    pass


# -----------------------------
# OBJECT INSTANCES
# -----------------------------
active_hero = ActiveHero(WIDTH // 2, HEIGHT // 2)
adversary = Adversary(WIDTH // 4, HEIGHT // 4)
# Example: a Queen piece positioned elsewhere.
queen_piece = Queen(WIDTH // 3, HEIGHT // 3)


# -----------------------------
# GLOBAL FUNCTION: update()
# Called automatically by pgzrun every frame.
# -----------------------------
def update():
    speed = 3
    active_hero.update_position(speed)
    adversary.update_position(speed)
    queen_piece.update_position(speed)


# -----------------------------
# Scheduled functions using clock.schedule_interval.
# They periodically call animation, turn, and timer methods.
# -----------------------------
def active_hero_animate():
    active_hero.animate_sprite()


def active_hero_turn():
    active_hero.update_turn()


def active_hero_timer():
    active_hero.check_turn_timer()


def adversary_animate():
    adversary.animate_sprite()


def adversary_turn():
    adversary.update_turn()


def adversary_timer():
    adversary.check_turn_timer()


# Scheduling for the active hero.
clock.schedule_interval(active_hero_animate, 0.1)   # animate hero's walk
clock.schedule_interval(active_hero_turn, 0.1)      # update hero's turn if active
clock.schedule_interval(active_hero_timer, 0.1)     # check timer for hero's turn

# Scheduling for the adversary.
clock.schedule_interval(adversary_animate, 0.1)
clock.schedule_interval(adversary_turn, 0.1)
clock.schedule_interval(adversary_timer, 0.1)


# -----------------------------
# GLOBAL FUNCTION: draw()
# Draws all objects on the screen.
# -----------------------------
def draw():
    screen.clear()
    active_hero.draw()
    adversary.draw()
    queen_piece.draw()


pgzrun.go()
