import random
import time
import json
import os
import json

# Load dialogue from JSON file
def load_dialogue(filename):
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'r') as file:
        return json.load(file)

# Example usage
dialogue = load_dialogue('dialogue.json')
    
# Define player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def heal(self, amount):
        self.hp += amount

    def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack)
        enemy.take_damage(damage)
        return damage

    def defend(self):
        return random.randint(1, self.defense)

# Define enemy class
class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def attack_player(self, player):
        damage = random.randint(1, self.attack)
        player.take_damage(damage)
        return damage

# Function to simulate a fight between player and enemy
def combat(player, enemy, dialogue):
    print(dialogue['enemies'][enemy.name]['intro'])
    while player.is_alive() and enemy.is_alive():
        print(f"{player.name}: HP = {player.hp}, Gold = {player.gold}")
        print(f"{enemy.name}: HP = {enemy.hp}")
        print("1. Attack")
        print("2. Defend")
        choice = input("Choose your action (1 or 2): ")

        if choice == '1':
            player_damage = player.attack_enemy(enemy)
            print(dialogue['actions']['attack']['player'].format(enemy=enemy.name, damage=player_damage))
            if enemy.is_alive():
                enemy_damage = enemy.attack_player(player)
                print(dialogue['actions']['attack']['enemy'].format(enemy=enemy.name, damage=enemy_damage))

        elif choice == '2':
            player_defense = player.defend()
            enemy_damage = enemy.attack_player(player)
            if player_defense >= enemy_damage:
                print(dialogue['actions']['defend']['success'].format(enemy=enemy.name))
            else:
                damage_taken = enemy_damage - player_defense
                player.take_damage(damage_taken)
                print(dialogue['actions']['defend']['failure'].format(damage=damage_taken, enemy=enemy.name))

        else:
            print("Invalid choice. Try again.")

        print()
        time.sleep(1)  # Pause briefly after each action

    if player.is_alive():
        print(dialogue['enemies'][enemy.name]['defeat'])
        player.gold += random.randint(1, 10)
        player.heal(random.randint(5, 15))
        return True  # Player has won
    else:
        print(dialogue['player']['defeat'])
        return False  # Player has lost

# Function to start the game
def start_game(dialogue):
    print(dialogue['intro']['narrator'])
    player_name = input(dialogue['intro']['player_name_prompt']).strip()
    player = Player(player_name)

    enemies = [Enemy("Goblin", 20, 5), Enemy("Troll", 30, 8), Enemy("Dragon", 50, 15)]

    game_running = True
    while game_running and player.is_alive():
        enemy = random.choice(enemies)
        if not combat(player, enemy, dialogue):
            break

        choice = input(dialogue['actions']['continue_prompt']).strip().lower()
        if choice != 'yes':
            game_running = False

    print(dialogue['actions']['thanks'])

# Load dialogue from JSON file
dialogue = load_dialogue('dialogue.json')

# Start the game
start_game(dialogue)