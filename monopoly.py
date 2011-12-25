import random

class Player(object):
    def __init__(self):
        self.pos = 0
        self.in_jail = False
        
    def place(self):
        return names[self.pos]

# all positions are ordered from GO = 0
names = [
            'GO',
            'Old Kent Road',
            'COMMUNITY CHEST',
            'Whitechapel Road',
            'INCOME TAX',
            'Kings Cross Station',
            'The Angel Islington',
            'Euston Road',
            'Pentonville Road',
            'JAIL',
            'Pall Mall',
            'Electric Company',
            'Whitehall',
            'Northumberland Avenue',
            'Marylebone Station',
            'Bow Street',
            'Marlborough Street',
            'Vine Street',
            'FREE PARKING',
            'Strand',
            'CHANCE',
            'Fleet Street',
            'Trafalgar Square',
            'Fenchurch St Station',
            'Leicester Square',
            'Coventry Street',
            'Water Works',
            'Picadilly',
            'GO TO JAIL',
            'Regent Street',
            'Oxford Street',
            'Community Chest',
            'Bond Street',
            'Liverpool St Station',
            'CHANCE',
            'Park Lane',
            'SUPER TAX',
            'Mayfair'
            ]

# initialize hits-per-places dict
hits = {}
for k in names:
    hits[k] = 0

def dice_roll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return (dice1 + dice2, dice1 == dice2)

def go_to_jail(player):
    player.pos = names.index('JAIL')
    player.in_jail = True
    #print "Gone to jail"

def take_chance(player):
    card = random.randint(0, 15) # there are 16 chance cards
    # only consider those cards which change the position
    if card == 0:
        player.pos = names.index('GO')
    if card == 1:
        player.pos = names.index('Marylebone Station')
    if card == 2:
        player.pos = names.index('Mayfair')
    if card == 3:
        go_to_jail(player)
    if card == 4:
        player.pos = names.index('Pall Mall')
    if card == 5:
        player.pos = (player.pos - 3) % len(names) 
    if card == 6:
        player.pos = names.index('Trafalgar Square')

def take_community_chest(player):
    card = random.randint(0, 15) # there are 16 community chest cards
    # only consider those cards which change the position
    if card == 0:
        go_to_jail(player)
    if card == 1:
        player.pos = names.index('Old Kent Road')
    if card == 2:
        player.pos = names.index('GO')
    

def do_turn(player):
    doubles_in_a_row = 0
    while True:
        roll, is_double = dice_roll()
        doubles_in_a_row = doubles_in_a_row + 1

        if player.in_jail:
            if not is_double:   # TODO leave jail after 3 goes anyway
#                print "Staying in jail..."
                break
            else:
                player.in_jail = False
        
        player.pos = (player.pos + roll) % len(names)
        
#        if is_double:
#            print "Double!"
#        print "rolled %s, landed on %s" %(roll, player.place())
        hits[player.place()] = hits[player.place()] + 1
        
        if player.place() == 'CHANCE':
            take_chance(player)
            break

        if player.place() == 'COMMUNITY CHEST':
            take_community_chest(player)
            break
        
        if player.place() == 'GO TO JAIL':
            go_to_jail(player)
            break

        if not is_double:
            break
        
        if doubles_in_a_row == 3:
            go_to_jail(player);
            break
                
def sim(max_rolls):
    player = Player()
    for i in range(max_rolls):
        do_turn(player)

if __name__ == "__main__":
    # run 200 realiations of 1000 throws each
    for i in range(200):
        sim(1000)

    # print hits per place in order, least to most
    summary_hits = [(place, hits[place]) for place in sorted(hits, key=hits.get)]
    for place, count in summary_hits:
        print place, count
         

    
