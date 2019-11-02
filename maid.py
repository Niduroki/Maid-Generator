from flask import Flask, render_template, request
from datetime import datetime
import random
from data import *

app = Flask(__name__)

def r6():
        return random.randint(1,6)
def r66():
        return r6()*10+r6()
def r666():
        return r6()*100+r66()
def attr_roll():
        r1 = r6()
        r2 = r6()
        attr = (r1+r2)//3
        return [r1, r2, attr]

@app.route('/')
def index():
        random.seed(str(datetime.now()))
        forenames = ["Yuki", "Tsugumi", "Sasara", "Ryouko", "Aki", "Kotori", "Shizuho", "Chikako", "Asumi",]
        surnames = ["Tanaka", "Okamura", "Kokura", "Sugiura", "Kishita", "Ozaki", "Hayashida", "Ono",]
        example = random.choice(forenames) + " " + random.choice(surnames)
        return render_template("index.html", example=example, click_me=random.randint(1,99999))

@app.route('/<name>/')
def detail(name):
        random.seed("maid-rpg-seed-"+str(name))
        display = []
        charsheet_dict = {
                'attrs': {'at': None, 'af': None, 'sk': None, 'cu': None, 'lu': None, 'wi': None},
                'types': [],
                'colors': [],
                'qualities': [],
                'root': "",
                'explosion': "",
                'weapon': "",
                'item': [],
                'powers': "Choose one:",
                'favor': 0,
                'spirit': 0,
        }
        
        # Step 1: Attributes
        attr_display = {
                'at': attr_roll(),
                'af': attr_roll(),
                'sk': attr_roll(),
                'cu': attr_roll(),
                'lu': attr_roll(),
                'wi': attr_roll(),
        }
        display.append(attr_display)
        charsheet_dict['attrs']['at'] = attr_display['at'][2]
        charsheet_dict['attrs']['af'] = attr_display['af'][2]
        charsheet_dict['attrs']['sk'] = attr_display['sk'][2]
        charsheet_dict['attrs']['cu'] = attr_display['cu'][2]
        charsheet_dict['attrs']['lu'] = attr_display['lu'][2]
        charsheet_dict['attrs']['wi'] = attr_display['wi'][2]
        
        # Step 2: Maid Types
        type_display = [[r6()], [r6()]]
        for maid_type in type_display:
                if maid_type[0] == 1:
                        maid_type.append("Lolita – Luck +1, Athletics -1 – Childish, young, innocent, cute, sweet")
                        charsheet_dict['types'].append("Lolita")
                        charsheet_dict['attrs']['lu'] += 1
                        charsheet_dict['attrs']['at'] -= 1
                if maid_type[0] == 2:
                        maid_type.append("Sexy – Cunning +1, Will -1 – Charming, coquiettish, womanly body, glamorous")
                        charsheet_dict['types'].append("Sexy")
                        charsheet_dict['attrs']['cu'] += 1
                        charsheet_dict['attrs']['wi'] -= 1
                if maid_type[0] == 3:
                        maid_type.append("Pure – Affection +1, Cunning -1 – Pure, maidenly, clean, fragile")
                        charsheet_dict['types'].append("Pure")
                        charsheet_dict['attrs']['af'] += 1
                        charsheet_dict['attrs']['cu'] -= 1
                if maid_type[0] == 4:
                        maid_type.append("Cool – Skill +1, Affection -1 – Composed, expressionless, unflappable, doll-like")
                        charsheet_dict['types'].append("Cool")
                        charsheet_dict['attrs']['sk'] += 1
                        charsheet_dict['attrs']['af'] -= 1
                if maid_type[0] == 5:
                        maid_type.append("Boyish – Athletics +1, Skill -1 – Wild, energetic, vigorous, at first glance, looks like a boy")
                        charsheet_dict['types'].append("Boyish")
                        charsheet_dict['attrs']['at'] += 1
                        charsheet_dict['attrs']['sk'] -= 1
                if maid_type[0] == 6:
                        maid_type.append("Heroine – Will +1, Luck -1 – Earnest, single-minded, tries her very best")
                        charsheet_dict['types'].append("Heroine")
                        charsheet_dict['attrs']['wi'] += 1
                        charsheet_dict['attrs']['lu'] -= 1
        
        display.append(type_display)
        
        # Attribute < 0 auf 0 setzen
        for attr in charsheet_dict['attrs']:
                if charsheet_dict['attrs'][attr] <= 0:
                        charsheet_dict['attrs'][attr] = 0
        
        # Step 3: Maid Colors
        color_display = [[r66()],[r66()],[r66()],[r66()]]
        for c in color_display:
                c.append(colors[c[0]])
                charsheet_dict['colors'].append(colors[c[0]])
        
        display.append(color_display)
        
        # Step 4: Special Qualities
        # Struktur: [Wurf, Erster Eintrag, opt. 2. Wurf, opt. 2. Eintrag]
        qualities_display = [[r66()], [r66()]]
        for quality in qualities_display:
                quality.append(qualities[quality[0]])
                if quality[0] > 40:
                        roll = r6()
                        quality.append(roll)
                        quality.append(sub_qualities[quality[0]][roll])
                        charsheet_dict['qualities'].append(qualities[quality[0]] + " → " + sub_qualities[quality[0]][roll])
                else:
                        charsheet_dict['qualities'].append(qualities[quality[0]])
        
        display.append(qualities_display)
                        
        # Step 5: Etcetera
        root = r66()
        stress = r66()
        weapon = r66()
        item = r666()

        root_lookup = root - 1 if root % 2 == 0 else root
        stress_lookup = stress - 1 if stress % 2 == 0 else stress
        
        etcetera_display = {
                'root': [root, roots[root_lookup]], 'stress': [stress, explosions[stress_lookup]],
                'weapon': [weapon, weapons[weapon]], 'item': [item, items[item]]
        }
        display.append(etcetera_display)
        charsheet_dict['root'] = roots[root_lookup]
        charsheet_dict['explosion'] = explosions[stress_lookup]
        charsheet_dict['weapon'] = weapons[weapon]
        charsheet_dict['item'] = [item, items[item]]
        
        # Step 6: Maid Power
        attr_sum = 0
        highest = 0
        for attr in charsheet_dict['attrs'].values():
                attr_sum += attr
                if attr > highest:
                        highest = attr
        extra_power = True if attr_sum <= 9 else False
        
        power_attrs = []
        for attr in charsheet_dict['attrs'].items():
                if attr[1] == highest:
                        power_attrs.append(attr[0])

        power_display = {'power': []}
        for attr in power_attrs:
                roll = r6()
                power_display['power'].append([attr, roll, powers[attr][roll]])
                charsheet_dict['powers'] += "<br>" + powers[attr][roll]
        display.append(power_display)
        
        # Step 7: Favor and Spirit
        charsheet_dict['favor'] = charsheet_dict['attrs']['af']*2
        charsheet_dict['spirit'] = charsheet_dict['attrs']['wi']*10
        
        return render_template("maid.html", name=name, display=display, extra_power=extra_power, charsheet_dict=charsheet_dict, dice_img=dice_img)

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)
