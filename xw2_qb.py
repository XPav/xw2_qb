import json
import os

path = 'c:\\dev\\xwing-data2\\data\\'

# Read ships and pilots
SHIPS = {}
PILOTS = {}
for r, d, f in os.walk(path + 'pilots'):
    for file in f:
        if '.json' in file:
            filename = os.path.join(r, file)
            with open(filename) as json_file:
                ship_json = json.load(json_file)
                SHIPS[ship_json['xws']] = ship_json
                for pilot in ship_json['pilots']:
                    if 'cost' in pilot:
                        PILOTS[pilot['xws']] = pilot

# Read upgrades                        
UPGRADES = {}                    
for r, d, f in os.walk(path + 'upgrades'):
    for file in f:
        if '.json' in file:
            filename = os.path.join(r, file)
            with open(filename) as json_file:
                upgrade_json = json.load(json_file)
                for upgrade in upgrade_json:
                    if 'cost' in upgrade:
                        UPGRADES[upgrade['xws']] = upgrade['cost']


# Read quick builds                        
QBS = []                        
for r, d, f in os.walk(path + 'quick-builds'):
    for file in f:
        if '.json' in file:
            filename = os.path.join(r, file)
            with open(filename) as json_file:
                qb_json = json.load(json_file)
                for qb in qb_json['quick-builds']:
                    QBS.append( qb )

# Add cost to quickbuilds
for qb in QBS:
    cost = 0
    for pilot in qb['pilots']:
        cost += PILOTS[pilot['id']]['cost']
        if 'upgrades' in pilot:
            for upgrade in pilot['upgrades'].values():
                for card in upgrade:
                    upgradecost = UPGRADES[card]
                    if 'variable' in upgradecost:
                        if upgradecost['variable'] == 'agility':
                            pass
                        elif upgradecost['variable'] == 'initiative':
                            pass
                        elif upgradecost['variable'] == 'size':
                            pass
                        else:
                            print( f"Unknown variability {upgradecost['variable']}")
                    else:
                        cost += upgradecost['value']
    qb['cost'] = cost

# Print out to CSV
print(QBS)


