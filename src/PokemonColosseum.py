'''
    Author: Byron Sophin
    Last Modified: 2/2/2024
    Description: This module creates a text-format Pokemon Colosseum game that can be played within a terminal. The user plays against
    Team Rocket where both teams consist of 3 randomly chosen Pokemons. Users can choose which move to use and the program ends when
    either team runs out of Pokemon.
'''

import csv
import ast
import Pokemon
import Moves
import random
import copy

'''
    Parse the moves-data.csv file and pokemon-data.csv file to create Moves and Pokemon objects from the Moves and Pokemon modules.
    The Moves objects are inserted into a dictionary, moves_dict. The pokemon-data.csv file contain the names of moves a Pokemon has. These names
    are used to look up the Moves object from the moves_dict dictionary and the matching Moves object is used when creating the Pokemon 
    object such that it also contains the Moves object and its properties.
'''
moves_filename = 'moves-data.csv'
moves_dict = {}
with open(moves_filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)

    for row in reader:
        moves = Moves.Moves(row[0], row[1], row[2], int(row[4]), int(row[5]), True)
        moves_dict[moves.name] = moves 
    csvfile.close()

pokemon_filename = 'pokemon-data.csv'
pokemon_dict = {}
with open(pokemon_filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)

    for row in reader:
        temp = ast.literal_eval(row[7])
        moves = []
        for move in temp:
            newMove = copy.copy(moves_dict[move])
            moves.append(newMove)
        mon = Pokemon.Pokemon(row[0], row[1], int(row[2]), int(row[3]), int(row[4]), moves)
        pokemon_dict[mon.name] = mon
    csvfile.close()

'''
    Two lists are created for both Team Rocket and the Player's Team. The list operates as a queue where randomly chosen Pokemon objects from the 
    dictionary pokemon_dict are appended to the end of the list.
'''
teamRocket = []
teamRed = []

while len(teamRocket) < 3:
    teamMember = random.choice(list(pokemon_dict.items()))[1]
    if teamMember in teamRocket:
        continue
    else:
        teamRocket.append(teamMember)
while len(teamRed) < 3:
    teamMember = random.choice(list(pokemon_dict.items()))[1]
    if teamMember in teamRed:
        continue
    elif teamMember in teamRocket:
        continue
    else:
        teamRed.append(teamMember)

#
print(f'Welcome to the Pokemon Colosseum!\n')
name = input(f"Enter Player Name:")

print(f'Team Rocket enters with {teamRocket[0].name} {teamRocket[1].name} {teamRocket[2].name}.\n')
print(f'Team {name} enters with {teamRed[0].name} {teamRed[1].name} {teamRed[2].name}.\n')
print("Let the battle begin!\n")

turn = random.randrange(0, 2) #used to choose between Team Rocket or Player's turn
num1 = 0 #used for counting how many moves were used/when to reset available moves
num2 = 0
if (turn % 2) == 0:
    print("Coin toss goes to ----- Team Rocket to start the battle!\n")
else:
    print(f'Coin toss goes to ----- Team {name} to start the battle!\n')

'''
    The while loop is broken when either teamRocket or teamRed lists are empty. If the integer value of variable turn is even, "Team Rocket's turn executes", and if
    odd, "Team Players turn executes". In the former scenario, an attack is chosen from the first pokemon in teamRocket list using random.choice. The attack
    is checked to see if the available attribute is true and if so the Damage method of the Pokemon class is called to calculate the damage dealt to
    the first pokemon in teamRed list and the health method is called to subtract the damage from the Pokemon's health. Using num1 to count the 
    number of moves used, when it is a multiple of the number of moves in the moves list then all moves.available are set back to true to be used 
    again. For Team Red/Players turn, similar operations are used but the attack is chosen by the user through standard input and checked to be a valid integer
    from the range of moves listed.
'''
while True:
    if (turn % 2) == 0:
        attack = random.choice(teamRocket[0].moves)
        while attack.available == False: #keep randomly choosing until an available move is chosen
            attack = random.choice(teamRocket[0].moves)
        damage = teamRocket[0].Damage(attack, teamRed[0])
        print(f'Team Rocket\'s {teamRocket[0].name} uses {attack.name} on {teamRed[0].name}.')
        print(f'{attack.name} deals {damage} damage to {teamRed[0].name}!')
        if teamRed[0].health(damage) < 0:
            print(f'Team {name}\'s {teamRed[0].name} faints back to the pokeball, and {teamRocket[0].name} has {teamRocket[0].hp} HP remaining.\n')
            teamRed.pop(0) #removes first Pokemon/ first in first out
            if teamRed:
                print(f'Team {name} sends out {teamRed[0].name}')
        else:
            print(f'Team Rocket\'s {teamRocket[0].name} has {teamRocket[0].hp} HP and Team {name}\'s {teamRed[0].name} has {teamRed[0].hp} HP remaining.\n')
        if not teamRed: #teamRed list is empty
            print(f'All of Team {name}\'s Pokemon have fainted. Team Rocket wins the battle!')
            break
        num1 = num1 + 1
        attack.available = False #attack was used and is no longer available until all moves are used
        if (num1 % len(teamRocket[0].moves)) == 0: #all moves have been used and available attributes are set back to true
            for items in teamRocket[0].moves:
               items.available = True
    else:
        print(f'Choose a move for {teamRed[0].name}\n')
        for i in range(len(teamRed[0].moves)): #prints all moves from the list and if it is not available (n/a) 
            if teamRed[0].moves[i].available == False:
                na = "(N/A)"
            else:
                na = ''
            print(f'{i + 1}: {teamRed[0].moves[i].name}{na}')
        while True: #handles invalid inputs including non integer inputs, integers outside specified range, and not available moves
            try:
                num = int(input(f"\n{name} chooses:")) #converts sting input to integer
                flag = True
            except ValueError:
                flag = False
            if flag == False: #input is a non integer
                print(f'Not a valid move selection. Please select a move from the range 1 - {len(teamRed[0].moves)}')
            elif num < 1 or num > len(teamRed[0].moves): #checked if input is in range 1-number of moves
                print(f'Not a valid move selection. Please select a move from the range 1 - {len(teamRed[0].moves)}')
            else:
                attack = teamRed[0].moves[num - 1]
                if attack.available == False: #move selected should not be available
                    print("That move can not be used right now. Please select an available move.")
                else: #imput and move selected is valid
                    break
        damage = teamRed[0].Damage(attack, teamRocket[0])
        print(f'\nTeam {name}\'s {teamRed[0].name} uses {attack.name} on {teamRocket[0].name}.')
        print(f'{attack.name} deals {damage} damage to {teamRocket[0].name}!')
        if teamRocket[0].health(damage) < 0:
            print(f'Team Rocket\'s {teamRocket[0].name} faints back to the pokeball, and {teamRed[0].name} has {teamRed[0].hp} HP remaining.\n')
            teamRocket.pop(0)
            if teamRocket:
                print(f'Team Rocket sends out {teamRocket[0].name}.')
        else:
            print(f'Team Rocket\'s {teamRocket[0].name} has {teamRocket[0].hp} HP and Team {name}\'s {teamRed[0].name} has {teamRed[0].hp} HP remaining.\n')
        if not teamRocket: #teamRocket list is empty and the program ends
            print(f'All of Team Rocket\'s Pokemon have fainted. Team {name} wins the battle!')
            break
        num2 = num2 + 1
        attack.available = False
        if (num2 % len(teamRed[0].moves)) == 0:#all moves have been used and available attributes are set back to true
            for items in teamRed[0].moves:
                items.available = True
    turn = turn + 1 #increment turn to switch between if and else/team rocket and team player
