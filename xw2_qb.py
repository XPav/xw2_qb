import json
import os

def PrintPilot(pilot):
    fullpilot = PILOTS[pilot['id']]
    ship = SHIPS[fullpilot['ship']]

    s = f"{ship['name']} - {fullpilot['name']}"

    if 'upgrades' in pilot:
        for upgrade in pilot['upgrades'].values():
            for card in upgrade:
                fullcard = UPGRADES[card]
                s += f"+{fullcard['name']}"
    return s

def PrintPilots( pilots ):
    if len(pilots) > 2:
        raise ValueError
    if len(pilots) > 1:
        return f'{PrintPilot(pilots[0])},{PrintPilot(pilots[1])}'
    else:
        return f'{PrintPilot(pilots[0])},'


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
                        pilot['ship'] = ship_json['xws']
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
                        UPGRADES[upgrade['xws']] = upgrade

# Read quick builds                        
QBS = []                        
for r, d, f in os.walk(path + 'quick-builds'):
    for file in f:
        if '.json' in file:
            filename = os.path.join(r, file)
            with open(filename) as json_file:
                qb_json = json.load(json_file)
                for qb in qb_json['quick-builds']:
                    qb['faction'] = os.path.splitext(file)[0]
                    QBS.append( qb )

# Add cost to quickbuilds
for qb in QBS:
    cost = 0
    for pilot in qb['pilots']:
        cost += PILOTS[pilot['id']]['cost']
        ship = SHIPS[PILOTS[pilot['id']]['ship']]
        if 'upgrades' in pilot:
            for upgrade in pilot['upgrades'].values():
                for card in upgrade:
                    upgradecost = UPGRADES[card]['cost']
                    if 'variable' in upgradecost:
                        if upgradecost['variable'] == 'agility':
                            for stat in ship['stats']:
                                if 'type' in stat:
                                    if stat['type'] == 'agility':
                                        agility = stat['value']
                                        cost += upgradecost['values'][str(agility)]
                                        break
                        elif upgradecost['variable'] == 'initiative':
                            initiative = PILOTS[pilot['id']]['initiative']
                            cost += upgradecost['values'][str(initiative)]
                        elif upgradecost['variable'] == 'size':
                            cost += upgradecost['values'][ship['size']]
                        else:
                            print( f"Unknown variability {upgradecost['variable']}")
                    else:
                        cost += upgradecost['value']
    qb['cost'] = cost
    qb['ratio'] = float(cost) / qb['threat']

# Print out to CSV.  Faction, Ship0, Ship1, TL, Cost, Cost/TL
with open('xw2_qb.csv', 'w') as csv:
    csv.write('Faction, Ship0, Ship1, Threat, Cost, Ratio\n')
    for qb in QBS:
        s = f"{qb['faction']},{PrintPilots(qb['pilots'])},{qb['threat']},{qb['cost']},{qb['ratio']},\n"
        csv.write( s )



