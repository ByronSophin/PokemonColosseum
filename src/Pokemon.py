import random
import math
typeTable = [#normal = 0 fire = 1 water = 2 electric = 3 grass = 4 other = 5
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 0.5, 0.5, 1.0, 2.0],
                [1.0, 2.0, 0.5, 1.0, 0.5],
                [1.0, 1.0, 2.0, 0.5, 0.5],
                [1.0, 0.5, 2.0, 1.0, 0.5],
                [1.0, 1.0, 1.0, 1.0, 1.0] # others
                                    ]

'''
    This class contains the properties of a Pokemon including the name, type, hp, attack, defense, and moves. This class also contains
    two methods for calculating damage this Pokemon deals to a defending Pokemon and how much health this Pokemon has after damage is dealt to it.
'''
class Pokemon:
    '''
        When a pokemon object is created the attributes name, type, hp, attack, defense, and moves are initialized.
    '''
    def __init__(self, name, type, hp, attack, defense, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves
    
    '''
        Takes in the parameters move, a Move object, and defender, a Pokemon object, and calculates the damage the move deals to the Pokemon.
    '''
    def Damage(self, move, defender):
        stab = 1.0
        if self.type == move.type: #attack bonus for move and pokemon having the same type
            stab = 1.5
        match move.type: #find the index in the typeTable for the correct type matching multiplier
            case 'Normal':
                row = 0
            case 'Fire':
                row = 1
            case 'Water':
                row = 2
            case 'Electric':
                row = 3
            case 'Grass':
                row = 4
            case _:
                row = 5
        match defender.type:
            case 'Normal':
                col = 0
            case 'Fire':
                col = 1
            case 'Water':
                col = 2
            case 'Electric':
                col = 3
            case 'Grass':
                col = 4  
        damage = move.power * (self.attack / defender.defense) * stab * typeTable[row][col] * (random.randint(5, 10)/10) #randint/10 generates numbers 0.5-1.0
        return math.ceil(damage) #non integer damage is rounded up
    
    def health(self, points): #takes in a integer and subtracts the value from current hp 
        self.hp = self.hp - points
        return self.hp
