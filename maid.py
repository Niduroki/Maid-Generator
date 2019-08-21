from flask import Flask, render_template, request
from datetime import datetime
import random

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
        colors = {
                11: "Red",       12: "Purple",13: "Orange",14: "Pink",    15: "Brown",   16: "Vermillion",
                21: "Purple",    22: "Blue",  23: "Green", 24: "Sky Blue",25: "Navy",    26: "Indigo",
                31: "Orange",    32: "Green", 33: "Yellow",34: "Cream",   35: "Beige",   36: "Gold",
                41: "Pink",      42: "Sky",   43: "Cream", 44: "White",   45: "Gray",    46: "Silver",
                51: "Brown",     52: "Navy",  53: "Beige", 54: "Gray",    55: "Black",   56: "Metallic",
                61: "Vermillion",62: "Indigo",63: "Gold",  64: "Silver",  65: "Metallic",66: "Transparent or Rainbow",
        }
        for c in color_display:
                c.append(colors[c[0]])
                charsheet_dict['colors'].append(colors[c[0]])
        
        display.append(color_display)
        
        # Step 4: Special Qualities
        qualities = {
                11: "Glasses – You wear glasses, and can't use contact lenses. The frame design can be whatever you want",
                12: "Freckles – You have freckles",
                13: "Sickly – You've got an incurable disease. However, this doesn't adversely affect your attributes. Choose your own symptoms.",
                14: "Quiet – You have a cool, subtle demeanor. No, there are no rules regarding how often you speak.",
                15: "Easygoing – You take things slow and calm, at your own pace. This doesn't affect your attributes.",
                16: "Neat freak – You're obsessed with cleanliness, and can't let the tiniest bit of dirt go unnoticed.",
                21: "Brown Skin – Your skin is a dark brown color. It could be natural, or a tan.",
                22: "Albino – You have no pigment. You're not necessarily completely colorless, this could simply be a very pale complexion.",
                23: "Shy – You're very shy. Don't forget to remain silent when encountering NPCs you haven't met before.",
                24: "Actually A Guy – You're actually a guy (cross-dresser?). Or possibly a hermaphrodite.",
                25: "Overactive Imagination – You frequently get caught up in your own imaginary world, or else tend to daydream a lot.",
                26: "Greedy – You will do absolutely anything for the sake of money.",
                31: "Elf Ears – You have long, pointed ears.",
                32: "Nekomimi – This varies a bit depending on the setting, but you're a catgirl, with the ears and possibly tail of a cat.",
                33: "Android/Gynoid – You're not human, but rather a human-looking robot. Parts of your body are very obviously artificial.",
                34: "Vampire – You are a vampire, with long fangs. Be sure to act … vampiric.",
                35: "Princess – You're actually the daughter of a family of even greater standing than the master. Depending on the setting, you could even be from another country's royal family. Whether you are in disguise or not is up to you.",
                36: "Angel/Devil – You are a being from another world charged with judging good and evil.The design and the details of your origins are up to you.",
                41: "Uniform – You've managed to make a special arrangement with your uniform.",
                42: " Symbol – You have some kind of special mark on your uniform of headdress.",
                43: " Delinquent – Something about you is very much like a delinquent.",
                44: "Accent – You have an unusual way of speaking.", 45: " Hairstyle – You have a special hairstyle.",
                46: " Accesory – You have a special accessory attached to your uniform.",
                51: "Relationship – You have a relationship to another player character (Maid).",
                52: "Criminal Tendencies – You have an inclination towards criminal acts.",
                53: "Injury – Because of mistreatment or an accident, you have some kind of permanent physical injury.",
                54: "Tragic Love – You have had sad or tragic experiences with love.",
                55: "Dark Past – There is something dark in your personal history.",
                56: "Trauma – After some terrible incident, you were traumatized.",
                61: "Secret Job – You're not just a maid: you're secretly holding another job.",
                62: "Membership – In addition to being a maid, you're also a member of a certain organization.",
                63: "Shapeshifter – You are an animal or weapon that has taken the form of a maid.",
                64: "Monster – You're not human, but rather some kind of monster.",
                65: "Magic – You can use some kind of magical power.",
                66: "Absurd – You're something that flies in the face of common sense."
        }
        sub_qualities = {
                41: {
                        1: "Tights – In place of a skirt, you wear tights of some color. Athletic, colorful, sexy, or weird (leopard pattern, RAWR!) it's up to you. (For the purposes of the maid uniform rules, treat these as a skirt)",
                        2: "China Dress – You wear a Chinese-style cheongsam maid uniform. (For the purposes of the rules, treat this as a one-piece maid uniform).",
                        3: "Armor – Your maid uniform is actually a stylized suit of metal armor.",
                        4: "Bondage – Your maid uniform is made of shiny rubber or leather, and generally a bit suspicious.",
                        5: "Miniskirt – Your skirt is very short, to the point where one can almost see its contents.",
                        6: "Kappougi – Instead of a Western maid uniform, you wear a Japanese-style one with a kimono and an apron over it. See the picture of the sample maid Akebi for a picture of one."
                },
                42: {
                        1: "Skull –  Your headdress, apron, necktie, forehead, or chest has a skull mark.",
                        2: "Bat –  Your headdress, apron, necktie, forehead, or chest has a bat symbol.",
                        3: "Cross –  Your headdress, apron, necktie, forehead, or chest has a cross on it.",
                        4: "Yin-Yang –  Your headdress, apron, necktie, forehead, or chest has a yin-yang symbol.",
                        5: "Star –  Your headdress, apron, necktie, forehead, or chest has a five- or six-pointed star mark.",
                        6: "Card Suit –  Your headdress, apron, necktie, forehead, or chest is marked with one of the four suits from playing cards (heart, diamond, club, spade)."
                },
                43: {
                        1: "Cigarettes – You've always got a cigarette in your mouth, or are chomping on a cigar.",
                        2: "Tattoo – Somewhere on your body - or maybe even all over it - you have a tattoo.",
                        3: "Sunglasses – You always wear sunglasses or mirrorshades. Even at night.",
                        4: "Bad Expression – You have a perpetual unpleasant facial expression (as if you're always angry, or always about to kick ass at any moment), and this makes first meetings difficult.",
                        5: "Piercings – You have piercings, and not just in your ears, but perhaps your forehead, lips, eyelids, chin, etc.",
                        6: "Rough Speak – You talk like a gangster, be it a Mafioso or a street ganger."
                },
                44: {
                        1: "Southern – Y'all talk like some kinda' country bumpkin or somethin', from down in the American South.",
                        2: "British – You talk with a British accent of some kind. We'll leave it up to you what kind specifically. If you are already from the UK in real life, then you are now DOUBLE BRITISH. Or choose Scottish or Welsh.",
                        3: "Pidgin English – You come from a country/society where English is taught as a pidgin language. You might sound like a Japanese salaryman or pop idol (“Body Feels Exit!”). Pick a country and go with it.",
                        4: "Meow – You like to sprinkle cat sounds in your speech every now and then.",
                        5: "Knight – You sound like a knight from a movie, or possibly a Renaissance Faire reject. Remember to say “Thou art” and whatnot a lot.",
                        6: "Foreigner – Pick a foreign nationality for your Maid other than Japanese. American (Brooklyn, Texas), French, Russian, Mexican, Nigerian, Indian, Canadian, etc."
                },
                45: {
                        1: "Long Ringlets – Your hair is done up in large, long ringlets.",
                        2: "Dumplings –  Your hair is long, with “dumplings” on top.",
                        3: "Mesh – You have a mesh haircut, a short, stylish hairdo that's trendy in Japan.",
                        4: "Curly Hair –  Your hair is curly enough to defy gravity, and always takes the same shape.",
                        5: "One Eye Hair –  Your hair hangs down so that it conceals one of your eyes.",
                        6: "Antenna Hair –  Your hair has antennas/feelers and a mind of its own."
                },
                46: {
                        1: "Collar –  Among your standard equipment is a collar, like a dog would wear. Spikes are optional.",
                        2: "Large Ribbon –  You wear a large ribbon in your hair.",
                        3: "Spike –  Your maid uniform has spikes attached to it.",
                        4: "Chains –  Your maid uniform has jangling chains attached to it.",
                        5: "Black Leather Gloves –  You normally wear black leather gloves. These can be fingerless or have rivets if you like.",
                        6: "Pet –  You have a cat, snake, raven, or some other small animal as a pet that rests on your shoulder or in your hand."
                },
                51: {
                        1: "Sibling –  You're related by blood to one of the other characters.",
                        2: "Childhoof Friends –  You grew up together in the same neighborhood as one of the other characters, and have been great friends since a very early age.",
                        3: "Mentor –  You look upon one of the characters as a personal mentor, perhaps even as a father/mother figure",
                        4: "Friendly Rival –  You and another character are rivals in some area of life, and you always find yourself both consciously or subconsciously competing with, and comparing yourself with, that person. However, you are still friends (at least in appearance).",
                        5: "Ex-Lover/Love Rival –  You used to date another character. Perhaps there are still feelings. Alternately, you both might be seeking the love of a third person.",
                        6: "Vengeance –  Another character wronged you in some way in the past. She may not even realize that she did (and it might not have seemed a big deal). But you will never forget."
                },
                52: {
                        1: "Killer – You have a bad habit killing people.",
                        2: "Pyromaniac – You love setting fires. You might even set fire to the mansion.",
                        3: "Kleptomaniac – You can't help but steal things, regardless of whether or not you have any use for them.",
                        4: "Addict – Whether it's narcotics, stimulants, or just sleeping pills, you're a substance-abuser. If you don't get to have any, you'll experience withdrawal symptoms.",
                        5: "Otaku –  You have some obsession that you tirelessly pursue, with little or no regard for common sense.",
                        6: "Stalker –  You're stalking a particular person. Select the target from among the other PCs or the master."
                },
                53: {
                        1: "Patchwork –  Your body is covered with stitching scars.",
                        2: "One Eye –  You have only one eye. You're free to decide whether you wear an eye patch, and if so its design.",
                        3: "Burns –  Your face, body, etc. are covered with painful-looking scars from burns.",
                        4: "Whip Scars –  Your back and such is covered with painful-looking welts from whippings you received (and may possibly be still receiving?)",
                        5: "Bandages – You wear many bandages and casts, concealing injuries that will not heal.",
                        6: "Blind –  You were rendered blind a long time ago. (No particular penalties for this: See the classic Zatoichi movies for reference)."
                },
                54: {
                        1: "Seperations – For some reason love just never works out for you. At this point you've resigned yourself to fate.",
                        2: "Lover Died – You had a lover who died since then you've been afraid to fall in love.",
                        3: "Killed Your Lover – For whatever reason, you killed your last lover since then you've been afraid to fall in love. Or afraid for the object of your desire.",
                        4: "Former Prostitute – You used to sell your body, for cheap. A complex remains.",
                        5: "Betrayal – You were once betrayed by a lover since then you've been afraid to fall in love or let your guard down.",
                        6: "Stalker Damage – You were once victimized by a stalker. You can't trust members of the opposite sex … or maybe the same sex."
                },
                55: {
                        1: "Former Delinquent – Although no one would know it looking at you now, you used to be a delinquent. Fortunately right now there's no one (in the mansion at least) who knows about your past.",
                        2: "Former Killer – You were once a hired killer. Even now, your skills have not been dulled.",
                        3: "Amnesiac – You've lost your memories from when you were very young. (The GM should come up with something to reveal during the game).",
                        4: "Bad Reputation – You were involved with some bad stuff back in the day, and you have the dubious honor of being a legend for all the wrong reasons.",
                        5: "Wanted – The police want to question you about a serious crime.The player can decide whether or not the character is actually guilty.",
                        6: "Runaway – You've left your real home without permission."
                },
                56: {
                        1: "Suicide Attempts – In the past, you attempted suicide many times.",
                        2: "Killed Your Parents – For whatever reason, you are responsible for the death of your parents.",
                        3: "Saw Parent Die – You witnessed your parents' (one or both) death with your own eyes.",
                        4: "Sibling Hate – You and your sister(s) detest each other.",
                        5: "Family Breakup – For some reason (economic trouble?) your family was forced to break up. You may have even caused it.",
                        6: "Abusive Parents – You were raised by abusive parents."
                },
                61: {
                        1: "Assassin – While you put on the façade of being a maid, underneath you're a coldhearted killer for hire.",
                        2: "Hacker – Aside from being a maid, you're a hacker, breaking into computer systems.",
                        3: "Scientist – Along with being a maid, you're some kind of mad scientist.",
                        4: "Doctor/Pharmacist – In addition to being a maid, you have the skills of a doctor or a pharmacist.",
                        5: "Doujin Artist – In addition to being a maid, you create doujinshi in your spare time. You can decide the genre.",
                        6: "Pro Creator – Along with being a maid, you're working as a professional creator, craftsperson or artist. You can decide the form and genre of your works."
                },
                62: {
                        1: "Evil Secret Society – You're a member of an evil secret society that seeks to conquer or destroy the world.",
                        2: "Secret Agency – You're part of a secret agency under the government or the United Nations, some sort of intelligence agent or spy.",
                        3: "Cult – You're a member of some kind of eccentric cult, whether as a believer, a leader, or even the founder.",
                        4: "Political – You're part of a group organized around some kind of political ideal, possibly something extreme to the point of insanity.",
                        5: "Shadow Clan – You're a member of one of the secret organizations that has existed throughout history. You could be a ninja, a magician, one of the knights templar, a kung fu assassin, etc.",
                        6: "Government Official – You're actually a government official who is working as a maid, whether because you're a nurse, a detective going undercover, or a politician's secretary."
                },
                63: {
                        1: "Fox – You're actually a fox, and can display or hide your ears and tail at will.",
                        2: "Spider – You're actually a spider, and you can become an actual human-sized spider, or else just grow up to six extra arms at will.",
                        3: "Raven – You're actually a raven. You have black wings that can be displayed or hidden.",
                        4: "Bunny – You're actually a bunny, with bunny ears and a tail.",
                        5: "Tiger/Lion – You're actually a predatory cat, and you have ears, a tail, claws, and sharp teeth than you can display or hide at will.",
                        6: "Snake – You're actually a snake, and you can take on a naga form, turning the lower half of your body into a snake tail."
                },
                64: {
                        1: "Mermaid – You're actually a mermaid. You love water, and your ears sometimes look like fins.",
                        2: "Zombie/Mummy – You're actually an animated corpse. Your complexion is probably bad, and you have conspicuous wounds.",
                        3: "Werewolf – You're actually a werewolf (or maybe a weretiger). Whether or not you want to, you turn into a wolf (or tiger) during a full moon.",
                        4: "Succubus – You're actually a succubus, a female demon that traps her prey by arousing their desires. You have some demonic physical traits (you decide the specifics) that can be displayed or hidden.",
                        5: "Ghost – You're actually a ghost.You might have been one of the master's ancestors, or perhaps a maid who worked at the mansion in the past.",
                        6: "Shinigami – You're actually a shinigami, a death reaper. As such, you carry with you an aura of death. You might be there to deliver a specific person to the other side, or perhaps your reasons are more mundane."
                },
                65: {
                        1: "Priestess – You can use magic grounded in some kind of religious ceremony.You must use various types of religious symbols to do so.",
                        2: "Onmyouji – You practice Eastern-style magic based on Taoist principles. Your key item for this is jufu, special curse charms written in brush ink on strips of paper.",
                        3: "Fortuneteller – Within certain limits, you have the ability to predict the future. There are countless methods of divination.",
                        4: "Western Magician – You practice alchemy, Kabbalah, or some other form of Western sorcery. As such, you are a staff-wielding orthodox magician.",
                        5: "Devil Summoner – You know the spells necessary to summon demons. Your tools of the trade are magic circles, a black cloak, and ancient books.",
                        6: "Necromancer – You wield magic that lets you control the souls and bodies of the dead. Your tools of the trade include skulls and black clothes."
                },
                66: {
                        1: "Alien – You're an alien who came to our world from somewhere in outer space. Your body can have some special properties if you wish.",
                        2: "Cyborg – You were turned into a cyborg by an evil secret society or some other country.Your body can have some special features if you wish.",
                        3: "Runaway Ninja – You ran away from your ninja village.",
                        4: "Magical Girl – You came from a land of magic in order to train.",
                        5: "Fairy – You're one of the fae folk. You can be a generic pixie, or something more specific.",
                        6: "Mutant – You've suffered some kind of strange mutation."
                }
        }

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
        
        roots = {
                11: "Debts – Your family wound up with massive debts, and you found yourself coming to work at the mansion as repayment.",
                13: "Slave – You are a slave, and have no choice about your line of work.",
                15: "Mistress – Although you appear to be a maid, it would be more accurate to call you the master's lover.",
                21: "Revenge – The master is your hated enemy, and you are infiltrating his mansion in order to extract revenge.",
                23: "Orphan – You are an orphan adopted by the master or his parents.",
                25: "Illegitimate Child – You are an illegitimate child. From a legal standpoint you're no different from the master.",
                31: "Hereditary Maid – You were born into a family that has served the mansion for generations.",
                33: "Self Punishment – In order to punish yourself for your inexperience or sins, you have taken up the job of a maid.",
                35: "Unrequited Love – Following your one-sided love of the master, you have come here.",
                41: "Business – You are a maid because you want the wages. And that's about it.",
                43: "Infiltrator – You are a member of an organization that opposes the master, and you have been sent to spy on or possibly even assassinate him.",
                45: "Loyalty – You feel great loyalty to the master.",
                51: "Childhood Friend – As the master's childhood friend, you've used your influence to get here.",
                53: "Admirer of Maids – You have long admired maids, and through much hard work you've finally become one yourself.",
                55: "Returning a Favor – The master did a great service to you, and you have become a maid in order to repay him.",
                61: "Distant Relative – Although you are only distantly related to the master, your parents have put you in his care.",
                63: "Bridal Training –  You became a maid in order to prepare yourself to become an ideal bride some day.",
                65: "Who Knows? – You're really not quite sure how you wound up becoming a maid.",
        }
        
        explosions = {
                11: "Alcohol/Drugs – You drink alcohol (or drugs) until you can't remember or care.",
                13: "Stealing – You steal valuables from the mansion or from other maids.",
                15: "Violence – You unleash violence on the other maids and the master.",
                21: "Gambling – You use every penny you have for gambling.",
                23: "Racing – You get into whatever car/vehicle is handy and go for a drive at at least twice the speed limit.",
                25: "Teasing – You start persistently tormenting the other maids.",
                31: "Mischief – You start playing troublesome tricks on the master and the other maids.",
                33: "Running Away – You run away from the mansion.",
                35: "Complaining – You start incessantly complaining to the master and other maids.",
                41: "Seclusion – You go into your room and won't come out, not even for food.",
                43: "Crying – You start crying. There's no need for an Affection check for this.",
                45: "Rampage – You use anything you can lay your hands on to run around destroying things around the mansion.",
                51: "Shopping – You go crazy spending your money on shopping.",
                53: "Sleep – You spend all day sleeping.", 55: "Binge – You go crazy eating.",
                61: "Prayer – You escape through religion, relentlessly praying to heaven for protection.",
                63: "Spoiled Child – You act like a spoiled child, making demands of the master.",
                65: "Player Choice – Let the player to your left decide for you.",
        }
        weapons = {
                11: "Mop/Broom – You fight with a broom or mop. This is a maid's basic fighting style.",
                12: "Stun Gun – You keep a stun gun ready to attack enemies.",
                13: "Kitchen Knife – You wield some kind of ordinary kitchen knife.",
                14: "Frying Pan – You hit things with a frying pan.",
                15: "Vase/Bottle/Pot – When trouble happens, you grab something suitable from around the mansion and wave it around or throw it.",
                16: "Hand-to-Hand – You fight with your bare hands, whether striking attacks or submission moves.",
                21: "Revolver – You fight with a revolver. Feel free to decide what kind.",
                22: "Machinegun – You wield a machinegun. Feel free to decide what kind.",
                23: "Rifle – You wield a rifle. Feel free to decide what kind.",
                24: "Bomb/Grenade – You use bombs, grenades, or maybe plastic explosives.",
                25: "Bazooka – When a fight breaks out you pull out a big ass bazooka.",
                26: "Ray Gun – It might look like a prop of a 50s sci-fi B movie, but the ray gun you're packing really does hurt people.",
                31: "Metal Pipe/Nail Bat – You use some crude weapon like a pipe or a bat with nails in it.",
                32: "Hammer – You wield a hammer, whether a small throwing hammer, a big warhammer, or one of the squeaky toy variety.",
                33: "Scythe – You wield a big scythe worthy of the Grim Reaper.",
                34: "Kung Fu Weapon – Nunchucks, Three-Section Staff, Tonfa, Sai, Tai Chi Sword, etc.",
                35: "Chainsaw – Never mind how loud it is you fight with a chainsaw!",
                36: "Wooden Sword/Staff – You wield bokken - Japanese-style wooden sword - or a staff.",
                41: "Axe/Hatchet – A tomahawk, battle axe, halberd, etc.",
                42: "Morningstar – Basically a mace with spikes. You can have a flail instead if you like.",
                43: "Western Sword – A long sword, rapier, flamberge, two-handed sword, etc., etc.",
                44: "Whip – A normal whip, a cat of nine tails, a metal whip, etc.",
                45: "Spear/Lance – A spear, lance, javelin, etc.",
                46: "Exotic Weapon – A boomerang, qatar, African throwing irons, etc.",
                51: "Knife/Scalpel – You attack with a knife or scalpel. You can throw it too, and it can be a large dagger if you like.",
                52: "Chain/Rope – You attack with a chain or rope.",
                53: "Claws – You attack with claws, a bagh nakh, cestus, or some other claw-like weapon.",
                54: "Katana – You wield a katana, or possibly a kusarigama or some other traditional Japanese weapon.",
                55: "Shuriken/Kunai – You have a seemingly unlimited supply of shuriken (throwing stars), or kunai (ninja throwing knives).",
                56: "Halberd/Pole Arm – Naginata, halberd, bardiche, or some other kind of pole arm.",
                61: "Summoning – You are able to summon some kind of special being to attack. You can decide what you summon and how it attacks.",
                62: "Magic – You use magic to attack.",
                63: "Psychic Powers – Well, you have some kind of psychic/super power that you use to attack.You can decide the details.",
                64: "Book – You wield a book as a blunt instrument, and possibly tear out pages, to attack.",
                65: "Internal Weapons – You have some kind of weapons installed in your body.",
                66: "Religious Symbol – You can use a cross, prayer wheel, paper charm, or other seemingly harmless religious symbol to deliver attacks.",
        }
        # Items start at Page 93
        items = {
                111: "Parents' Locket", 112: "Typical Mask", 113: "Black Hole Cloak", 114: "Killer Intent (Satsui no Hadou)", 115: "Flying Guillotine", 116: "Mecha Suit",
                121: "Card Dueling Kind of War", 122: "Mah-Jongg Set", 123: "Evil Eye", 124: "Chef of Destruction", 125: "Ogre Face", 126: "Mysterious Vibrating Egg",
                131: "Gargoyle Suit", 132: "The Finest Maid Uniform in the World", 133: "Water-Soluble Maid Uniform", 134: "Non-Removable Maid Uniform", 135: "Eye of the Tiger", 136: "Delusional Date Fix-Up Tendencies",
                141: "Rumbling Tummy", 142: "Grave Blade", 143: "Mystical Starfish Weapon", 144: "Club of Gol-Fu", 145: "Crazy Cosplayer Suit", 146: "Role-playing Handbook",
                151: "Murderer's Frying Pan", 152: "Reverse Bat", 153: "Sundering Cross of Montezuma", 154: "Old Time Spectacles (Head Maid Only)", 155: "Unexpected Underwear", 156: "Wartime Kappougi Of Endurance",
                161: "Burdening Cross", 162: "Viscous Slimy Liquid", 163: "Maid Bath Towel", 164: "Pyrenean Rose", 165: "Big Ass Anime Sword", 166: "Deadly Omega Rage Whip",
                211: "Chivalrous Stand", 212: "Alchemist's Crystal", 213: "Whip of Love", 214: "Magical Baton", 215: "Food Mascot Suit", 216: "Left Arm Gun",
                221: "Protrusion", 222: "Battle Hair", 223: "Coffin", 224: "Reverse-Blade Katana", 225: "Positive Thinking", 226: "Drill Knuckle",
                231: "Picaresque Glove", 232: "Poison Touch", 233: "Phoenix Maid Uniform", 234: "World-Changing Song", 235: "Luchador Wrestling Mask", 236: "Piercing Fingers",
                241: "Artificial Arm", 242: "World-Rending Grudge Sword", 243: "Greenmerang", 244: "Corset of Fate", 245: "Old Kokeshi Doll", 246: "Demonic Poison War Elephant",
                251: "Annelids", 252: "Death Reaper", 253: "Pioneer", 254: "Mark of the Scapegoat", 255: "Anti-Lock Blade", 256: "Heavy Spear",
                261: "Destructive Tone Deafness", 262: "Evil Whisper", 263: "Harisen/Paper Fan", 264: "Maid Swimsuit", 265: "Dark Battle Dress", 266: "Romantic Vessel",
                311: "Rocket Pack", 312: "Maid Training Exoskeleton", 313: "Archangel's Eye", 314: "Poison Psychic Waves", 315: "Terrorist Group", 316: "That Collar-thing from that Really Awesome Movie",
                321: "Akashic Ouroboros", 322: "Murderous Stationary", 323: "Classic Japanese Flag", 324: "Angelic Demon Face", 325: "Pet Photograph", 326: "Personal Barrier",
                331: "Tear-Inducing Past", 332: "Memories of Powerful Foes", 333: "Kitty Gloves (Lolita Only)", 334: "Third-Stage Maid Uniform", 335: "Chaos Fist", 336: "Reindeer",
                341: "Yuppie Shirt", 342: "Mascara Bomb", 343: "Maid Soul (Non-Maids Only)", 344: "Shrine Maiden Satellite", 345: "Dragon Crest", 346: "Chromosome Cream",
                351: "Survive Card", 352: "Guardian Spirit", 353: "Solomon's Flute", 354: "Bureaucratic Soul", 355: "Monocle", 356: "Second Personality",
                361: "Devil Star", 362: "Indra's Maid Uniform", 363: "Cyber-Eye of Vecnut", 364: "Papillion (Masquerade Ball) Mask", 365: "Sealed Power", 366: "Master Screen",
                411: "Occult Book from Beyond", 412: "DekaBen™", 413: "Memento Music Box", 414: "102 Ultimate Essential Maid Arts", 415: "Challenge Gong", 416: "Devil Pen",
                421: "Letter Home", 422: "Cursed Straw Doll", 423: "Copycat", 424: "Juicy Diary", 425: "Decisive Coin", 426: "Shinigami Notebook",
                431: "Desu Note", 432: "Compromising Photos", 433: "Adamantium Chastity Belt", 434: "Arsenal Guitar Case", 435: "Ring Bought at the Night Fair", 436: "Maid Groupies",
                441: "Interfering Cockroaches", 442: "Mecha Beast", 443: "Super Gleaming Protein Brothers", 444: "Damaged Plushie", 445: "The Holy Grail", 446: "Skull Stone",
                451: "Demonic Ritual Book", 452: "Pancho the Dog", 453: "The Gimp", 454: "Love Potion", 455: "Government Cheese", 456: "Risky Dice",
                461: "Hell Phone", 462: "Portable Changing Room", 463: "Golden Pail", 464: "Dictator's Switch", 465: "Red and Blue Candies", 466: "Production Model Maid Robot",
                511: "Master Capturing Cage", 512: "Reset Button", 513: "Giant Growth Formula", 514: "Shrinking Formula", 515: "God of Romance", 516: "Enigmatic Silver Key",
                521: "Tam-Tam Seed", 522: "Fertility Goddess Milk", 523: "Secret Key", 524: "Hot Spring Resort Tickets", 525: "Texas-Sized T-Bone Steak", 526: "Murder Condom",
                531: "Certificate For Giving One Order to the Master", 532: "Angelic Rebirth Statue", 533: "Fir Seeds", 534: "Puppy Soba", 535: "Friend", 536: "Grecian Poisonous Snake",
                541: "Easily-Broken Vase", 542: "Cat With A Million Lives", 543: "Do Your Life Over Machine", 544: "Command Curse", 545: "Friendship Overcomes Evil Power", 546: "Snapmaid Dragon",
                551: "Ultimate One Billion Reverse-Prana Terminal Overdrive Omega Plus Power", 552: "Heavy Metal Roadie", 553: "The Only Neat Thing to Do", 554: "Red Rice", 555: "Violet Rose", 556: "Fan Survey Card",
                561: "Memory Fragment", 562: "True Nature", 563: "Once In A Lifetime Request", 564: "Crested Ibis", 565: "Bridal Night Rights", 566: "Earth-Destroying Bomb",
                611: "Carnivorous Refrigerator", 612: "Stairs of Legend", 613: "Execution Pit", 614: "Dark Temple", 615: "Dragon God Pond", 616: "Imperial Mausoleum",
                621: "Rose Gate", 622: "Mirror Seal Hallway", 623: "Zen Rock Garden", 624: "Surveillance Cameras", 625: "Underground Arena", 626: "What-If Box",
                631: "Creepy Laboratory", 632: "Sealed Room", 633: "Popular Guy Cell", 634: "Unpopular Guy Cell", 635: "Hook Shot", 636: "Pipe Organ of Memories",
                641: "Doberman", 642: "Crocodile That Doesn't Look Like A Crocodile", 643: "Nuclear Missile (Usable by Master Only)", 644: "No Pets Allowed", 645: "Bed Where Everyone Can Sleep", 646: "Independent Territory",
                651: "Carnivorous Pit", 652: "P.E. Shed", 653: "Secret Garden", 654: "Unseen Resident", 655: "Belfry Full of Bats", 656: "Gallows",
                661: "Spiritual Force Field", 662: "Secret Construction Plant", 663: "Mists of Ignorance", 664: "Sinister Raves", 665: "Hell Well", 666: "Banana Peel"
        }

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
        
        powers = {
                'at': {
                        1: "Super Evasion – In exchange for 1d6 Stress, you can completely avoid a single attack.",
                        2: "Iron Wall – You can use your Athletics attribute to defend up to two other characters.",
                        3: "Trespass – You can take 1d6 Stress to intrude on a battle, love scene, etc. You can also butt in after the action has ended, and this can even work when someone is using World For Two.",
                        4: "Weapon From Nowhere – You can pull your weapon out seemingly from nowhere, and get in a surprise attack. If you make a surprise attack, you get to make an attack roll without the target getting to make an opposed roll.",
                        5: "Giant Weapon – You can attack with a giant weapon. (+1 to Athletics for attacking).",
                        6: "Ultimate Retort – You can blow off an opponent completely by delivering a good retort (GM decides). You can make it impossible to defend against this by taking 2 Stress. (This must be role-played).",
                },
                'af': {
                        1: "Maiden's Tears – By taking 2D6 Stress, you can make a request that can't be refused. (This must be role-played).",
                        2: "World for Two – By taking 1D6 Stress, you can create a “world” for you and one other person, where for 5 minutes no one else can intrude.",
                        3: "Power of Friendship – You can take 1D6 Stress in order to remove 2D6 Stress from someone else.",
                        4: "Cooked With Love – When someone eats food you've prepared, they lose 1D6 Stress.",
                        5: "Windows of the Soul – You understand the master's feelings better than anyone, and can offer careful help. (Add 2 to Favor gained).",
                        6: "Passionate Gaze – With just a glance, you can ingratiate yourself with the master, taking 1D6 Stress to gain 1D3 Favor.",
                },
                'sk': {
                        1: "Lock Picking – You can enter any room whenever you feel like. This works even when someone is using World for Two.",
                        2: "Stalking – When you're following someone, there's no chance for them to detect you. Don't even bother rolling dice.",
                        3: "Lie Detector – By taking 1 Stress you can make other players or the master admit if they've lied.",
                        4: "Ultimate Menu – Add +1 to your Skill for the purposes of cooking.",
                        5: "Instant Cleaning – Add +1 to your Skill for the purposes of doing cleaning.",
                        6: "4-D Dress – You can produce anything in the mansion from within your maid uniform.",
                },
                'cu': {
                        1: "Punishment – When other maids make mistakes, you can gain the right to punish them, without them having a chance to make an opposed roll.",
                        2: "Instant Restraint – If you win a roll of Cunning Vs. Athletics, you can restrain someone from doing something indecent.",
                        3: "Coercion – If you win a roll of Cunning Vs. Athletics, you can completely damage or tear off someone's clothes, even “accidentally”.",
                        4: "Trap – Even if you aren't there at the time, you can have a trap prepared in advance during a battle.",
                        5: "Fake Crying – You can use fake frying to use your Cunning for what would normally be an Affection roll. (This must be role-played).",
                        6: "Mockery – When someone is taking Stress points, you can mock them and cause them to gain an additional 2 Stress points. (This must be role-played).",
                },
                'lu': {
                        1: "Karma – You can use your Luck to dodge an attack, and if you roll a 10 or higher you cause twice as much Stress to the opponent.",
                        2: "Saw It – You can declare that you've seen something happening in the mansion; you can decide the timing too.",
                        3: "Teleport – You can go just about anywhere in the mansion instantly.",
                        4: "Escape – You can completely flee from a battle without taking any Stress.",
                        5: "Foreboding – You can tell when something dangerous is coming.",
                        6: "Chance Meeting – By taking 2 points of Stress, you can have an NPC that's just showing up for the first time be an acquaintance from some time before.",
                },
                'wi': {
                        1: "Immune to Pain – During a battle, even if you're sent flying, you don't take any Stress. Outside of battle, however, you can still take Stress points like usual.",
                        2: "Crisis Adrenaline – You can spend 1D6 points of Favor to add an Athletics roll to your Stress. You cannot use this to deliberately avoid the natural removal of Stress points.",
                        3: "Persistence – Whenever you take Stress, automatically reduce the amount by 1 point.",
                        4: "Tenacity – Even after being defeated in battle, you can take 2 Stress to get to your feet.",
                        5: "Hard Work – Your relentless hard work pays off in the form of a +3 bonus to the end result (not the attribute or die roll) of Skill rolls.",
                        6: "Absolute Maid – You are the very epitome of a maid, and you take no penalties when not in full uniform.",
                },
        }

        power_display = {'power': []}
        for attr in power_attrs:
                roll = r6()
                power_display['power'].append([attr, roll, powers[attr][roll]])
                charsheet_dict['powers'] += "<br>" + powers[attr][roll]
        display.append(power_display)
        
        # Step 7: Favor and Spirit
        charsheet_dict['favor'] = charsheet_dict['attrs']['af']*2
        charsheet_dict['spirit'] = charsheet_dict['attrs']['wi']*10

        # Convenience
        dice_img = '<img src="data:image/jpg; base64, /9j/4AAQSkZJRgABAQEASABIAAD/2wBDABIMDRANCxIQDhAUExIVGywdGxgYGzYnKSAsQDlEQz85Pj1HUGZXR0thTT0+WXlaYWltcnNyRVV9hnxvhWZwcm7/2wBDARMUFBsXGzQdHTRuST5Jbm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm7/wAARCAAoACgDASIAAhEBAxEB/8QAGQAAAwEBAQAAAAAAAAAAAAAAAAQFAwIG/8QALBAAAgEDAgUCBQUAAAAAAAAAAQIDAAQRBRIGEyExQVFhMjOh4fAVIiNxsf/EABcBAAMBAAAAAAAAAAAAAAAAAAIDBAX/xAAkEQACAgECBgMBAAAAAAAAAAABAgARAwQxEiFBUWFxEyIykf/aAAwDAQACEQMRAD8A9rNNHAheRgoAyc1KGsQX0hjtbmJivUrG4Jx60arqNnYuBfTLGJWKqGBOftRBZ2kX8ltDDHvHxRoBuH9jvWFqtY7WtEDp5jlQRVteigvxaFrjmk4+WSPz3rW91i+tHQQWDXYbuwcLtpnlnwelcsu2pk1bIRw3/YfADGINRL7BLCUZsZGc7T6UUrH85Pdh/tFamj1GXKpLc4p1AmPEWiW+s7VmZkeM5V18Z7isRe6foq22nTXOxwgCb8nI7ZJ7DtW/FEl9BYSyaaMzgg9F3Hb5wKiQaYOJtPgudUSWC5jzGWQbeYo84I9z9ahyJbN8rfQMfYhg9t5pa2+twcTO0kjyWMjMSS4KhcHAA8EdB0q83VqTh1WwN7+nxzjnp+3Zg9x4z2zTrDrUmZmYjiWuXar8wwB0kfhq7nv7m4nlJ5RuNsS+gH4KKt6daKjBo0WONCcBRgE0VvaIWpaqB29RD71KLIr/ABKDWT2qN2JH1oop+TBjyftbghiNpEuOFLaTVk1EB+arByqsArMOxI+9U47ZnfDgqo7+9FFTPo8bOtkkDpDDmjHgAoAAwBRRRV8XP//Z">'
        
        return render_template("maid.html", name=name, display=display, extra_power=extra_power, charsheet_dict=charsheet_dict, dice_img=dice_img)

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)
