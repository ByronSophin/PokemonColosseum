'''
    Class contains necessary properties of Pokemon Moves including name, type, category, pp, and power. It also contains the available attribute
    which is a boolean value that is used to check if the move is currently available (true) or not available to be used (false).
'''
class Moves:
    def __init__(self, name, type, category, pp, power, available):
        self.name = name
        self.type = type
        self.category = category
        self.pp = pp
        self.power = power
        self.available = available
    

        