
import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('dnd_character_info.db')
c = conn.cursor()

#Create table for DnD classes
c.execute('''CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            hit_die TEXT NOT NULL,
            description TEXT NOT NULL)
    ''')

# Insert all 13 DnD classes into the table in alphabetical order
dnd_classes = [
    (1, "Artificer", "1d8", "A master of invention, Artificers use ingenuity and magic to unlock extraordinary capabilities in objects."),
    (2, "Barbarian", "1d12", "A fierce warrior of primitive background who can enter a battle rage."),
    (3, "Bard", "1d8", "An inspiring magician whose power echoes the music of creation."),
    (4, "Cleric", "1d8", "A priestly champion who wields divine magic in service of a higher power."),
    (5, "Druid", "1d8", "A priest of the Old Faith, wielding the powers of nature and adopting animal forms."),
    (6, "Fighter", "1d10", "A master of martial combat, skilled with a variety of weapons and armor."),
    (7, "Monk", "1d8", "A master of martial arts, harnessing the power of the body in pursuit of physical and spiritual perfection."),
    (8, "Paladin", "1d10", "A holy warrior bound to a sacred oath."),
    (9, "Ranger", "1d10", "A warrior who uses martial prowess and nature magic to combat threats on the edges of civilization."),
    (10, "Rogue", "1d8", "A scoundrel who uses stealth and trickery to overcome obstacles and enemies."),
    (11, "Sorcerer", "1d6", "A spellcaster who draws on inherent magic from a gift or bloodline."),
    (12, "Warlock", "1d8", "A wielder of magic that is derived from a bargain with an extraplanar entity."),
    (13, "Wizard", "1d6", "A scholarly magic-user capable of manipulating the structures of reality."),
]

# # Insert classes into the database
c.executemany('INSERT OR IGNORE INTO classes VALUES (?, ?, ?, ?)', dnd_classes)

def main():
    # Step 1: Display available classes
    classes = fetch_classes()
    
    # Step 2: Ask the user to choose a class
    if classes:
        # Step 2: Ask the user to choose a class
        ask = int(input("What class do you want to choose? (Enter the class number): "))
        
        # Validate user input and get the selected class
        selected_class = next((cls for cls in classes if cls[0] == ask), None)
        
        if selected_class:
            print(f"\nYou chose the {selected_class[1]} class.")
            print(f"Here is a list of their abilities:\n")
            
            # Step 3: Fetch and display features of the selected class
            fetch_class_features(ask)
            print(f'\nWhat subclass do you want to pick for the {selected_class[1]}?\n')
            fetch_subclass(ask)
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Unable to fetch classes. Please check your database connection.")    



def fetch_classes():
    # Connect to the database
    conn = sqlite3.connect('dnd_character_info.db')
    c = conn.cursor()

    try:
        # Fetch all classes from the 'classes' table
        c.execute('SELECT * FROM classes')
        classes = c.fetchall()

        # Check if the query returned any results
        if classes:
            print("Available Classes:")
            for cls in classes:
                class_id = cls[0]
                class_name = cls[1]
                hit_die = cls[2]
                description = cls[3]

                print(f"{class_id}. {class_name}")
                print(f"Hit Die: {hit_die}")
                print(f"Description: {description}\n")
        else:
            print("No classes found in the database.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        classes = None

    # Close the connection
    conn.close()

    return classes




def fetch_class_features(class_id):
    # Connect to the database
    conn = sqlite3.connect('dnd_character_info.db')
    c = conn.cursor()

    try:
        # Fetch features for the specified class
        c.execute('SELECT * FROM features WHERE class_id = ? ORDER BY level', (class_id,))
        features = c.fetchall()

        # Check if any features were found
        if features:
            for feature in features:
                print(f"Level: {feature[3]}")
                print(f"Feature: {feature[2]}")
                print(f"Description: {feature[4]}")
                print("-" * 40)
        else:
            print("No features found for this class.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # Close the connection
    conn.close()

def fetch_subclass(class_id):
    conn = sqlite3.connect('dnd_character_info.db')
    c = conn.cursor()
    
    try:
        # Fetch subclasses for the specified class
        c.execute('SELECT * FROM subclasses WHERE class_id = ?', (class_id,))
        subclasses = c.fetchall()

        # Check if any subclasses were found
        if subclasses:
            for subclass in subclasses:
                print(f'{subclass[1]}. {subclass[2]}')
                print(f'Description: {subclass[3]}')
                print("-" * 40)
        else:
            print("No subclasses found for this class.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # Close the connection
    conn.close()


# Create table for class features
c.execute('''CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            feature_name TEXT NOT NULL,
            level INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(id))
    ''')


# # Artificer features from level 1 to 20
artificer_features = [
    (1, "Magical Tinkering", 1, "At 1st level, you've learned how to invest a spark of magic into "
    "mundane objects. To use this ability, you must have thieves' tools or artisan's tools in "
    "hand. You then touch a Tiny nonmagical object as an action and give it one of the following "
    "magical properties of your choice:\n\t" + chr(9679) + "The object sheds bright light in a "
    "5-foot radius and dim light for an additional 5 feet.\n\t" + chr(9679) + "Whenever tapped "
    "by a creature, the object emits a recorded message that can be heard up to 10 feet away. "
    "You utter the message when you bestow this property on the object, and the recording "
    "can be no more than 6 seconds long.\n\t" + chr(9679) + "The object continuously emits "
    "your choice of an odor or a nonverbal sound (wind, waves, chirping, or the "
    "like). The chosen phenomenon is perceivable up to 10 feet away.\n\t" + chr(9679) + "A "
    "static visual effect appears on one of the object's surfaces. This effect can be a "
    "picture, up to 25 words of text, lines and shapes, or a mixture of these elements, "
    "as you like.\n\nThe chosen property lasts indefinitely. As an action, you can touch "
    "the object and end the property early.\n\nYou can bestow magic on multiple objects, touching "
    "one object each time you use this feature, though a single object can only bear one property "
    "at a time. The maximum number of objects you can affect with this feature at one time "
    "is equal to your Intelligence modifier (minimum of one object). If you try to exceed "
    "your maximum, the oldest property immediately ends, and then the new property applies."),
    (1, "Spellcasting", 1, "You've studied the workings of magic and how to cast spells, "
    "channeling the magic through objects. To observers, you don't appear to be casting spells "
    "in a conventional way; you appear to produce wonders from mundane items and outlandish "
    "inventions.\n\nTools Required\n\nYou produce your artificer spell effects through your tools. "
    "You must have a spellcasting focus - specifically thieves' tools or some kind of "
    "artisan's tool - in hand when you cast any spell with this Spellcasting feature (meaning "
    "the spell has an 'M' component when you cast it). You must be proficient with the tool "
    "to use it in this way. See the equipment chapter in the Player's Handbook for descriptions "
    "of these tools.\n\nAfter you gain the Infuse Item feature at 2nd level, you can also use "
    "any item bearing one of your infusions as a spellcasting focus.\n\nCantrips\n\n"
    "At 1st level, you know two cantrips of your choice from the artificer spell list. At higher "
    "levels, you learn additional artificer cantrips of your choice, as shown in the Cantrips "
    "Known column of the Artificer table.\n\nWhen you gain a level in this class, you can replace "
    "one of the artificer cantrips you know with another cantrip from the artificer spell "
    "list.\n\nPreparing and Casting Spells\n\nThe Artificer table shows how many spell slots you "
    "have to cast your artificer spells. To cast one of your artificer spells of 1st level "
    "or higher, you must expend a slot of the spell's level or higher. You regain all "
    "expended spell slots when you finish a long rest.\n\nYou prepare the list of artificer "
    "spells that are available for you to cast, choosing from the artificer spell list. When "
    "you do so, choose a number of artificer spells equal to your Intelligence modifier + half "
    "your artificer level, rounded down (minimum of one spell). The spells must be of a level "
    "for which you have spell slots.\n\nFor example, if you are a 5th-level artificer, you have "
    "four 1st-level and two 2nd-level spell slots. With an Intelligence of 14, your list of "
    "prepared spells can include four spells of 1st or 2nd level, in any combination. If you "
    "prepare the 1st-level spell Cure Wounds, you can cast it using a lst-level or a "
    "2nd-level slot. Casting the spell doesn't remove it from your list of prepared "
    "spells.\n\nYou can change your list of prepared spells when you finish a long rest. "
    "Preparing a new list of artificer spells requires time spent tinkering with your "
    "spellcasting focuses: at least 1 minute per spell level for each spell on your list.\n\n"
    "Spellcasting Ability\n\nIntelligence is your spellcasting ability for your artificer spells; "
    "your understanding of the theory behind magic allows you to wield these spells with "
    "superior skill. You use your Intelligence whenever an artificer spell refers to your "
    "spellcasting ability. In addition, you use your Intelligence modifier when setting the "
    "saving throw DC for an artificer spell you cast and when making an attack roll with one.\n\t"
    "Spell save DC = 8 + your proficiency bonus + your Intelligence modifier\n\tSpell attack modifier "
    "= your proficiency bonus + your Intelligence modifier\n\nRitual Casting\n\nYou can cast an "
    "artificer spell as a ritual if that spell has the ritual tag and you have the spell prepared."),
    (1, "Infuse Item", 2, "At 2nd level, you've gained the ability to imbue mundane items with certain "
    "magical infusions, turning those objects into magic items.\n\nInfusions Known\n\nWhen you gain this "
    "feature, pick four artificer infusions to learn. You learn additional infusions of your choice "
    "when you reach certain levels in this class, as shown in the Infusions Known column of the "
    "Artificer table.\n\nWhenever you gain a level in this class, you can replace one of the artificer "
    "infusions you learned with a new one.\n\nInfusing an Item\n\nWhenever you finish a long rest, you "
    "can touch a nonmagical object and imbue it with one of your artificer infusions, turning it "
    "into a magic item. An infusion works on only certain kinds of objects, as specified in the "
    "infusion's description. If the item requires attunement, you can attune yourself to it the "
    "instant you infuse the item. If you decide to attune to the item later, you must do so "
    "using the normal process for attunement (see the attunement rules in the Dungeon Master's "
    "Guide).\n\nYour infusion remains in an item indefinitely, but when you die, the infusion "
    "vanishes after a number of days equal to your Intelligence modifier (minimum of 1 day). "
    "The infusion also vanishes if you replace your knowledge of the infusion.\n\nYou can infuse "
    "more than one nonmagical object at the end of a long rest; the maximum number of objects "
    "appears in the Infused Items column of the Artificer table. You must touch each of the "
    "objects, and each of your infusions can be in only one object at a time. Moreover, no "
    "object can bear more than one of your infusions at a time. If you try to exceed your "
    "maximum number of infusions, the oldest infusion ends, and then the new infusion "
    "applies.\n\nIf an infusion ends on an item that contains other things, like a bag "
    "of holding, its contents harmlessly appear in and around its space."),
    (1, "Artificer Specialist", 3, "Choose a specialty in a specific area of invention, "
    "such as Alchemist, Armorer, Artillerist, or Battle Smith."),
    (1, "The Right Tool for the Job", 3, "At 3rd level, you've learned how to produce "
    "exactly the tool you need: with thieves' tools or artisan's tools in hand, you can "
    "magically create one set of artisan's tools in an unoccupied space within 5 "
    "feet of you. This creation requires 1 hour of uninterrupted work, which can "
    "coincide with a short or long rest. Though the product of magic, the tools are nonmagical, "
    "and they vanish when you use this feature again."),
    (1, "Ability Score Improvement", 4, "When you reach 4th level, 8th, 12th, 16th, and 19th level, "
    "you can increase one ability score of your choice by 2, or you can increase two ability "
    "scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature."),
    (1, "Artificer Specialist Feature", 5, "Feature from your chosen Specialist"),
    (1, "Tool Expertise", 6, "At 6th level, your proficiency bonus is now doubled for any ability "
    "check you make that uses your proficiency with a tool."),
    (1, "Flash of Genius", 7, "At 7th level, you've gained the ability to come up with solutions "
    "under pressure. When you or another creature you can see within 30 feet of you makes an "
    "ability check or a saving throw, you can use your reaction to add your Intelligence modifier "
    "to the roll.\n\nYou can use this feature a number of times equal to your Intelligence modifier "
    "(minimum of once). You regain all expended uses when you finish a long rest."),
    (1, "Ability Score Improvement", 8, "When you reach 4th level, 8th, 12th, 16th, and 19th level, "
    "you can increase one ability score of your choice by 2, or you can increase two ability "
    "scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature."),
    (1, "Artificer Specialist Feature", 9, "Feature from your chosen Specialist"),
    (1, "Magic Item Adept", 10, "When you reach 10th level, you achieve a profound understanding "
    "of how to use and make magic items:\n\t" + chr(9679) + "You can attune to up to four magic "
    "items at once.\n\t" + chr(9679) + "If you craft a magic item with a rarity of common "
    "or uncommon, it takes you a quarter of the normal time, and it costs you half "
    "as much of the usual gold."),
    (1, "Spell-Storing Item", 11, "At 11th level, you can now store a spell in an object. "
    "Whenever you finish a long rest, you can touch one simple or martial weapon or one item "
    "that you can use as a spellcasting focus, and you store a spell in it, choosing a 1st- "
    "or 2nd-level spell from the artificer spell list that requires 1 action to cast (you "
    "needn't have it prepared).\n\nWhile holding the object, a creature can take an action "
    "to produce the spell's effect from it, using your spellcasting ability modifier. If the "
    "spell requires concentration, the creature must concentrate. The spell stays in the "
    "object until it's been used a number of times equal to twice your Intelligence "
    "modifier (minimum of twice) or until you use this feature again to store a spell in an object."),
    (1, "Ability Score Improvement", 12, "You can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (1, "Magic Item Savant", 14, "At 14th level, your skill with magic items deepens more:\n\t"
    + chr(9679) + "You can attune to up to five magic items at once.\n\t" + chr(9679) + "You ignore "
    "all class, race, spell and level requirements on attuning to or using a magic item."),
    (1, "Artificer Specialist Feature", 15, "Feature from your chosen Specialist"),
    (1, "Ability Score Improvement", 16, "You can increase one ability score of your choice by 2, or you "
    "can increase two ability scores of your choice by 1. As normal, you can't increase an ability score "
    "above 20 using this feature."),
    (1, "Magic Item Master", 18, "Starting at 18th level, you can attune up to six magic items at once."),
    (1, "Ability Score Improvement", 19, "You can increase one ability score of your choice by 2, or you "
    "can increase two ability scores of your choice by 1. As normal, you can't increase an ability score "
    "above 20 using this feature."),
    (1, "Soul of Artifice", 20, "At 20th level, you develop a mystical connection to your magic items, "
    "which you can draw on for protection:\n\t" + chr(9679) + "You gain a +1 bonus to all saving throws "
    "per magic item you are currently attuned to.\n\t" + chr(9679) + "If you're reduced to 0 hit points "
    "but not killed out-right, you can use your reaction to end one of your artificer infusions, "
    "causing you to drop to 1 hit point instead of 0."),
]

# Insert Artificer features into the database
c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', artificer_features)


barbarian_features = [
    (2, "Rage", 1, "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a "
    "bonus action.\n\nWhile raging, you gain the following benefits if you aren’t wearing heavy "
    "armor:\n\t" + chr(9679) + "You have advantage on Strength checks and Strength saving "
    "throws.\n\t" + chr(9679) + "When you make a melee weapon attack using Strength, you gain a bonus "
    "to the damage roll that increases as you gain levels as a barbarian, as shown in the Rage "
    "Damage column of the Barbarian table.\n\t" + chr(9679) + "You have resistance to bludgeoning, "
    "piercing, and slashing damage.\n\nIf you are able to cast spells, you can’t cast them or "
    "concentrate on them while raging.\n\nYour rage lasts for 1 minute. It ends early if you are "
    "knocked unconscious or if your turn ends and you haven’t attacked a hostile creature "
    "since your last turn or taken damage since then. You can also end your rage on your turn "
    "as a bonus action.\n\nOnce you have raged the number of times shown for your barbarian level "
    "in the Rages column of the Barbarian table, you must finish a long rest before you can rage again."),
    (2, "Unarmored Defense", 1, "While you are not wearing any armor, your Armor Class equals 10 "
    "+ your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit."),
    (2, "Reckless Attack", 2, "Starting at 2nd level, you can throw aside all concern for defense to "
    "attack with fierce desperation. When you make your first attack on your turn, you can decide to "
    "attack recklessly. Doing so gives you advantage on melee weapon attack rolls using Strength during "
    "this turn, but attack rolls against you have advantage until your next turn."),
    (2, "Danger Sense", 2, "At 2nd level, you gain an uncanny sense of when things nearby aren't "
    "as they should be, giving you an edge when you dodge away from danger. You have advantage on "
    "Dexterity saving throws against effects that you can see, such as traps and spells. To gain "
    "this benefit, you can't be blinded, deafened, or incapacitated."),
    (2, "Primal Path", 3, "Choose a primal path that shapes the nature of your rage. Your choice grants "
    "you features at 3rd level, 6th level, 10th level, and 14th level."),
    (2, "Ability Score Improvement", 4, "When you reach 4th level, and again at 8th, 12th, 16th, and 19th "
    "level, you can increase one ability score of your choice by 2, or you can increase two ability scores "
    "of your choice by 1. As normal, you can't increase an ability score above 20 using this feature."),
    (2, "Extra Attack", 5, "Beginning at 5th level, you can attack twice, instead of once, whenever "
    "you take the Attack action on your turn."),
    (2, "Fast Movement", 5, "Starting at 5th level, your speed increases by 10 feet while you "
    "aren't wearing heavy armor."),
    (2, "Path Feature", 6, "Feature from your chosen Path"),
    (2, "Feral Instinct", 7, "Your instincts are so honed that you have advantage on initiative rolls. "
    "Additionally, if you are surprised at the beginning of combat and aren't incapacitated, you can act "
    "normally on your first turn, but only if you enter your rage before doing anything else."),
    (2, "Ability Score Improvement", 8, "You can increase one ability score of your choice by 2, or "
    "you can increase two ability scores of your choice by 1. As normal, you can't increase an "
    "ability score above 20 using this feature."),
    (2, "Brutal Critical", 9, "Beginning at 9th level, you can roll one additional weapon "
    "damage die when determining the extra damage for a critical hit with a melee attack.\n\nThis "
    "increases to two additional dice at 13th level and three additional dice at 17th level."),
    (2, "Path Feature", 10, "Feature from your chosen Path"),
    (2, "Relentless Rage", 11, "Starting at 11th level, your rage can keep you fighting despite "
    "grievous wounds. If you drop to 0 hit points while you're raging and don't die outright, "
    "you can make a DC 10 Constitution saving throw. If you succeed, you drop to 1 hit point "
    "instead.\n\nEach time you use this feature after the first, the DC increases by 5. When "
    "you finish a short or long rest, the DC resets to 10."),
    (2, "Ability Score Improvement", 12, "You can increase one ability score of your choice by 2, or "
    "you can increase two ability scores of your choice by 1. As normal, you can't increase an "
    "ability score above 20 using this feature."),
    (2, "Brutal Critical (2 dice)", 13, "You can roll two additional weapon damage dice when "
    "determining the extra damage for a critical hit with a melee attack."),
    (2, "Path Feature", 14, "Feature from your chosen Path"),
    (2, "Persistent Rage", 15, "Beginning at 15th level, your rage is so fierce that it ends "
    "early only if you fall unconscious or if you choose to end it."),
    (2, "Ability Score Improvement", 16, "You can increase one ability score of your choice by 2, or "
    "you can increase two ability scores of your choice by 1. As normal, you can't increase an "
    "ability score above 20 using this feature."),
    (2, "Brutal Critical (3 dice)", 17, "You can roll three additional weapon damage dice when "
    "determining the extra damage for a critical hit with a melee attack."),
    (2, "Indomitable Might", 18, "Beginning at 18th level, if your total for a Strength check "
    "is less than your Strength score, you can use that score in place of the total."),
    (2, "Ability Score Improvement", 19, "You can increase one ability score of your choice by 2, or "
    "you can increase two ability scores of your choice by 1. As normal, you can't increase an "
    "ability score above 20 using this feature."),
    (2, "Primal Champion", 20, "At 20th level, you embody the power of the wilds. Your Strength "
    "and Constitution scores increase by 4. Your maximum for those scores is now 24."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', barbarian_features)

bard_features = [
    (3, "Spellcasting", 1, "You have learned to untangle and reshape the fabric of reality in harmony "
    "with your wishes and music. Your spells are part of your vast repertoire, magic that you can tune "
    "to different situations.\n\nCantrips\n\nYou know two cantrips of your choice from the bard spell "
    "list. You learn additional bard cantrips of your choice at higher levels, as shown in the "
    "Cantrips Known column of the Bard table.\n\nSpell Slots\n\nThe Bard table shows how many "
    "spell slots you have to cast your bard spells of 1st level and higher. To cast one of "
    "these spells, you must expend a slot of the spell's level or higher. You regain all "
    "expended spell slots when you finish a long rest. For example, if you know the "
    "1st-level spell Cure Wounds and have a 1st-level and a 2nd-level spell slot "
    "available, you can cast Cure Wounds using either slot.\n\nSpells Known of 1st "
    "Level and Higher\n\nYou know four 1st-level spells of your choice from the bard "
    "spell list.\n\nThe Spells Known column of the Bard table shows when you learn more "
    "bard spells of your choice. Each of these spells must be of a level for which you "
    "have spell slots, as shown on the table. For instance, when you reach 3rd level in "
    "this class, you can learn one new spell of 1st or 2nd level.\n\nAdditionally, when "
    "you gain a level in this class, you can choose one of the bard spells you know "
    "and replace it with another spell from the bard spell list, which also must be of "
    "a level for which you have spell slots.\n\nSpellcasting Ability\n\nCharisma is your "
    "spellcasting ability for your bard spells. Your magic comes from the heart and "
    "soul you pour into the performance of your music or oration. You use your "
    "Charisma whenever a spell refers to your spellcasting ability. In addition, you "
    "use your Charisma modifier when setting the saving throw DC for a bard spell you "
    "cast and when making an attack roll with one.\n\tSpell save DC = 8 + your "
    "proficiency bonus + your Charisma modifier\n\tSpell attack modifier = your "
    "proficiency bonus + your Charisma modifier\n\nRitual Casting\n\nYou can cast any "
    "bard spell you know as a ritual if that spell has the ritual tag.\n\nSpellcasting Focus\n\n"
    "You can use a musical instrument (found in chapter 5) as a spellcasting focus for "
    "your bard spells."),
    (3, "Bardic Inspiration", 1, "You can inspire others through stirring words or "
    "music. To do so, you use a bonus action on your turn to choose one creature "
    "other than yourself within 60 feet of you who can hear you. That creature gains "
    "one Bardic Inspiration die, a d6.\n\nOnce within the next 10 minutes, the "
    "creature can roll the die and add the number rolled to one ability check, "
    "attack roll, or saving throw it makes. The creature can wait until after it "
    "rolls the d20 before deciding to use the Bardic Inspiration die, but must decide "
    "before the DM says whether the roll succeeds or fails. Once the Bardic "
    "Inspiration die is rolled, it is lost. A creature can have only one "
    "Bardic Inspiration die at a time.\n\nYou can use this feature a number of "
    "times equal to your Charisma modifier (a minimum of once). You regain any "
    "expended uses when you finish a long rest.\n\nYour Bardic Inspiration die changes "
    "when you reach certain levels in this class. The die becomes a d8 at 5th "
    "level, a d10 at 10th level, and a d12 at 15th level."),
    (3, "Jack of All Trades", 2, "Starting at 2nd level, you can add half your "
    "proficiency bonus, rounded down, to any ability check you make that "
    "doesn't already include your proficiency bonus."),
    (3, "Song of Rest", 2, "Beginning at 2nd level, you can use soothing music "
    "or oration to help revitalize your wounded allies during a short rest. If you "
    "or any friendly creatures who can hear your performance regain hit points at the "
    "end of the short rest by spending one or more Hit Dice, each of those "
    "creatures regains an extra 1d6 hit points.\n\nThe extra Hit Points increase when "
    "you reach certain levels in this class: to 1d8 at 9th level, to 1d10 at 13th "
    "level, and to 1d12 at 17th level."),
    (3, "Bard College", 3, "At 3rd level, you delve into the advanced techniques "
    "of a bard college of your choice. Your choice grants you features at 3rd "
    "level and again at 6th and 14th level."),
    (3, "Expertise", 3, "At 3rd level, choose two of your skill proficiencies. "
    "Your proficiency bonus is doubled for any ability check you make that uses "
    "either of the chosen proficiencies.\n\nAt 10th level, you can choose "
    "another two skill proficiencies to gain this benefit."),
    (3, "Ability Score Improvement", 4, "When you reach 4th level, and again at "
    "8th, 12th, 16th, and 19th level, you can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. "
    "As normal, you can't increase an ability score above 20 using this feature."),
    (3, "Bardic Inspiration (d8)", 5, "Your Bardic Inspiration die becomes a d8."),
    (3, "College Feature", 6, "Feature from your chosen College."),
    (3, "Font of Inspiration", 6, "Beginning when you reach 5th level, you regain "
    "all of your expended uses of Bardic Inspiration when you finish a short or long rest."),
    (3, "Countercharm", 6, "At 6th level, you gain the ability to use musical notes or "
    "words of power to disrupt mind-influencing effects. As an action, you can start "
    "a performance that lasts until the end of your next turn. During that time, you "
    "and any friendly creatures within 30 feet of you have advantage on saving throws "
    "against being frightened or charmed. A creature must be able to hear you to "
    "gain this benefit. The performance ends early if you are incapacitated or "
    "silenced or if you voluntarily end it (no action required)."),
    (3, "Ability Score Improvement", 8, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. "
    "As normal, you can't increase an ability score above 20 using this feature."),
    (3, "Song of Rest (d8)", 9, "The die for Song of Rest becomes a d8"),
    (3, "Magical Secrets", 10, "By 10th level, you have plundered magical knowledge "
    "from a wide spectrum of disciplines. Choose two spells from any classes, "
    "including this one. A spell you choose must be of a level you can cast, as "
    "shown on the Bard table, or a cantrip.\n\nThe chosen spells count as bard "
    "spells for you and are included in the number in the Spells Known column of "
    "the Bard table.\n\nYou learn two additional spells from any classes at 14th "
    "level and again at 18th level."),
    (3, "Bardic Inspiration (d10)", 10, "Your Bardic Inspiration die becomes a d10."),
    (3, "Ability Score Improvement", 12, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. "
    "As normal, you can't increase an ability score above 20 using this feature."),
    (3, "Song of Rest (d10)", 13, "The die for Song of Rest becomes a d10"),
    (3, "College Feature", 14, "Feature from your chosen College."),
    (3, "Magical Secrets", 14, "Choose two additional spells from any class."),
    (3, "Bardic Inspiration (d12)", 15, "Your Bardic Inspiration die becomes a d12."),
    (3, "Ability Score Improvement", 16, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."
    "As normal, you can't increase an ability score above 20 using this feature."),
    (3, "Song of Rest (d12)", 17, "The die for Song of Rest becomes a d12"),
    (3, "Magical Secrets", 18, "Choose two additional spells from any class."),
    (3, "Ability Score Improvement", 19, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. "
    "As normal, you can't increase an ability score above 20 using this feature."),
    (3, "Superior Inspiration", 20, "At 20th level, when you roll initiative and "
    "have no uses of Bardic Inspiration left, you regain one use."),
]

# # Insert Artificer features into the database
c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', bard_features)

cleric_features = [
    (4, "Spellcasting", 1, "As a conduit for divine power, you can cast cleric "
    "spells.\n\nCantrips\n\nAt 1st level, you know three cantrips of your choice from "
    "the cleric spell list. You learn additional cleric cantrips of your choice "
    "at higher levels, as shown in the Cantrips Known column of the Cleric table."
    "\n\nSpell Slots\n\nThe Cleric table shows how many spell slots you have to cast "
    "your cleric spells of 1st level and higher. To cast one of these spells, "
    "you must expend a slot of the spell's level or higher. You regain all expended "
    "spell slots when you finish a long rest.\n\nYou prepare the list of cleric "
    "spells that are available for you to cast, choosing from the cleric spell "
    "list. When you do so, choose a number of cleric spells equal to your Wisdom "
    "modifier + your cleric level (minimum of one spell). The spells must be of "
    "a level for which you have spell slots.\n\nFor example, if you are a "
    "3rd-level cleric, you have four 1st-level and two 2nd-level spell slots. "
    "With a Wisdom of 16, your list of prepared spells can include six spells "
    "of 1st or 2nd level, in any combination. If you prepare the 1st-level "
    "spell Cure Wounds, you can cast it using a 1st-level or 2nd-level "
    "slot. Casting the spell doesn't remove it from your list of prepared "
    "spells.\n\nYou can change your list of prepared spells when you finish a "
    "long rest. Preparing a new list of cleric spells requires time spent in "
    "prayer and meditation: at least 1 minute per spell level for each spell "
    "on your list.\n\nSpellcasting Ability\n\nWisdom is your spellcasting ability "
    "for your cleric spells. The power of your spells comes from your devotion "
    "to your deity. You use your Wisdom whenever a cleric spell refers to "
    "your spellcasting ability. In addition, you use your Wisdom modifier "
    "when setting the saving throw DC for a cleric spell you cast and when "
    "making an attack roll with one.\n\tSpell save DC = 8 + your proficiency "
    "bonus + your Wisdom modifier\n\tSpell attack modifier = your proficiency "
    "bonus + your Wisdom modifier\n\nRitual Casting\n\nYou can cast a cleric "
    "spell as a ritual if that spell has the ritual tag and you have the "
    "spell prepared.\n\nSpellcasting Focus\n\nYou can use a holy symbol as a "
    "spellcasting focus for your cleric spells."),
    (4, "Divine Domain", 1, "At 1st level, you choose a domain shaped by "
    "your choice of Deity and the gifts they grant you. Your choice grants "
    "you domain spells and other features when you choose it at 1st level. It "
    "also grants you additional ways to use Channel Divinity when you gain that "
    "feature at 2nd level, and additional benefits at 6th, 8th, and 17th levels."),
    (4, "Channel Divinity", 2, "At 2nd level, you gain the ability to channel "
    "divine energy directly from your deity, using that energy to fuel magical "
    "effects. You start with two such effects: Turn Undead and an effect determined "
    "by your domain. Some domains grant you additional effects as you advance "
    "in levels, as noted in the domain description.\n\nWhen you use your Channel "
    "Divinity, you choose which effect to create. You must then finish a short "
    "or long rest to use your Channel Divinity again.\n\nSome Channel Divinity "
    "effects require saving throws. When you use such an effect from this "
    "class, the DC equals your cleric spell save DC.\n\nBeginning at 6th "
    "level, you can use your Channel Divinity twice between rests, and "
    "beginning at 18th level, you can use it three times between rests. "
    "When you finish a short or long rest, you regain your expended uses."),
    (4, "Channel Divinity: Turn Undead", 2, "As an action, you present "
    "your holy symbol and speak a prayer censuring the undead. Each "
    "undead that can see or hear you within 30 feet of you must make a "
    "Wisdom saving throw. If the creature fails its saving throw, it is "
    "turned for 1 minute or until it takes any damage.\n\nA turned creature "
    "must spend its turns trying to move as far away from you as it "
    "can, and it can't willingly move to a space within 30 feet of "
    "you. It also can't take reactions. For its action, it can use only "
    "the Dash action or try to escape from an effect that prevents it "
    "from moving. If there's nowhere to move, the creature can use "
    "the Dodge action."),
    (4, "Ability Score Improvement", 4, "When you reach 4th level, and again at "
    "8th, 12th, 16th, and 19th level, you can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (4, "Destroy Undead (CR 1/2)", 5, "Starting at 5th level, when an undead fails "
    "its saving throw against your Turn Undead feature, the creature is instantly "
    "destroyed if its challenge rating is at or below a certain threshold, as "
    "shown in the Cleric table above."),
    (4, "Divine Domain", 6, "Feature from your chosen Domain"),
    (4, "Ability Score Improvement", 8, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (4, "Divine Domain", 8, "Feature from your chosen Domain"),
    (4, "Destroy Undead (CR 1)", 8, "When an undead fails its saving throw against "
    "your Turn Undead feature, the creature is instantly destroyed if its challenge "
    "rating is at or below 1."),
    (4, "Divine Intervention", 10, "Beginning at 10th level, you can call on your "
    "deity to intervene on your behalf when your need is great.\n\nImploring your "
    "deity's aid requires you to use your action. Describe the assistance you "
    "seek, and roll percentile dice. If you roll a number equal to or lower "
    "than your cleric level, your deity intervenes. The DM chooses the nature "
    "of the intervention; the effect of any cleric spell or cleric domain "
    "spell would be appropriate. If your deity intervenes, you can't use this "
    "feature again for 7 days. Otherwise, you can use it again after you finish "
    "a long rest.\n\nAt 20th level, your call for intervention succeeds "
    "automatically, no roll required."),
    (4, "Destroy Undead (CR 2)", 11, "When an undead fails its saving throw "
    "against your Turn Undead feature, the creature is instantly destroyed if "
    "its challenge rating is at or below 2."),
    (4, "Ability Score Improvement", 12, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (4, "Destroy Undead (CR 3)", 14, "When an undead fails its saving throw "
    "against your Turn Undead feature, the creature is instantly destroyed if "
    "its challenge rating is at or below 3."),
    (4, "Ability Score Improvement", 16, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (4, "Destroy Undead (CR 4)", 17, "When an undead fails its saving throw "
    "against your Turn Undead feature, the creature is instantly destroyed if "
    "its challenge rating is at or below 4."),
    (4, "Divine Domain", 17, "Feature from your chosen Domain"),
    (4, "Channel Divinity (x3)", 18, "You can use your Channel Divinity three times between rests"),
    (4, "Ability Score Improvement", 19, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (4, "Divine Intervention Improvement", 20, "When you use your Divine "
    "Intervention feature, it automatically succeeds, no roll required."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', cleric_features)


druid_features = [
    (5, "Druidic", 1, "You know Druidic, the secret language of druids. You can speak the language "
    "and use it to leave hidden messages. You and others who know this language automatically "
    "spot such a message. Others spot the message's presence with a successful DC 15 "
    "Wisdom (Perception) check but can't decipher it without magic."),
    (5, "Spellcasting", 1, "Drawing on the divine essence of nature itself, you can cast spells "
    "to shape that essence to your will.\n\nCantrips\n\nAt 1st level, you know two cantrips of "
    "your choice from the druid spell list. You learn additional druid cantrips of your "
    "choice at higher levels, as shown in the Cantrips Known column of the Druid table."
    "\n\nPreparing and Casting Spells\n\nThe Druid table shows how many spell slots you have "
    "to cast your druid spells of 1st level and higher. To cast one of these druid spells, "
    "you must expend a slot of the spell's level or higher. You regain all expended spell "
    "slots when you finish a long rest.\n\nYou prepare the list of druid spells that are "
    "available for you to cast, choosing from the druid spell list. When you do so, choose "
    "a number of druid spells equal to your Wisdom modifier + your Druid level (minimum of "
    "one spell). The spells must be of a level for which you have spell slots.\n\nFor example, "
    "if you are a 3rd-level druid, you have four 1st-level and two 2nd-level spell slots. With "
    "a Wisdom of 16, your list of prepared spells can include six spells of 1st or 2nd "
    "level, in any combination. If you prepare the 1st-level spell Cure Wounds, you can "
    "cast it using a 1st-level or 2nd-level slot. Casting the spell doesn't remove it "
    "from your list of prepared spells.\n\nYou can also change your list of prepared "
    "spells when you finish a long rest. Preparing a new list of druid spells requires "
    "time spent in prayer and meditation: at least 1 minute per spell level for each "
    "spell on your list.\n\nSpellcasting Ability\n\nWisdom is your spellcasting ability "
    "for your druid spells, since your magic draws upon your devotion and attunement "
    "to nature. You use your Wisdom whenever a spell refers to your spellcasting "
    "ability. In addition, you use your Wisdom modifier when setting the saving "
    "throw DC for a druid spell you cast and when making an attack roll with one.\n\tSpell "
    "save DC = 8 + your proficiency bonus + your Wisdom modifier\n\tSpell attack modifier "
    "= your proficiency bonus + your Wisdom modifier\n\nRitual Casting\n\nYou can cast a "
    "druid spell as a ritual if that spell has the ritual tag and you have the spell "
    "prepared.\n\nSpellcasting Focus\n\nYou can use a druidic focus as a spellcasting "
    "focus for your druid spells."),
    (5, "Wild Shape", 2, "Starting at 2nd level, you can use your action to magically "
    "assume the shape of a beast that you have seen before. You can use this feature "
    "twice. You regain expended uses when you finish a short or long rest.\n\nYour druid "
    "level determines the beasts you can transform into, as shown in the Beast Shapes "
    "table. At 2nd level, for example, you can transform into any beast that has a "
    "challenge rating of 1/4 or lower that doesn't have a flying or swimming speed.\n\nYou "
    "can stay in a beast shape for a number of hours equal to half your druid level "
    "(rounded down). You then revert to your normal form unless you expend another use "
    "of this feature. You can revert to your normal form earlier by using a bonus "
    "action on your turn. You automatically revert if you fall unconscious, drop to "
    "0 hit points, or die.\n\nWhile you are transformed, the following rules apply:\n\t "
    + chr(9679) + "Your game statistics are replaced by the statistics of the beast, "
    "but you retain your alignment, personality, and Intelligence, Wisdom, and Charisma "
    "scores. You also retain all of your skill and saving throw proficiencies, in addition "
    "to gaining those of the creature. If the creature has the same proficiency as "
    "you and the bonus in its stat block is higher than yours, use the creature's bonus "
    "instead of yours. If the creature has any legendary or lair actions, you can't "
    "use them.\n\t" + chr(9679) + "When you transform, you assume the beast's hit "
    "points and Hit Dice. When you revert to your normal form, you return to the number "
    "of hit points you had before you transformed. However, if you revert as a result "
    "of dropping to 0 hit points, any excess damage carries over to your normal form, "
    "For example, if you take 10 damage in animal form and have only 1 hit point left, "
    "you revert and take 9 damage. As long as the excess damage doesn't reduce your "
    "normal form to 0 hit points, you aren't knocked unconscious.\n\t" + chr(9679) + "You "
    "can't cast spells, and your ability to speak or take any action that requires hands "
    "is limited to the capabilities of your beast form. Transforming doesn't break your "
    "concentration on a spell you've already cast, however, or prevent you from taking "
    "actions that are part of a spell, such as Call Lightning, that you've already cast.\n\t"
    + chr(9679) + "You retain the benefit of any features from your class, race, or other "
    "source and can use them if the new form is physically capable of doing so. However, "
    "you can't use any of your special senses, such as darkvision, unless your new form "
    "also has that sense.\n\t" + chr(9679) + "You choose whether your equipment falls "
    "to the ground in your space, merges into your new form, or is worn by it. Worn "
    "equipment functions as normal, but the DM decides whether it is practical for "
    "the new form to wear a piece of equipment, based on the creature's shape and "
    "size. Your equipment doesn't change size or shape to match the new form, and any "
    "equipment that the new form can't wear must either fall to the ground or merge "
    "with it. Equipment that merges with the form has no effect until you leave the form."),
    (5, "Druid Circle", 2, "At 2nd level, you choose to identify with a circle of druids. "
    "Your choice grants you features at 2nd level and again at 6th, 10th, and 14th level."),
    (5, "Wild Shape Improvement", 4, "You can transform into a beast with a challenge "
    "rating as high as 1/2 (no flying speed)."),
    (5, "Ability Score Improvement", 4, "When you reach 4th level, and again at 8th, 12th, "
    "16th, and 19th level, you can increase one ability score of your choice by 2, or "
    "you can increase two ability scores of your choice by 1. As normal, you can't "
    "increase an ability score above 20 using this feature."),
    (5, "Druid Circle", 6, "Feature of your chosen Circle"),
    (5, "Ability Score Improvement", 8, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (5, "Wild Shape Improvement", 8, "You can transform into a beast with a challenge "
    "rating as high as 1 (no flying speed)."),
    (5, "Druid Circle", 10, "Feature of your chosen Circle"),
    (5, "Ability Score Improvement", 12, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (5, "Druid Circle", 14, "Feature of your chosen Circle"),
    (5, "Ability Score Improvement", 16, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (5, "Timeless Body", 18, "Starting at 18th level, the primal magic that you wield causes "
    "you to age more slowly. For every 10 years that pass, your body ages only 1 year."),
    (5, "Beast Spells", 18, "Beginning at 18th level, you can cast many of your druid spells "
    "in any shape you assume using Wild Shape. You can perform the somatic and verbal components of "
    "a druid spell while in a beast shape, but you aren't able to provide material components."),
    (5, "Ability Score Improvement", 19, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1."),
    (5, "Archdruid", 20, "At 20th level, you can use your Wild Shape an unlimited number of times.\nAdditionally, "
    "you can ignore the verbal and somatic components of your druid spells, as well as any material components "
    "that lack a cost and aren't consumed by a spell. You gain this benefit in both your normal shape "
    "and your beast shape from Wild Shape."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', druid_features)

fighter_features = [
    (6, "Fighting Style", 1, "You adopt a particular style of fighting as your "
    "specialty. Choose one of the following options. You can't take a Fighting "
    "Style option more than once, even if you later get to choose again.\n\t" + chr(9679) +
    "Archery. You gain a +2 bonus to attack rolls you make with ranged weapons.\n\t" + chr(9679) +
    "Blind Fighting. You have blindsight with a range of 10 feet. Within that range, you can "
    "effectively see anything that isn't behind total cover, even if you're blinded or "
    "in darkness. Moreover, you can see an invisible creature within that range, "
    "unless the creature successfully hides from you.\n\t" + chr(9679) + "Defense. "
    "While you are wearing armor, you gain a +1 bonus to AC.\n\t" + chr(9679) + "Dueling. "
    "When you are wielding a melee weapon in one hand and no other weapons, you gain a "
    "+2 bonus to damage rolls with that weapon.\n\t" + chr(9679) + "Great Weapon Fighting. "
    "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon "
    "that you are wielding with two hands, you can reroll the die and must use the new "
    "roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed "
    "or versatile property for you to gain this benefit.\n\t" + chr(9679) + "Interception. "
    "When a creature you can see hits a target, other than you, within 5 feet of you "
    "with an attack, you can use your reaction to reduce the damage the target takes "
    "by 1d10 + your proficiency bonus (to a minimum of 0 damage). You must be wielding "
    "a shield or a simple or martial weapon to use this reaction.\n\t" + chr(9679) + "Protection. "
    "When a creature you can see attacks a target other than you that is within 5 feet of you, "
    "you can use your reaction to impose disadvantage on the attack roll. You must be "
    "wielding a shield.\n\t" + chr(9679) + "Superior Technique. You learn one maneuver "
    "of your choice from among those available to the Battle Master archetype. If a maneuver "
    "you use requires your target to make a saving throw to resist the maneuver's effects, "
    "the saving throw DC equals 8 + your proficiency bonus + your Strength or Dexterity "
    "modifier (your choice.)\n\t\t" + chr(9679) + "You gain one superiority die, which "
    "is a d6 (this die is added to any superiority dice you have from another source). "
    "This die is used to fuel your maneuvers. A superiority die is expended when you use "
    "it. You regain your expended superiority dice when you finish a short or long rest."
    "\n\t" + chr(9679) + "Thrown Weapon Fighting. You can draw a weapon that has the "
    "thrown property as part of the attack you make with the weapon.\n\t\t" + chr(9679) + "In "
    "addition, when you hit with a ranged attack using a thrown weapon, you gain a +2 "
    "bonus to the damage roll.\n\t" + chr(9679) + "Two-Weapon Fighting. When you engage "
    "in two-weapon fighting, you can add your ability modifier to the damage of the "
    "second attack.\n\t" + chr(9679) + "Unarmed Fighting. Your unarmed strikes can "
    "deal bludgeoning damage equal to 1d6 + your Strength modifier on a hit. If "
    "you aren't wielding any weapons or a shield when you make the attack roll, "
    "the d6 becomes a d8.\n\t\t" + chr(9679) + "At the start of each of your "
    "turns, you can deal 1d4 bludgeoning damage to one creature grappled by "
    "you."),
    (6, "Second Wind", 1, "You have a limited well of stamina that you can draw on "
    "to protect yourself from harm. On your turn, you can use a bonus action to "
    "regain hit points equal to 1d10 + your fighter level.\n\nOnce you use this "
    "feature, you must finish a short or long rest before you can use it again."),
    (6, "Action Surge", 2, "Starting at 2nd level, you can push yourself "
    "beyond your normal limits for a moment. On your turn, you can take one "
    "additional action.\n\nOnce you use this feature, you must finish a short "
    "or long rest before you can use it again. Starting at 17th level, you "
    "can use it twice before a rest, but only once on the same turn."),
    (6, "Martial Archetype", 3, "At 3rd level, you choose an archetype that you strive "
    "to emulate in your combat styles and techniques. The archetype you choose grants "
    "you features at 3rd level and again at 7th, 10th, 15th, and 18th level."),
    (6, "Ability Score Improvement", 4, "When you reach 4th level, and again at "
    "6th, 8th, 12th, 14th, 16th, and 19th level, you can increase one ability "
    "score of your choice by 2, or you can increase two ability scores of "
    "your choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (6, "Extra Attack", 5, "Beginning at 5th level, you can attack twice, "
    "instead of once, whenever you take the Attack action on your turn. \nThe "
    "number of attacks increases to three when you reach 11th level in this "
    "class and to four when you reach 20th level in this class."),
    (6, "Ability Score Improvement", 6, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Martial Archetype Feature", 7, "Feature from your chosen Martial Archetype."),
    (6, "Ability Score Improvement", 8, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Indomitable", 9, "Beginning at 9th level, you can reroll a "
    "saving throw that you fail. If you do so, you must use the new roll, "
    "and you can't use this feature again until you finish a long rest.\n\nYou "
    "can use this feature twice between long rests starting at 13th level "
    "and three times between long rests starting at 17th level."),
    (6, "Martial Archetype Feature", 10, "Feature from your chosen Martial Archetype."),
    (6, "Extra Attack (2)", 11, "You can attack three times whenever you take "
    "the Attack action on your turn."),
    (6, "Ability Score Improvement", 12, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Indomitable (2 uses)", 13, "You can reroll a saving throw that you "
    "fail twice per long rest."),
    (6, "Ability Score Improvement", 14, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Martial Archetype Feature", 15, "Feature from your chosen Martial Archetype."),
    (6, "Ability Score Improvement", 16, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Action Surge (2 uses)", 17, "You can use Action Surge twice per short "
    "or long rest."),
    (6, "Indomitable (3 uses)", 17, "You can reroll a saving throw that you "
    "fail three times per long rest."),
    (6, "Martial Archetype Feature", 18, "Feature from your chosen Martial Archetype."),
    (6, "Ability Score Improvement", 19, "You can increase one ability score of your "
    "choice by 2, or you can increase two ability scores of your choice by 1. As "
    "normal, you can't increase an ability score above 20 using this feature."),
    (6, "Extra Attack (3)", 20, "You can attack four times whenever you take "
    "the Attack action on your turn.")
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', fighter_features)



monk_features = [
    (7, "Unarmored Defense", 1, "Beginning at 1st level, while you are wearing no armor "
    "and not wielding a shield, your AC equals 10 + your Dexterity modifier + your Wisdom modifier."),
    (7, "Martial Arts", 1, "At 1st level, your practice of martial arts gives you mastery of "
    "combat styles that use unarmed strikes and monk weapons, which are shortswords and any "
    "simple melee weapons that don't have the two-handed or heavy property.\n\nYou gain the "
    "following benefits while you are unarmed or wielding only monk weapons and you aren't "
    "wearing armor or wielding a shield:\n\t" + chr(9679) + "You can use Dexterity instead "
    "of Strength for the attack and damage rolls of your unarmed strikes and monk weapons.\n\t"
    + chr(9679) + "You can roll a d4 in place of the normal damage of your unarmed strike "
    "or monk weapon. This die changes as you gain monk levels, as shown in the Martial Arts "
    "column of the Monk table.\n\t" + chr(9679) + "When you use the Attack action with an "
    "unarmed strike or a monk weapon on your turn, you can make one unarmed strike as a "
    "bonus action. For example, if you take the Attack action and attack with a "
    "quarterstaff, you can also make an unarmed strike as a bonus action, assuming you "
    "haven't already taken a bonus action this turn.\n\nCertain monasteries use specialized "
    "forms of the monk weapons. For example, you might use a club that is two lengths of "
    "wood connected by a short chain (called a nunchaku) or a sickle with a shorter, "
    "straighter blade (called a kama). Whatever name you use for a monk weapon, you can "
    "use the game statistics provided for the weapon on the Weapons page."),
    (7, "Ki", 2, "Starting at 2nd level, your training allows you to harness the mystic "
    "energy of ki. Your access to this energy is represented by a number of ki points. Your "
    "monk level determines the number of points you have, as shown in the Ki Points "
    "column of the Monk table.\n\nYou can spend these points to fuel various ki features. "
    "You start knowing three such features: Flurry of Blows, Patient Defense, and Step "
    "of the Wind. You learn more ki features as you gain levels in this class.\n\nWhen "
    "you spend a ki point, it is unavailable until you finish a short or long rest, at "
    "the end of which you draw all of your expended ki back into yourself. You must spend at "
    "least 30 minutes of the rest meditating to regain your ki points.\n\nSome of your ki "
    "features require your target to make a saving throw to resist the feature's effects. "
    "The saving throw DC is calculated as follows:\n\tKi save DC = 8 + your proficiency "
    "bonus + your Wisdom modifier\n\t" + chr(9679) + "Flurry of Blows. Immediately after "
    "you take the Attack action on your turn, you can spend 1 ki point to make two "
    "unarmed strikes as a bonus action.\n\t" + chr(9679) + "Patient Defense. You can "
    "spend 1 ki point to take the Dodge action as a bonus action on your turn.\n\t" + chr(9679)
    + "Step of the Wind. You can spend 1 ki point to take the Disengage or Dash action "
    "as a bonus action on your turn, and your jump distance is doubled for the turn."),
    (7, "Unarmored Movement", 2, "Starting at 2nd level, your speed increases by 10 feet "
    "while you are not wearing armor or wielding a shield. This bonus increases when you "
    "reach certain monk levels, as shown in the Monk table.\n\nAt 9th level, you gain "
    "the ability to move along vertical surfaces and across liquids on your turn "
    "without falling during the move."),
    (7, "Monastic Tradition", 3, "When you reach 3rd level, you commit yourself to a "
    "monastic tradition. Your tradition grants you features at 3rd level and again "
    "at 6th, 11th, and 17th level."),
    (7, "Deflect Missiles", 3, "Starting at 3rd level, you can use your reaction to "
    "deflect or catch the missile when you are hit by a ranged weapon attack. When "
    "you do so, the damage you take from the attack is reduced by 1d10 + your Dexterity "
    "modifier + your monk level.\n\nIf you reduce the damage to 0, you can catch "
    "the missile if it is small enough for you to hold in one hand and you have at "
    "least one hand free. If you catch a missile in this way, you can spend 1 ki point "
    "to make a ranged attack with a range of 20/60 using the weapon or piece of ammunition "
    "you just caught, as part of the same reaction. You make this attack with "
    "proficiency, regardless of your weapon proficiencies, and the missile counts as "
    "a monk weapon for the attack."),
    (7, "Ability Score Improvement", 4, "When you reach 4th level, and again at 8th, "
    "12th, 16th, and 19th level, you can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (7, "Slow Fall", 4, "Beginning at 4th level, you can use your reaction when you "
    "fall to reduce any falling damage you take by an amount equal to five times your monk level."),
    (7, "Extra Attack", 5, "Beginning at 5th level, you can attack twice, instead of once, "
    "whenever you take the Attack action on your turn."),
    (7, "Stunning Strike", 5, "Starting at 5th level, you can interfere with the flow "
    "of ki in an opponent's body. When you hit another creature with a melee weapon "
    "attack, you can spend 1 ki point to attempt a stunning strike. The target must "
    "succeed on a Constitution saving throw or be stunned until the end of your next turn."),
    (7, "Ki-Empowered Strikes", 6, "Starting at 6th level, your unarmed strikes count "
    "as magical for the purpose of overcoming resistance and immunity to nonmagical "
    "attacks and damage."),
    (7, "Monastic Tradition", 6, "Feature from your chosen Tradition."),
    (7, "Evasion", 7, "At 7th level, your instinctive agility lets you dodge out of "
    "the way of certain area effects, such as a blue dragon's lightning breath or a "
    "fireball spell. When you are subjected to an effect that allows you to make a "
    "Dexterity saving throw to take only half damage, you instead take no damage if "
    "you succeed on the saving throw, and only half damage if you fail."),
    (7, "Stillness of Mind", 7, "Starting at 7th level, you can use your action to "
    "end one effect on yourself that is causing you to be charmed or frightened."),
    (7, "Ability Score Improvement", 8, "You can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (7, "Unarmored Movement Improvement", 9, "You gain the ability to move along "
    "vertical surfaces and across liquids on your turn without falling during "
    "the move."),
    (7, "Purity of Body", 10, "At 10th level, your mastery of the ki flowing through "
    "you makes you immune to disease and poison."),
    (7, "Monastic Tradition", 11, "Feature from your chosen Tradition."),
    (7, "Ability Score Improvement", 12, "You can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (7, "Tongue of the Sun and Moon", 13, "Starting at 13th level, you learn to "
    "touch the ki of other minds so that you understand all spoken languages. Moreover, "
    "any creature that can understand a language can understand what you say."),
    (7, "Diamond Soul", 14, "Beginning at 14th level, your mastery of ki grants you "
    "proficiency in all saving throws.\n\nAdditionally, whenever you make a "
    "saving throw and fail, you can spend 1 ki point to reroll it and take the second result."),
    (7, "Timeless Body", 15, "At 15th level, your ki sustains you so that you suffer none "
    "of the frailty of old age, and you can't be aged magically. You can still die "
    "of old age, however. In addition, you no longer need food or water."),
    (7, "Ability Score Improvement", 16, "You can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (7, "Monastic Tradition", 17, "Feature from your chosen Tradition."),
    (7, "Empty Body", 18, "Beginning at 18th level, you can use your action to spend "
    "4 ki points to become invisible for 1 minute. During that time, you also have "
    "resistance to all damage but force damage.\n\nAdditionally, you can spend 8 "
    "ki points to cast the astral projection spell, without needing material "
    "components. When you do so, you can't take any other creatures with you."),
    (7, "Ability Score Improvement", 19, "You can increase one ability score of your choice "
    "by 2, or you can increase two ability scores of your choice by 1. As normal, you "
    "can't increase an ability score above 20 using this feature."),
    (7, "Perfect Self", 20, "At 20th level, when you roll for initiative and "
    "have no ki points remaining, you regain 4 ki points."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', monk_features)

paladin_features = [
    (8, "Divine Sense", 1, "The presence of strong evil registers on your senses like a noxious "
    "odor, and powerful good rings like heavenly music in your ears. As an action, you can "
    "open your awareness to detect such forces. Until the end of your next turn, you know "
    "the location of any celestial, fiend, or undead within 60 feet of you that is not "
    "behind total cover. You know the type (celestial, fiend, or undead) of any being "
    "whose presence you sense, but not its identity (the vampire Count Strahd von "
    "Zarovich, for instance). Within the same radius, you also detect the presence "
    "of any place or object that has been consecrated or desecrated, as with the "
    "Hallow spell.\n\nYou can use this feature a number of times equal to 1 + your "
    "Charisma modifier. When you finish a long rest, you regain all expended uses."),
    (8, "Lay on Hands", 1, "Your blessed touch can heal wounds. You have a pool of "
    "healing power that replenishes when you take a long rest. With that pool, you "
    "can restore a total number of hit points equal to your paladin level x 5.\n\nAs "
    "an action, you can touch a creature and draw power from the pool to restore a "
    "number of hit points to that creature, up to the maximum amount remaining in "
    "your pool.\n\nAlternatively, you can expend 5 hit points from your pool of "
    "healing to cure the target of one disease or neutralize one poison affecting "
    "it. You can cure multiple diseases and neutralize multiple poisons with a "
    "single use of Lay on Hands, expending hit points separately for each one.\n\n"
    "This feature has no effect on undead and constructs."),
    (8, "Fighting Style", 2, "Starting at 2nd level, you adopt a particular style "
    "of fighting as your specialty. Choose one of the following options. You "
    "can't take a Fighting Style option more than once, even if you later get "
    "to choose again.\n\t" + chr(9679) + "Blessed Warrior. You learn two cantrips "
    "of your choice from the cleric spell list. They count as paladin spells "
    "for you, and Charisma is your spellcasting ability for them. Whenever you "
    "gain a level in this class, you can replace one of these cantrips with "
    "another cantrip from the cleric spell list.\n\t" + chr(9679) + "Blind Fighting. "
    "You have blindsight with a range of 10 feet. Within that range, you can "
    "effectively see anything that isn't behind total cover, even if you're "
    "blinded or in darkness. Moreover, you can see an invisible creature within "
    "that range, unless the creature successfully hides from you.\n\t" + chr(9679) + 
    "Defense. While you are wearing armor, you gain a +1 bonus to AC.\n\t" + chr(9679)
    + "Dueling. When you are wielding a melee weapon in one hand and no other "
    "weapons, you gain a +2 bonus to damage rolls with that weapon.\n\t" + chr(9679) +
    "Great Weapon Fighting. When you roll a 1 or 2 on a damage die for an attack "
    "you make with a melee weapon that you are wielding with two hands, you "
    "can reroll the die and must use the new roll, even if the new roll is a "
    "1 or a 2. The weapon must have the two-handed or versatile property for "
    "you to gain this benefit.\n\t" + chr(9679) + "Interception. When a creature "
    "you can see hits a target, other than you, within 5 feet of you with an "
    "attack, you can use your reaction to reduce the damage the target takes "
    "by 1d10 + your proficiency bonus (to a minimum of 0 damage). You must "
    "be wielding a shield or a simple or martial weapon to use this reaction.\n\t"
    + chr(9679) + "Protection. When a creature you can see attacks a target "
    "other than you that is within 5 feet of you, you can use your reaction "
    "to impose disadvantage on the attack roll. You must be wielding a shield."),
    (8, "Spellcasting", 2, "By 2nd level, you have learned to draw on divine "
    "magic through meditation and prayer to cast spells as a cleric does.\n\nPreparing "
    "and Casting Spells\n\nThe Paladin table shows how many spell slots you have "
    "to cast your paladin spells. To cast one of your paladin spells of 1st "
    "level or higher, you must expend a slot of the spell's level or higher. "
    "You regain all expended spell slots when you finish a long rest.\n\nYou "
    "prepare the list of paladin spells that are available for you to cast, "
    "choosing from the paladin spell list. When you do so, choose a number "
    "of paladin spells equal to your Charisma modifier + half your paladin "
    "level, rounded down (minimum of one spell). The spells must be of a "
    "level for which you have spell slots.\n\nFor example, if you are a "
    "5th-level paladin, you have four 1st-level and two 2nd-level spell "
    "slots. With a Charisma of 14, your list of prepared spells can include "
    "four spells of 1st or 2nd level, in any combination. If you prepare "
    "the 1st-level spell Cure Wounds, you can cast it using a 1st-level "
    "or a 2nd-level slot. Casting the spell doesn't remove it from your "
    "list of prepared spells.\n\nYou can change your list of prepared "
    "spells when you finish a long rest. Preparing a new list of paladin "
    "spells requires time spent in prayer and meditation: at least 1 minute "
    "per spell level for each spell on your list.\n\nSpellcasting Ability\n\n"
    "Charisma is your spellcasting ability for your paladin spells, since "
    "their power derives from the strength of your convictions. You use your "
    "Charisma whenever a spell refers to your spellcasting ability. In "
    "addition, you use your Charisma modifier when setting the saving "
    "throw DC for a paladin spell you cast and when making an attack roll "
    "with one.\n\tSpell save DC = 8 + your proficiency bonus + your "
    "Charisma modifier\n\tSpell attack modifier = your proficiency bonus "
    "+ your Charisma modifier\n\nSpellcasting Focus\n\nYou can use a holy "
    "symbol as a spellcasting focus for your paladin spells."),
    (8, "Divine Smite", 2, "Starting at 2nd level, when you hit a creature "
    "with a melee weapon attack, you can expend one spell slot to deal "
    "radiant damage to the target, in addition to the weapon's damage. The "
    "extra damage is 2d8 for a 1st-level spell slot, plus 1d8 for each "
    "spell level higher than 1st, to a maximum of 5d8. The damage increases "
    "by 1d8 if the target is an undead or a fiend, to a maximum of 6d8."),
    (8, "Divine Health", 3, "By 3rd level, the divine magic flowing through "
    "you makes you immune to disease."),
    (8, "Sacred Oath", 3, "When you reach 3rd level, you swear the oath "
    "that binds you as a paladin forever. Up to this time you have been "
    "in a preparatory stage, committed to the path but not yet sworn to "
    "it. Your choice grants you features at 3rd level and again at 7th, "
    "15th, and 20th level. Those features include oath spells and the "
    "Channel Divinity feature.\n\nOath Spells\n\nEach oath has a list of "
    "associated spells. You gain access to these spells at the levels "
    "specified in the oath description. Once you gain access to an oath "
    "spell, you always have it prepared. Oath spells don't count against "
    "the number of spells you can prepare each day.\n\nIf you gain an "
    "oath spell that doesn't appear on the paladin spell list, the spell "
    "is nonetheless a paladin spell for you.\n\nChannel Divinity\n\nYour "
    "oath allows you to channel divine energy to fuel magical effects. Each "
    "Channel Divinity option provided by your oath explains how to use "
    "it.\n\nWhen you use your Channel Divinity, you choose which option "
    "to use. You must then finish a short or long rest to use your "
    "Channel Divinity again.\n\nSome Channel Divinity effects require saving "
    "throws. When you use such an effect from this class, the DC equals "
    "your paladin spell save DC."),
    (8, "Ability Score Improvement", 4, "When you reach 4th level, and again "
    "at 8th, 12th, 16th, and 19th level, you can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (8, "Extra Attack", 5, "Beginning at 5th level, you can attack "
    "twice, instead of once, whenever you take the Attack action on your turn."),
    (8, "Aura of Protection", 6, "Starting at 6th level, whenever you or a "
    "friendly creature within 10 feet of you must make a saving throw, the "
    "creature gains a bonus to the saving throw equal to your Charisma modifier "
    "(with a minimum bonus of +1). You must be conscious to grant this bonus.\n\n"
    "At 18th level, the range of this aura increases to 30 feet."),
    (8, "Sacred Oath", 7, "Feature from your chosen Sacred Oath."),
    (8, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (8, "Aura of Courage", 10, "Starting at 10th level, you and friendly "
    "creatures within 10 feet of you can't be frightened while you are "
    "conscious.\n\nAt 18th level, the range of this aura increases to 30 feet."),
    (8, "Improved Divine Smite", 11, "By 11th level, you are so suffused "
    "with righteous might that all your melee weapon strikes carry divine "
    "power with them. Whenever you hit a creature with a melee weapon, the "
    "creature takes an extra 1d8 radiant damage."),
    (8, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (8, "Cleansing Touch", 14, "Beginning at 14th level, you can use your "
    "action to end one spell on yourself or on one willing creature that "
    "you touch.\n\nYou can use this feature a number of times equal to "
    "your Charisma modifier (a minimum of once). You regain expended uses "
    "when you finish a long rest."),
    (8, "Sacred Oath", 15, "Feature from your chosen Sacred Oath."),
    (8, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (8, "Aura Improvements", 18, "Your auras now affect friendly creatures "
    "within 30 feet of you, rather than 10 feet."),
    (8, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (8, "Sacred Oath", 20, "Feature from your chosen Sacred Oath."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', paladin_features)


ranger_features = [
    (9, "Favored Enemy", 1, "Beginning at 1st level, you have significant experience "
    "studying, tracking, hunting, and even talking to a certain type of enemy.\n\nChoose "
    "a type of favored enemy: aberrations, beasts, celestials, constructs, dragons, "
    "elementals, fey, fiends, giants, monstrosities, oozes, plants, or undead. "
    "Alternatively, you can select two races of humanoid (such as gnolls and orcs) "
    "as favored enemies.\n\nYou have advantage on Wisdom (Survival) checks to "
    "track your favored enemies, as well as on Intelligence checks to recall "
    "information about them.\n\nWhen you gain this feature, you also learn one "
    "language of your choice that is spoken by your favored enemies, if they "
    "speak one at all.\n\nYou choose one additional favored enemy, as well "
    "as an associated language, at 6th and 14th level. As you gain levels, "
    "your choices should reflect the types of monsters you have encountered "
    "on your adventures."),
    (9, "Natural Explorer", 1, "Also at 1st level, you are particularly familiar "
    "with one type of natural environment and are adept at traveling and "
    "surviving in such regions. Choose one type of favored terrain: arctic, coast, "
    "desert, forest, grassland, mountain, swamp, or the Underdark. When you "
    "make an Intelligence or Wisdom check related to your favored terrain, "
    "your proficiency bonus is doubled if you are using a skill that you’re "
    "proficient in.\n\nWhile traveling for an hour or more in your favored "
    "terrain, you gain the following benefits:\n\t" + chr(9679) + "Difficult "
    "terrain doesn’t slow your group’s travel.\n\t" + chr(9679) + "Your group "
    "can’t become lost except by magical means.\n\t" + chr(9679) + "Even when "
    "you are engaged in another activity while traveling (such as foraging, "
    "navigating, or tracking), you remain alert to danger.\n\t" + chr(9679) + "If "
    "you are traveling alone, you can move stealthily at a normal pace.\n\t" + chr(9679) + 
    "When you forage, you find twice as much food as you normally would.\n\t"
    + chr(9679) + "While tracking other creatures, you also learn their exact "
    "number, their sizes, and how long ago they passed through the area.\n\nYou "
    "choose additional favored terrain types at 6th and 10th level."),
    (9, "Fighting Style", 2, "At 2nd level, you adopt a particular style of "
    "fighting as your specialty. Choose one of the following options. You "
    "can't take a Fighting Style option more than once, even if you later "
    "get to choose again.\n\t" + chr(9679) + "Archery. You gain a +2 "
    "bonus to attack rolls you make with ranged weapons.\n\t" + chr(9679) +
    "Blind Fighting. You have blind sight with a range of 10 feet. Within that "
    "range, you can effectively see anything that isn't behind total cover, "
    "even if you're blinded or in darkness. Moreover, you can see an invisible "
    "creature within that range, unless the creature successfully hides from you.\n\t"
    + chr(9679) + "Defense. While you are wearing armor, you gain a +1 bonus to "
    "AC.\n\t" + chr(9679) + "Druidic Warrior. You learn two cantrips of your "
    "choice from the Druid spell list. They count as ranger spells for you, "
    "and Wisdom is your spellcasting ability for them. Whenever you gain a "
    "level in this class, you can replace one of these cantrips with "
    "another cantrip from the Druid spell list.\n\t" + chr(9679) + "Dueling. "
    "When you are wielding a melee weapon in one hand and no other weapons, "
    "you gain a +2 bonus to damage rolls with that weapon.\n\t" + chr(9679) +
    "Thrown Weapon Fighting. You can draw a weapon that has the thrown "
    "property as part of the attack you make with the weapon.\n\t\t" + chr(9679) +
    "In addition, when you hit with a ranged attack using a thrown weapon, you "
    "gain a +2 bonus to the damage roll.\n\t" + chr(9679) + "Two-Weapon Fighting. "
    "When you engage in two-weapon fighting, you can add your ability modifier "
    "to the damage of the second attack."),
    (9, "Spellcasting", 2, "By the time you reach 2nd level, you have learned "
    "to use the magical essence of nature to cast spells, much as a druid "
    "does.\n\nSpell Slots\n\nThe Ranger table shows how many spell slots "
    "you have to cast your ranger spells of 1st level and higher. To cast "
    "one of these spells, you must expend a slot of the spell's level or "
    "higher. You regain all expended spell slots when you finish a long "
    "rest.\n\nFor example, if you know the 1st-level spell Animal Friendship "
    "and have a 1st-level and a 2nd-level spell slot available, you can "
    "cast Animal Friendship using either slot.\n\nSpells Known of 1st "
    "Level and Higher\n\nYou know two 1st-level spells of your choice "
    "from the ranger spell list.\n\nThe Spells Known column of the "
    "Ranger table shows when you learn more ranger spells of your "
    "choice. Each of these spells must be of a level for which you have "
    "spell slots. For instance, when you reach 5th level in this "
    "class, you can learn one new spell of 1st or 2nd level.\n\nAdditionally, "
    "when you gain a level in this class, you can choose one of the "
    "ranger spells you know and replace it with another spell from "
    "the ranger spell list, which also must be of a level for which "
    "you have spell slots.\n\nSpellcasting Ability\n\nWisdom is your "
    "spellcasting ability for your ranger spells, since your magic "
    "draws on your attunement to nature. You use your Wisdom whenever "
    "a spell refers to your spellcasting ability. In addition, you "
    "use your Wisdom modifier when setting the saving throw DC for "
    "a ranger spell you cast and when making an attack roll with one.\n\t"
    "Spell save DC = 8 + your proficiency bonus + your Wisdom modifier\n\t"
    "Spell attack modifier = your proficiency bonus + your Wisdom modifier"),
    (9, "Primeval Awareness", 3, "Beginning at 3rd level, you can use your "
    "action and expend one ranger spell slot to focus your awareness on "
    "the region around you. For 1 minute per level of the spell slot you "
    "expend, you can sense whether the following types of creatures are "
    "present within 1 mile of you (or within up to 6 miles if you are "
    "in your favored terrain): aberrations, celestials, dragons, elementals, "
    "fey, fiends, and undead. This feature doesn’t reveal the creatures’ "
    "location or number."),
    (9, "Ranger Conclave", 3, "At 3rd level, you choose to emulate the "
    "ideals and training of a ranger conclave. Your choice grants you "
    "features at 3rd level and again at 7th, 11th, and 15th level."),
    (9, "Ability Score Improvement", 4, "When you reach 4th level, and again "
    "at 8th, 12th, 16th, and 19th level, you can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (9, "Extra Attack", 5, "Beginning at 5th level, you can attack twice, "
    "instead of once, whenever you take the Attack action on your turn."),
    (9, "Favored Enemy Improvement", 6, "You choose one additional favored "
    "enemy, as well as an associated language."),
    (9, "Natural Explorer Improvement", 6, "You choose additional favored "
    "terrain types"),
    (9, "Ranger Conclave", 7, "Feature from chosen Conclave."),
    (9, "Land's Stride", 8, "Starting at 8th level, moving through nonmagical "
    "difficult terrain costs you no extra movement. You can also pass "
    "through nonmagical plants without being slowed by them and without "
    "taking damage from them if they have thorns, spines, or a similar "
    "hazard.\n\nIn addition, you have advantage on saving throws against "
    "plants that are magically created or manipulated to impede movement, "
    "such as those created by the Entangle spell."),
    (9, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (9, "Natural Explorer Improvement", 10, "You choose additional favored "
    "terrain types"),
    (9, "Hide in Plain Sight", 10, "Starting at 10th level, you can spend "
    "1 minute creating camouflage for yourself. You must have access to "
    "fresh mud, dirt, plants, soot, and other naturally occurring materials "
    "with which to create your camouflage.\n\nOnce you are camouflaged in "
    "this way, you can try to hide by pressing yourself up against a solid "
    "surface, such as a tree or wall, that is at least as tall and wide "
    "as you are. You gain a +10 bonus to Dexterity (Stealth) checks as "
    "long as you remain there without moving or taking actions. Once you "
    "move or take an action or a reaction, you must camouflage yourself "
    "again to gain this benefit."),
    (9, "Ranger Conclave", 11, "Feature from chosen Conclave."),
    (9, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (9, "Favored Enemy Improvement", 14, "You choose one additional favored "
    "enemy, as well as an associated language."),
    (9, "Vanish", 14, "Starting at 14th level, you can use the Hide action "
    "as a bonus action on your turn. Also, you can't be tracked by "
    "nonmagical means, unless you choose to leave a trail."),
    (9, "Ranger Conclave", 15, "Feature from chosen Conclave."),
    (9, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (9, "Feral Senses", 18, "At 18th level, you gain preternatural senses "
    "that help you fight creatures you can't see. When you attack a "
    "creature you can't see, your inability to see it doesn't impose "
    "disadvantage on your attack rolls against it.\n\nYou are also aware "
    "of the location of any invisible creature within 30 feet of you, "
    "provided that the creature isn't hidden from you and you aren't "
    "blinded or deafened."),
    (9, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (9, "Foe Slayer", 20, "At 20th level, you become an unparalleled hunter "
    "of your enemies. Once on each of your turns, you can add your Wisdom "
    "modifier to the attack roll or the damage roll of an attack you make "
    "against one of your favored enemies. You can choose to use this "
    "feature before or after the roll, but before any effects of the roll "
    "are applied."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', ranger_features)

rogue_features = [
    (10, "Expertise", 1, "At 1st level, choose two of your skill proficiencies, "
    "or one of your skill proficiencies and your proficiency with thieves' "
    "tools. Your proficiency bonus is doubled for any ability check you make "
    "that uses either of the chosen proficiencies.\n\nAt 6th level, you can "
    "choose two more of your proficiencies (in skills or with thieves' tools) "
    "to gain this benefit."),
    (10, "Sneak Attack", 1, "Beginning at 1st level, you know how to strike "
    "subtly and exploit a foe's distraction. Once per turn, you can deal an "
    "extra 1d6 damage to one creature you hit with an attack if you have "
    "advantage on the attack roll. The attack must use a finesse or a ranged "
    "weapon.\n\nYou don't need advantage on the attack roll if another enemy "
    "of the target is within 5 feet of it, that enemy isn't incapacitated, "
    "and you don't have disadvantage on the attack roll.\n\nThe amount of "
    "the extra damage increases as you gain levels in this class, as shown "
    "in the Sneak Attack column of the Rogue table."),
    (10, "Thieves' Cant", 1, "During your rogue training you learned thieves' "
    "cant, a secret mix of dialect, jargon, and code that allows you to "
    "hide messages in seemingly normal conversation. Only another creature "
    "that knows thieves' cant understands such messages. It takes four "
    "times longer to convey such a message than it does to speak the "
    "same idea plainly.\n\nIn addition, you understand a set of secret "
    "signs and symbols used to convey short, simple messages, such as "
    "whether an area is dangerous or the territory of a thieves' guild, "
    "whether loot is nearby, or whether the people in an area are easy "
    "marks or will provide a safe house for thieves on the run."),
    (10, "Cunning Action", 2, "Starting at 2nd level, your quick thinking "
    "and agility allow you to move and act quickly. You can take a bonus "
    "action on each of your turns in combat. This action can be used "
    "only to take the Dash, Disengage, or Hide action."),
    (10, "Roguish Archetype", 3, "At 3rd level, you choose an archetype "
    "that you emulate in the exercise of your rogue abilities. Your "
    "archetype choice grants you features at 3rd level and then again "
    "at 9th, 13th, and 17th level."),
    (10, "Ability Score Improvement", 4, "When you reach 4th level, and "
    "again at 8th, 10th, 12th, 16th, and 19th level, you can increase "
    "one ability score of your choice by 2, or you can increase two "
    "ability scores of your choice by 1. As normal, you can't increase "
    "an ability score above 20 using this feature."),
    (10, "Uncanny Dodge", 5, "Starting at 5th level, when an attacker "
    "that you can see hits you with an attack, you can use your reaction "
    "to halve the attack's damage against you."),
    (10, "Expertise", 6, "Choose two more of your proficiencies in skills"
    "or your proficiency with thieves' tools. Your proficiency bonus is doubled for any"
    "ability check you make that uses either of the chosen proficiencies."),
    (10, "Evasion", 7, "Beginning at 7th level, you can nimbly dodge out "
    "of the way of certain area effects, such as a red dragon's fiery "
    "breath or an Ice Storm spell. When you are subjected to an effect "
    "that allows you to make a Dexterity saving throw to take only half "
    "damage, you instead take no damage if you succeed on the saving "
    "throw, and only half damage if you fail."),
    (10, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (10, "Roguish Archetype", 9, "Feature of chosen Archetype."),
    (10, "Ability Score Improvement", 10, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (10, "Reliable Talent", 11, "By 11th level, you have refined your "
    "chosen skills until they approach perfection. Whenever you make an "
    "ability check that lets you add your proficiency bonus, you can "
    "treat a d20 roll of 9 or lower as a 10."),
    (10, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (10, "Roguish Archetype", 13, "Feature of chosen Archetype."),
    (10, "Blindsense", 14, "Starting at 14th level, if you are able to "
    "hear, you are aware of the location of any hidden or invisible "
    "creature within 10 feet of you."),
    (10, "Slippery Mind", 15, "By 15th level, you have acquired greater "
    "mental strength. You gain proficiency in Wisdom saving throws."),
    (10, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (10, "Roguish Archetype", 17, "Feature of chosen Archetype."),
    (10, "Elusive", 18, "Beginning at 18th level, you are so evasive "
    "that attackers rarely gain the upper hand against you. No attack "
    "roll has advantage against you while you aren't incapacitated."),
    (10, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (10, "Stroke of Luck", 20, "At 20th level, you have an uncanny knack "
    "for succeeding when you need to. If your attack misses a target "
    "within range, you can turn the miss into a hit. Alternatively, if "
    "you fail an ability check, you can treat the d20 roll as a 20.\n\nOnce "
    "you use this feature, you can't use it again until you finish a "
    "short or long rest.")
]
c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', rogue_features)


sorcerer_features = [
    (11, "Spellcasting", 1, "An event in your past, or in the life of "
    "a parent or ancestor, left an indelible mark on you, infusing you "
    "with arcane magic. This font of magic, whatever its origin, fuels "
    "your spells.\n\nCantrips\n\nAt 1st level, you know four cantrips "
    "of your choice from the sorcerer spell list. You learn additional "
    "sorcerer cantrips of your choice at higher levels, as shown in "
    "the Cantrips Known column of the Sorcerer table.\n\nSpell Slots\n\nThe "
    "Sorcerer table shows how many spell slots you have to cast your "
    "sorcerer spells of 1st level and higher. To cast one of these "
    "sorcerer spells, you must expend a slot of the spell's level or "
    "higher. You regain all expended spell slots when you finish a "
    "long rest.\n\nFor example, if you know the 1st-level spell burning "
    "hands and have a 1st-level and a 2nd-level spell slot available, "
    "you can cast burning hands using either slot.\n\nSpells Known of "
    "1st Level and Higher\n\nYou know two 1st-level spells of your "
    "choice from the sorcerer spell list.\n\nThe Spells Known column "
    "of the Sorcerer table shows when you learn more sorcerer spells "
    "of your choice. Each of these spells must be of a level for "
    "which you have spell slots. For instance, when you reach 3rd "
    "level in this class, you can learn one new spell of 1st or 2nd "
    "level.\n\nAdditionally, when you gain a level in this class, "
    "you can choose one of the sorcerer spells you know and replace "
    "it with another spell from the sorcerer spell list, which also "
    "must be of a level for which you have spell slots.\n\nSpellcasting "
    "Ability\n\nCharisma is your spellcasting ability for your "
    "sorcerer spells, since the power of your magic relies on your "
    "ability to project your will into the world. You use your Charisma "
    "whenever a spell refers to your spellcasting ability. In addition, "
    "you use your Charisma modifier when setting the saving throw DC "
    "for a sorcerer spell you cast and when making an attack roll with "
    "one.\n\tSpell save DC = 8 + your proficiency bonus + your Charisma "
    "modifier\n\tSpell attack modifier = your proficiency bonus + your "
    "Charisma modifier\n\nSpellcasting Focus\n\nYou can use an arcane "
    "focus as a spellcasting focus for your sorcerer spells."),
    (11, "Sorcerous Origin", 1, "Choose a sorcerous origin, which describes "
    "the source of your innate magical power. Your choice grants you "
    "features when you choose it at 1st level and again at 6th, 14th, "
    "and 18th level."),
    (11, "Font of Magic", 2, "At 2nd level, you tap into a deep wellspring "
    "of magic within yourself. This wellspring is represented by sorcery "
    "points, which allow you to create a variety of magical effects.\n\t"
    + chr(9679) + "Sorcery Points. You have 2 sorcery points, and you gain "
    "more as you reach higher levels, as shown in the Sorcery Points column of the "
    "Sorcerer table. You can never have more sorcery points than shown "
    "on the table for your level. You regain all spent sorcery points "
    "when you finish a long rest.\n\t" + chr(9679) + "Flexible Casting. You "
    "can use your sorcery points to gain additional spell slots, or sacrifice "
    "spell slots to gain additional sorcery points. You learn other ways to "
    "use your sorcery points as you reach higher levels.\n\t\t" + chr(9679) + "Creating "
    "Spell Slots. You can transform unexpended sorcery points into one spell "
    "slot as a bonus action on your turn. The Creating Spell Slots table shows "
    "the cost of creating a spell slot of a given level. You can create spell "
    "slots no higher in level than 5th. Any spell slot you create with this "
    "feature vanishes when you finish a long rest.\n\t\t" + chr(9679) + "Converting "
    "a Spell Slot to Sorcery Points. As a bonus action on your turn, you can "
    "expend one spell slot and gain a number of sorcery points equal to the slot's level."),
    (11, "Metamagic", 3, "At 3rd level, you gain the ability to twist your spells to "
    "suit your needs. You gain two of the following Metamagic options of your "
    "choice. You gain another one at 10th and 17th level.\n\nYou can use only "
    "one Metamagic option on a spell when you cast it, unless otherwise noted.\n\t"
    + chr(9679) + "Careful Spell. When you cast a spell that forces other "
    "creatures to make a saving throw, you can protect some of those creatures "
    "from the spell's full force. To do so, you spend 1 sorcery point and choose "
    "a number of those creatures up to your Charisma modifier (minimum of one "
    "creature). A chosen creature automatically succeeds on its saving throw "
    "against the spell.\n\t" + chr(9679) + "Distant Spell. When you cast a "
    "spell that has a range of 5 feet or greater, you can spend 1 sorcery "
    "point to double the range of the spell.\n\t" + chr(9679) + "When you "
    "cast a spell that has a range of touch, you can spend 1 sorcery point "
    "to make the range of the spell 30 feet.\n\t" + chr(9679) + "Empowered Spell. "
    "When you roll damage for a spell, you can spend 1 sorcery point to "
    "reroll a number of the damage dice up to your Charisma modifier (minimum "
    "of one). You must use the new rolls.\n\t" + chr(9679) + "You can use "
    "Empowered Spell even if you have already used a different Metamagic "
    "option during the casting of the spell.\n\t" + chr(9679) + "Extended Spell. "
    "When you cast a spell that has a duration of 1 minute or longer, you "
    "can spend 1 sorcery point to double its duration, to a maximum duration "
    "of 24 hours.\n\t" + chr(9679) + "Heightened Spell. When you cast a "
    "spell that forces a creature to make a saving throw to resist its "
    "effects, you can spend 3 sorcery points to give one target of the "
    "spell disadvantage on its first saving throw made against the spell."
    + chr(9679) + "Quickened Spell. When you cast a spell that has a "
    "casting time of 1 action, you can spend 2 sorcery points to change "
    "the casting time to 1 bonus action for this casting.\n\t" + chr(9679) +
    "Seeking Spell. If you make an attack roll for a spell and miss, you "
    "can spend 2 sorcerer points to reroll the d20, and you must use the "
    "new roll.\n\t" + chr(9679) + "You can use Seeking Spell even if you "
    "have already used a different Metamagic option during the casting of "
    "the spell.\n\t" + chr(9679) + "Seeking Spell (UA). When you cast a "
    "spell that requires you to make a spell attack roll or that forces "
    "a target to make a Dexterity saving throw, you can spend 1 sorcery "
    "point to ignore the effects of half- and three-quarters cover against "
    "targets of the spell.\n\t" + chr(9679) + "Subtle Spell. When you "
    "cast a spell, you can spend 1 sorcery point to cast it without any "
    "somatic or verbal components.\n\t" + chr(9679) + "Transmuted Spell. "
    "When you cast a spell that deals a type of damage from the "
    "following list, you can spend 1 sorcery point to change that damage "
    "type to one of the other listed types: acid, cold, fire, lightning, "
    "poison, thunder.\n\t" + chr(9679) + "Twinned Spell. When you cast "
    "a spell that targets only one creature and doesn't have a range "
    "of self, you can spend a number of sorcery points equal to the "
    "spell's level to target a second creature in range with the "
    "same spell (1 sorcery point if the spell is a cantrip). To be "
    "eligible, a spell must be incapable of targeting more than one "
    "creature at the spell's current level. For example, magic missile "
    "and scorching ray aren't eligible, but ray of frost and chromatic "
    "orb are."),
    (11, "Ability Score Improvement", 4, "When you reach 4th level, and "
    "again at 8th, 12th, 16th, and 19th level, you can increase one "
    "ability score of your choice by 2, or you can increase two ability "
    "scores of your choice by 1. As normal, you can't increase an ability "
    "score above 20 using this feature."),
    (11, "Sorcerous Origin Feature", 6, "Feature from your chosen Sorcerous."),
    (11, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (11, "Metamagic", 10, "Gain another Metamagic."),
    (11, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (11, "Sorcerous Origin", 14, "Feature from your chosen Sorcerous."),
    (11, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (11, "Metamagic", 17, "Gain another Metamagic."),
    (11, "Sorcerous Origin Feature", 18, "Feature from your chosen Sorcerous."),
    (11, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above "
    "20 using this feature."),
    (11, "Sorcerous Restoration", 20, "At 20th level, you regain 4 expended "
    "sorcery points whenever you finish a short rest."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', sorcerer_features)


warlock_features = [
    (12, "Otherworldly Patron", 1, "At 1st level, you have struck a bargain with "
    "an otherworldly being of your choice. Your choice grants you features at 1st "
    "level and again at 6th, 10th, and 14th level."),
    (12, "Pact Magic", 1, "Your arcane research and the magic bestowed on you by "
    "your patron have given you facility with spells.\n\nCantrips\n\nYou know two "
    "cantrips of your choice from the warlock spell list. You learn additional "
    "warlock cantrips of your choice at higher levels, as shown in the Cantrips "
    "Known column of the Warlock table.\n\nSpell Slots\n\nThe Warlock table "
    "shows how many spell slots you have to cast your warlock spells of 1st "
    "through 5th level. The table also shows what the level of those slots is; "
    "all of your spell slots are the same level. To cast one of your warlock "
    "spells of 1st level or higher, you must expend a spell slot. You regain "
    "all expended spell slots when you finish a short or long rest.\n\nFor example, "
    "when you are 5th level, you have two 3rd-level spell slots. To cast the "
    "1st-level spell witch bolt, you must spend one of those slots, and you "
    "cast it as a 3rd-level spell.\n\nSpells Known of 1st Level and Higher\n\n"
    "At 1st level, you know two 1st-level spells of your choice from the "
    "warlock spell list.\n\nThe Spells Known column of the Warlock table "
    "shows when you learn more warlock spells of your choice of 1st level "
    "or higher. A spell you choose must be of a level no higher than what's "
    "shown in the table's Slot Level column for your level. When you reach "
    "6th level, for example, you learn a new warlock spell, which can be 1st, "
    "2nd, or 3rd level.\n\nAdditionally, when you gain a level in this "
    "class, you can choose one of the warlock spells you know and replace "
    "it with another spell from the warlock spell list, which also must "
    "be of a level for which you have spell slots.\n\nSpellcasting Ability\n\n"
    "Charisma is your spellcasting ability for your warlock spells, so you "
    "use your Charisma whenever a spell refers to your spellcasting ability. "
    "In addition, you use your Charisma modifier when setting the saving "
    "throw DC for a warlock spell you cast and when making an attack roll "
    "with one.\n\tSpell save DC = 8 + your proficiency bonus + your Charisma "
    "modifier\n\tSpell attack modifier = your proficiency bonus + your "
    "Charisma modifier\n\nSpellcasting Focus\n\nYou can use an arcane focus "
    "as a spellcasting focus for your warlock spells."),
    (12, "Eldritch Invocations", 2, "In your study of occult lore, you have "
    "unearthed Eldritch Invocations, fragments of forbidden knowledge that "
    "imbue you with an abiding magical ability.\n\nAt 2nd level, you gain "
    "two eldritch invocations of your choice. When you gain certain warlock "
    "levels, you gain additional invocations of your choice, as shown in the "
    "Invocations Known column of the Warlock table. A level prerequisite "
    "refers to your level in this class.\n\nAdditionally, when you gain a "
    "level in this class, you can choose one of the invocations you know "
    "and replace it with another invocation that you could learn at that level."),
    (12, "Pact Boon", 3, "At 3rd level, your otherworldly patron bestows a gift "
    "upon you for your loyal service. You gain one of the following features "
    "of your choice.\n\t" + chr(9679) + "Pact of the Blade\n\t\tYou can use your "
    "action to create a pact weapon in your empty hand. You can choose the form that "
    "this melee weapon takes each time you create it. You are proficient with "
    "it while you wield it. This weapon counts as magical for the purpose of "
    "overcoming resistance and immunity to nonmagical attacks and damage.\n\t\t"
    "Your pact weapon disappears if it is more than 5 feet away from you "
    "for 1 minute or more. It also disappears if you use this feature again, "
    "if you dismiss the weapon (no action required), or if you die.\n\t\t"
    "You can transform one magic weapon into your pact weapon by performing "
    "a special ritual while you hold the weapon. You perform the ritual over "
    "the course of 1 hour, which can be done during a short rest.\n\t\t"
    "You can then dismiss the weapon, shunting it into an extradimensional "
    "space, and it appears whenever you create your pact weapon thereafter. "
    "You can't affect an artifact or a sentient weapon in this way. The weapon "
    "ceases being your pact weapon if you die, if you perform the 1-hour ritual "
    "on a different weapon, or if you use a 1-hour ritual to break your bond "
    "to it. The weapon appears at your feet if it is in the extradimensional "
    "space when the bond breaks.\n\t" + chr(9679) + "Pact of the Chain\n\t\t"
    "You learn the find familiar spell and can cast it as a ritual. The spell "
    "doesn't count against your number of spells known.\n\t\tWhen you cast the "
    "spell, you can choose one of the normal forms for your familiar or one "
    "of the following special forms: imp, pseudodragon, quasit, or sprite.\n\t\t"
    "Additionally, when you take the Attack action, you can forgo one of "
    "your own attacks to allow your familiar to make one attack with its "
    "reaction.\n\t" + chr(9679) + "Pact of the Tome\n\t\tYour patron gives "
    "you a grimoire called a Book of Shadows. When you gain this feature, "
    "choose three cantrips from any class's spell list (the three needn't "
    "be from the same list). While the book is on your person, you can "
    "cast those cantrips at will. They don't count against your number of "
    "cantrips known. If they don't appear on the warlock spell list, they "
    "are nonetheless warlock spells for you.\n\t\tIf you lose your Book of "
    "Shadows, you can perform a 1-hour ceremony to receive a replacement "
    "from your patron. This ceremony can be performed during a short or "
    "long rest, and it destroys the previous book. The book turns to ash "
    "when you die.\n\t" + chr(9679) + "Pact of the Talisman\n\t\tYour "
    "patron gives you an amulet, a talisman that can aid the wearer when "
    "the need is great. When the wearer fails an ability check, they can "
    "add a d4 to the roll, potentially turning the roll into a success. "
    "This benefit can be used a number of times equal to your proficiency "
    "bonus, and all expended uses are restored when you finish a long rest.\n\t\t"
    "If you lose the talisman, you can perform a 1-hour ceremony to receive "
    "a replacement from your patron. This ceremony can be performed during "
    "a short or long rest, and it destroys the previous amulet. The talisman "
    "turns to ash when you die."),
    (12, "Ability Score Improvement", 4, "When you reach 4th level, and again "
    "at 8th, 12th, 16th, and 19th level, you can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (12, "Otherworldly Patron", 6, "Feature from chosen Patron."),
    (12, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (12, "Otherworldly Patron", 10, "Feature from chosen Patron."),
    (12, "Mystic Arcanum", 11, "At 11th level, your patron bestows upon "
    "you a magical secret called an arcanum. Choose one 6th-level spell "
    "from the warlock spell list as this arcanum.\n\nYou can cast your "
    "arcanum spell once without expending a spell slot. You must finish a "
    "long rest before you can do so again.\n\nAt higher levels, you gain "
    "more warlock spells of your choice that can be cast in this way: one "
    "7th-level spell at 13th level, one 8th-level spell at 15th level, and "
    "one 9th-level spell at 17th level. You regain all uses of your Mystic "
    "Arcanum when you finish a long rest."),
    (12, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (12, "Mystic Arcanum (7th level)", 13, "You can cast one 7th-level spell once "
    "without expending a spell slot."),
    (12, "Otherworldly Patron", 14, "Feature from chosen Patron."),
    (12, "Mystic Arcanum (8th level)", 15, "You can cast one 8th-level spell once "
    "without expending a spell slot."),
    (12, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (12, "Mystic Arcanum (9th level)", 17, "You can cast one 9th-level spell once "
    "without expending a spell slot."),
    (12, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (12, "Eldritch Master", 20, "At 20th level, you can draw on your inner "
    "reserve of mystical power while entreating your patron to regain expended "
    "spell slots. You can spend 1 minute entreating your patron for aid to regain "
    "all your expended spell slots from your Pact Magic feature. Once you regain "
    "spell slots with this feature, you must finish a long rest before you can "
    "do so again."),
    
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', warlock_features)


wizard_features = [
    (13, "Spellcasting", 1, "As a student of arcane magic, you have a spellbook "
    "containing spells that show the first glimmerings of your true power.\n\nCantrips\n\n"
    "At 1st level, you know three cantrips of your choice from the wizard spell "
    "list. You learn additional wizard cantrips of your choice at higher levels, "
    "as shown in the Cantrips Known column of the Wizard table.\n\nSpellbook\n\nAt "
    "1st level, you have a spellbook containing six 1st-level wizard spells of your "
    "choice. Your spellbook is the repository of the wizard spells you know, except "
    "your cantrips, which are fixed in your mind.\n\nThe spells that you add to "
    "your spellbook as you gain levels reflect the arcane research you conduct on "
    "your own, as well as intellectual breakthroughs you have had about the nature "
    "of the multiverse. You might find other spells during your adventures. You "
    "could discover a spell recorded on a scroll in an evil wizard's chest, for "
    "example, or in a dusty tome in an ancient library.\n\nCopying a Spell into "
    "the Book. When you find a wizard spell of 1st level or higher, you can add "
    "it to your spellbook if it is of a spell level you can prepare and if you "
    "can spare the time to decipher and copy it.\n\nCopying a spell into your "
    "spellbook involves reproducing the basic form of the spell, then deciphering "
    "the unique system of notation used by the wizard who wrote it. You must "
    "practice the spell until you understand the sounds or gestures required, "
    "then transcribe it into your spellbook using your own notation.\n\nFor each "
    "level of the spell, the process takes 2 hours and costs 50 gp. The cost "
    "represents material components you expend as you experiment with the spell "
    "to master it, as well as the fine inks you need to record it. Once you have "
    "spent this time and money, you can prepare the spell just like your other "
    "spells.\n\n Replacing the Book. You can copy a spell from your own spellbook "
    "into another book-for example, if you want to make a backup copy of your "
    "spellbook. This is just like copying a new spell into your spellbook, but "
    "faster and easier, since you understand your own notation and already know "
    "how to cast the spell. You need spend only 1 hour and 10 gp for each level "
    "of the copied spell.\n\nIf you lose your spellbook, you can use the same "
    "procedure to transcribe the spells that you have prepared into a new "
    "spellbook. Filling out the remainder of your spellbook requires you to "
    "find new spells to do so, as normal. For this reason, many wizards keep "
    "backup spellbooks in a safe place.\n\nThe Book's Appearance. Your spellbook "
    "is a unique compilation of spells, with its own decorative flourishes and "
    "margin notes. It might be a plain, functional leather volume that you "
    "received as a gift from your master, a finely bound gilt-edged tome you "
    "found in an ancient library or even a loose collection of notes scrounged "
    "together after you lost your previous spellbook in a mishap.\n\nPreparing and "
    "Casting Spells\n\nThe Wizard table shows how many spell slots you have to "
    "cast your wizard spells of 1st level and higher. To cast one of these "
    "spells, you must expend a slot of the spell's level or higher. You regain "
    "all expended spell slots when you finish a long rest.\n\nYou prepare the "
    "list of wizard spells that are available for you to cast. To do so, choose "
    "a number of wizard spells from your spellbook equal to your Intelligence "
    "modifier + your wizard level (minimum of one spell). The spells must be "
    "of a level for which you have spell slots.\n\nFor example, if you're a "
    "3rd-level wizard, you have four 1st-level and two 2nd-level spell slots. "
    "With an Intelligence of 16, your list of prepared spells can include six "
    "spells of 1st or 2nd level, in any combination, chosen from your spellbook. "
    "If you prepare the 1st-level spell magic missile, you can cast it using a "
    "1st-level or a 2nd-level slot. Casting the spell doesn't remove it from "
    "your list of prepared spells.\n\nYou can change your list of prepared "
    "spells when you finish a long rest. Preparing a new list of wizard spells "
    "requires time spent studying your spellbook and memorizing the incantations "
    "and gestures you must make to cast the spell: at least 1 minute per spell "
    "level for each spell on your list.\n\nSpellcasting Ability\n\nIntelligence "
    "is your spellcasting ability for your wizard spells, since you learn your "
    "spells through dedicated study and memorization. You use your Intelligence "
    "whenever a spell refers to your spellcasting ability. In addition, you "
    "use your Intelligence modifier when setting the saving throw DC for a "
    "wizard spell you cast and when making an attack roll with one.\n\tSpell "
    "save DC = 8 + your proficiency bonus + your Intelligence modifier\n\tSpell "
    "attack modifier = your proficiency bonus + your Intelligence modifier\n\nRitual "
    "Casting\n\nYou can cast a wizard spell as a ritual if that spell has the "
    "ritual tag and you have the spell in your spellbook. You don't need to have "
    "the spell prepared.\n\nSpellcasting Focus\n\nYou can use an arcane focus "
    "as a spellcasting focus for your wizard spells.\n\nLearning Spells of 1st "
    "Level and Higher\n\nEach time you gain a wizard level, you can add two "
    "wizard spells of your choice to your spellbook. Each of these spells must "
    "be of a level for which you have spell slots, as shown on the Wizard table. "
    "On your adventures, you might find other spells that you can add to your spellbook."),
    (13, "Arcane Recovery", 1, "You have learned to regain some of your magical "
    "energy by studying your spellbook. Once per day when you finish a short rest, "
    "you can choose expended spell slots to recover. The spell slots can have a "
    "combined level that is equal to or less than half your wizard level (rounded "
    "up), and none of the slots can be 6th level or higher.\n\nFor example, if "
    "you're a 4th-level wizard, you can recover up to two levels worth of "
    "spell slots. You can recover either a 2nd-level spell slot or two "
    "1st-level spell slots."),
    (13, "Arcane Tradition", 2, "When you reach 2nd level, you choose an "
    "arcane tradition, shaping your practice of magic through one of the following "
    "schools. Your choice grants you features at 2nd level and again at 6th, "
    "10th, and 14th level."),
    (13, "Ability Score Improvement", 4, "When you reach 4th level, and again "
    "at 8th, 12th, 16th, and 19th level, you can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (13, "Arcane Tradition", 6, "From your chosen Arcane Tradition."),
    (13, "Ability Score Improvement", 8, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (13, "Arcane Tradition", 10, "From your chosen Arcane Tradition."),
    (13, "Ability Score Improvement", 12, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (13, "Arcane Tradition", 14, "From your chosen Arcane Tradition."),
    (13, "Ability Score Improvement", 16, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (13, "Spell Mastery", 18, "At 18th level, you have achieved such mastery "
    "over certain spells that you can cast them at will. Choose a 1st-level "
    "wizard spell and a 2nd-level wizard spell that are in your spellbook. "
    "You can cast those spells at their lowest level without expending a "
    "spell slot when you have them prepared. If you want to cast either "
    "spell at a higher level, you must expend a spell slot as normal.\n\nBy "
    "spending 8 hours in study, you can exchange one or both of the spells "
    "you chose for different spells of the same levels."),
    (13, "Ability Score Improvement", 19, "You can increase one ability score "
    "of your choice by 2, or you can increase two ability scores of your "
    "choice by 1. As normal, you can't increase an ability score above 20 "
    "using this feature."),
    (13, "Signature Spells", 20, "When you reach 20th level, you gain "
    "mastery over two powerful spells and can cast them with little effort. "
    "Choose two 3rd-level wizard spells in your spellbook as your signature "
    "spells. You always have these spells prepared, they don't count against "
    "the number of spells you have prepared, and you can cast each of them "
    "once at 3rd level without expending a spell slot. When you do so, you "
    "can't do so again until you finish a short or long rest.\n\nIf you want "
    "to cast either spell at a higher level, you must expend a spell slot "
    "as normal."),
    
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', wizard_features)


c.execute('''CREATE TABLE IF NOT EXISTS subclasses(
            class_id INTEGER,
            subclass_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(id))
    ''')

subclasses = [
    (1, 1, "Alchemist", "You specialize in experimental potion-making, using your alchemical mastery to"
    "craft powerful elixirs. These potions can heal, bolster defenses or provide various enhancements"
    "to you and your allies."),
    (1, 2, "Armorer", "You channel your expertise into crafting magical armor, transforming it"
    "into a powerful exosuit. This suit enhances your combat abilities, offers exceptional protection"
    "and can be customized with various magical effects to suit different combat roles."),
    (2, 1, "Path of the Berserker", "You give in to the fury of combat, allowing you to fight with a primal ferocity."
    "While in the grips of your battle rage, you can make extra attacks and ignore effects that would otherwise"
    "cause damage or slow you down."),
    (2, 2, "Path of the Totem Warrior", "You forge a spiritual bond with a totem animal spirit,"
    "emulating the aspects of that being. Each animal spirit—be it bear, eagle, elk, tiger or"
    "wolf—provides unique strengths and supernatural abilities to aid you and your allies."),
    (3, 1, "College of Lore", "You collect bits of knowledge from all manner of stories, songs and spells. This"
    "subclass enhances your versatility by granting additional proficiencies, magical secrets from other classes"
    "and the ability to use your knowledge to limit enemy attacks."),
    (3, 2, "College of Swords", "You blend performance with martial prowess, using your weapon as both an instrument"
    "and a conduit for your bardic spells. This subclass focuses on enhancing your combat abilities, allowing for"
    "flourishes that deal extra damage and bolster your defenses."),
    (4, 1, "Life Domain", "You are a conduit of healing and vitality, specializing in spells that restore"
    "and sustain life. This domain increases the effectiveness of your healing spells and grants you"
    "abilities to protect and bolster your allies."),
    (4, 2, "Light Domain", "You channel the power of light and fire, wielding these elements against the darkness."
    "This domain provides powerful options to scorch your enemies, dispel darkness, and protect allies with radiant energy."),
    (5, 1, "Circle of the Land", "You have a deep connection to a specific natural terrain,"
    "such as forests, mountains or coastlines. This subclass enhances your magical abilities,"
    "allowing you to draw upon the arcane essence of your chosen land for additional spells."),
    (5, 2, "Circle of the Moon", "You specialize in transforming into more powerful animals"
    "and even elemental forms. This subclass focuses on improving your combat effectiveness"
    "in beast form, granting you the ability to become larger, stronger and more formidable creatures."),
    (6, 1, "Battle Master", "You are a master of combat techniques and tactics, using maneuvers to"
    "outsmart and defeat your enemies. This subclass grants you abilities to enhance your attacks,"
    "control the battlefield and provide tactical advantages to your allies."),
    (6, 2, "Champion", "You focus on refining your martial prowess, becoming a formidable warrior. This"
    "subclass enhances your ability to land critical hits more often and increases your physical capabilities,"
    "making you a relentless fighter."),
    (7, 1, "Way of the Open Hand", "You focus on the pure techniques of martial arts, perfecting"
    "strikes that incapacitate your foes. This subclass gives you powerful techniques to"
    "knock enemies prone, push them away or deny them reactions, exemplifying the art of hand-to-hand combat."),
    (7, 2, "Way of the Shadow", "You embrace the stealth and cunning of the shadow, using darkness to"
    "conceal your movements and strike unseen. This subclass allows you to teleport into shadows, become"
    "invisible in dim light and use the dark as a weapon against your enemies."),
    (8, 1, "Oath of the Ancients", "Dedicated to preserving the light and life found in nature, you can"
    "access abilities that heal and protect, as well as tapping into offensive spells that harness nature’s wrath."),
    (8, 2, "Oath of Vengeance", "Focused on punishing evildoers, this subclass offers aggressive"
    "tactics and powers that enhance your ability to hunt down and destroy your enemies, emphasizing"
    "relentless offensive attacks."),
    (9, 1, "Gloom Stalker", "You excel in darkness and ambush, using your skills to become nearly invisible in the shadows."
    "Your attacks are swift and deadly, particularly at the onset of battle, giving you a critical advantage in the first"
    "moments of combat."),
    (9, 2, "Hunter", "You specialize in tracking and defeating a variety of creatures, adapting your tactics based on the"
    "nature of your prey. In addition, you gain specific abilities that enhance your effectiveness against certain types"
    "of enemies."),
    (10, 1, "Arcane Trickster", "You enhance your skills as a rogue with the subtle magic of illusion and"
    "enchantment. This subclass grants you the ability to cast spells that can manipulate others, hide your"
    "movements or confuse your foes."),
    (10, 2, "Assassin", "You specialize in infiltration and the art of the kill, becoming a master"
    "of disguise and deadly strikes. This subclass provides you with bonuses for attacking unaware"
    "opponents, allowing you to deal significant damage in the first moments of combat."),
    (11, 1, "Divine Soul", "With a touch of the divine in your bloodline, you blend sorcerous"
    "magic with divine power. This subclass provides you access to both sorcerer and cleric"
    "spell lists, enhancing your healing and protective capabilities alongside your natural sorcery."),
    (11, 2, "Draconic Bloodline", "Your magical powers derive from a dragon ancestor, granting you"
    "scales, fearsome presence and elemental affinities related to your dragon’s nature. This"
    "subclass enhances your durability, charisma, and grants abilities based on the type of dragon from which you descend."),
    (12, 1, "Fiend", "Your patron is a creature of the lower planes, bestowing upon you the"
    "ability to channel fiery wrath and curses upon your foes. This subclass enhances your resilience,"
    "provides bonuses to certain types of spells and allows you to temporarily gain hit points"
    "when you reduce a foe to 0 hit points."),
    (12, 2, "Hexblade", "You are connected to a magical weapon borne from the Shadowfell,"
    "which grants you combat prowess and the ability to curse your foes. This subclass"
    "enhances your melee capabilities, allows you to use charisma for weapon attacks and"
    "provides spells related to combat and protection."),
    (13, 1, "School of Abjuration", "You specialize in protective magic, strengthening"
    "your defenses and banishing enemies. This school enhances your ability to cast wards,"
    "counterspells and protective enchantments, making you and your allies more resilient against attacks."),
    (13, 2, "School of Evocation", "You channel raw elemental power into destructive spells"
    "to control and maximize damage. This school allows you to shape spells to protect allies,"
    "augment attacks and target enemies from afar."),
    ]

c.executemany('''INSERT INTO subclasses (class_id, subclass_id, name, description) VALUES (?, ?, ?, ?)''', subclasses)

c.execute('''CREATE TABLE IF NOT EXISTS subclass_features (
            class_id INTEGER NOT NULL,
            subclass_id INTEGER NOT NULL,
            feature_name TEXT NOT NULL,
            level INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(id),
            FOREIGN KEY (subclass_id) REFERENCES sublasses(subclass_id))
    ''')



subclass_features = [
    (1, 1, "Tool Proficiency", 3, "When you adopt this specialization at 3rd level, you"
    "gain proficiency with alchemist's supplies. If you already have this proficiency, you"
    "gain proficiency with one other type of artisan's tools of your choice."),
    (1, 1, "Alchemist Spells", 3, "Starting at 3rd level, you always have certain spells"
    "prepared after you reach particular levels in this class, as shown in the Alchemist"
    "Spells table. These spells count as artificer spells for you, but they don’t count against"
    "the number of artificer spells you prepare."),
    (1, 1, "Experimental Elixir", 3, "Beginning at 3rd level, whenever you finish a long rest, you"
    "can magically produce an experimental elixir in an empty flask you touch. Roll on the Experimental"
    "Elixir table for the elixir's effect, which is triggered when someone drinks the elixir. As an"
    "action, a creature can drink the elixir or administer it to an incapacitated creature.\n"
    "You can create additional experimental elixirs by expending a spell slot of 1st level or"
    "higher for each one. When you do so, you use your action to create the elixir in an empty flask"
    "you touch, and you choose the elixir's effect from the Experimental Elixir table.\n Creating"
    "an experimental elixir requires you to have alchemist supplies on your person, and any elixir you"
    "create with this feature lasts until it is drunk or until the end of your next long rest.\n When"
    "you reach certain levels in this class, you can make more elixirs at the end of a long rest: two"
    "at 6th level and three at 15th level. Roll for each elixir's effect separately. Each"
    "elixir requires its own flask."),
    (1, 1, "Alchemical Savant", 5, "At 5th level, you've developed masterful command of magical chemicals,"
    "enhancing the healing and damage you create through them. Whenever you cast a spell using your alchemist's"
    "supplies as the spellcasting focus, you gain a bonus to one roll of the spell. That roll must restore hit"
    "points or be a damage roll that deals acid, fire, necrotic, or poison damage, and the bonus equals your"
    "Intelligence modifier (minimum of +1)."),
    (1, 1, "Restorative Reagents", 9, "Starting at 9th level, you can incorporate restorative reagents into"
    "some of your works:\n Whenever a creature drinks an experimental elixir you created, the creature"
    "gains temporary hit points equal to 2d6 + your Intelligence modifier (minimum of 1 temporary hit point).\n"
    "You can cast Lesser Restoration without expending a spell slot and without preparing the spell, provided"
    "you use alchemist's supplies as the spellcasting focus. You can do so a number of times equal to your"
    "Intelligence modifier (minimum of once), and you regain all expended uses when you finish a long rest."),
    (1, 1, "Chemical Mastery", 15, "By 15th level, you have been exposed to so many chemicals that they pose"
    "little risk to you, and you can use them to quickly end certain ailments:\n You gain resistance to"
    "acid damage and poison damage, and you are now immune to the poisoned condition.\n You can cast"
    "Greater Restoration and Heal without expending a spell slot, without preparing the spell, and"
    "without providing the material component, provided you use alchemist’s supplies as the spellcasting"
    "focus. Once you cast either spell with this feature, you can't cast that spell with it again until"
    "you finish a long rest."),
    (1, 2, "Tools of the Trade", 3, "When you adopt this specialization at 3rd level, you gain"
    "proficiency with heavy armor. You also gain proficiency with smith's tools. If you already"
    "have this tool proficiency, you gain proficiency with one other type of artisan's tools of your choice."),
    (1, 2, "Armorer Spells", 3, "Starting at 3rd level, you always have certain spells prepared after"
    "you reach particular levels in this class, as shown in the Armorer Spells table. These spells count"
    "as artificer spells for you, but they don't count against the number of artificer spells you prepare."),
    (1, 2, "Arcane Armor", 3, "Beginning at 3rd level, your metallurgical pursuits have led to you making"
    "armor a conduit for your magic. As an action, you can turn a suit of armor you are wearing into"
    "Arcane Armor, provided you have smith's tools in hand. \nYou gain the following benefits while"
    "wearing this armor: \nIf the armor normally has a Strength requirement, the arcane armor lacks"
    "this requirement for you. \nYou can use the arcane armor as a spellcasting focus for your artificer spells."
    "The armor attaches to you and can’t be removed against your will. It also expands to cover your"
    "entire body, although you can retract or deploy the helmet as a bonus action. The armor replaces"
    "any missing limbs, functioning identically to a body part it is replacing. \nYou can doff or don"
    "the armor as an action. \nThe armor continues to be Arcane Armor until you don another suit of armor or you die."),
    (1, 2, "Armor Model", 3, "Beginning at 3rd level, you can customize your Arcane Armor. When you do so,"
    "choose one of the following armor models: Guardian or Infiltrator. The model you choose gives you"
    "special benefits while you wear it. \nEach model includes a special weapon. When you attack with"
    "that weapon, you can add your Intelligence modifier, instead of Strength or Dexterity, to the"
    "attack and damage rolls. \nYou can change the armor's model whenever you finish a short or"
    "long rest, provided you have smith's tools in hand. \nGuardian. You design your armor to be"
    "in the front line of conflict. It has the following features: \nThunder Gauntlets. Each of the"
    "armor's gauntlets counts as a simple melee weapon while you aren't holding anything in it, and"
    "it deals 1d8 thunder damage on a hit. A creature hit by the gauntlet has disadvantage on attack"
    "rolls against targets other than you until the start of your next turn, as the armor magically"
    "emits a distracting pulse when the creature attacks someone else. \nDefensive Field. As a bonus"
    "action, you can gain temporary hit points equal to your level in this class, replacing any temporary"
    "hit points you already have. You lose these temporary hit points if you doff the armor. You"
    "can use this bonus action a number of times equal to your proficiency bonus, and you regain all"
    "expended uses when you finish a long rest. \nInfiltrator. \nYou customize your armor for subtle"
    "undertakings. It has the following features: \nLightning Launcher. A gemlike node appears on"
    "one of your armored fists or on the chest (your choice). It counts as a simple ranged weapon, with"
    "a normal range of 90 feet and a long range of 300 feet, and it deals 1d6 lightning damage"
    "on a hit. Once on each of your turns when you hit a creature with it, you can deal an extra"
    "1d6 lightning damage to that target. \nPowered Steps. Your walking speed increases by 5 feet."
    "\nDampening Field. You have advantage on Dexterity (Stealth) checks. If the armor normally"
    "imposes disadvantage on such checks, the advantage and disadvantage cancel each other, as normal."),
    (1, 2, "Extra Attack", 5, "Starting at 5th level, you can attack twice, rather than once, whenever"
    "you take the Attack action on your turn."),
    (1, 2, "Armor Modifications", 9, "At 9th level, you learn how to use your artificer infusions"
    "to specially modify your Arcane Armor. That armor now counts as separate items for the purposes"
    "of your Infuse Items feature: armor (the chest piece), boots, helmet, and the armor's special weapon."
    "Each of those items can bear one of your infusions, and the infusions transfer over if you change your"
    "armor's model with the Armor Model feature. In addition, the maximum number of items you can infuse"
    "at once increases by 2, but those extra items must be part of your Arcane Armor."),
    (1, 2, "Perfected Armor", 3, "At 15th level, your Arcane Armor gains additional benefits based on its"
    "model, as shown below. \nGuardian. When a Huge or smaller creature you can see ends its turn within"
    "30 feet of you, you can use your reaction to magically force it to make a Strength saving throw"
    "against your spell save DC. On a failed save, you pull the creature up to 25 feet directly to"
    "an unoccupied space. If you pull the target to a space within 5 feet of you, you can make a"
    "melee weapon attack against it as part of this reaction. \nYou can use this reaction a number"
    "of times equal to your proficiency bonus, and you regain all expended uses of it when you finish"
    "a long rest. \nInfiltrator. Any creature that takes lightning damage from your Lightning Launcher"
    "glimmers with magical light until the start of your next turn. The glimmering creature sheds"
    "dim light in a 5-foot radius, and it has disadvantage on attack rolls against you, as the light"
    "jolts it if it attacks you. In addition, the next attack roll against it has advantage, and"
    "if that attack hits, the target takes an extra 1d6 lightning damage."),
    (2, 1, "Frenzy", 3, "Starting when you choose this path at 3rd level, you can go into a frenzy "
    "when you rage. If you do so, for the duration of your rage you can make a single melee weapon "
    "attack as a bonus action on each of your turns after this one. When your rage ends, you suffer "
    "one level of exhaustion."),
    (2, 1, "Mindless Rage", 6, "Beginning at 6th level, you can't be charmed or frightened while "
    "raging. If you are charmed or frightened when you enter your rage, the effect is suspended "
    "for the duration of the rage."),
    (2, 1, "Intimidating Presence", 10, "Beginning at 10th level, you can use your action to "
    "frighten someone with your menacing presence. When you do so, choose one creature that "
    "you can see within 30 feet of you. If the creature can see or hear you, it must succeed on a "
    "Wisdom saving throw (DC equal to 8 + your proficiency bonus + your Charisma modifier) or be "
    "frightened of you until the end of your next turn. On subsequent turns, you can use your "
    "action to extend the duration of this effect on the frightened creature until the end of "
    "your next turn. This effect ends if the creature ends its turn out of line of sight or more "
    "than 60 feet away from you.\n\nIf the creature succeeds on its saving throw, you can't use "
    "this feature on that creature again for 24 hours."),
    (2, 1, "Retaliation", 14, "Starting at 14th level, when you take damage from a creature that "
    "is within 5 feet of you, you can use your reaction to make a melee weapon attack against "
    "that creature."),
    (2, 2, "Spirit Seeker", 3, "Yours is a path that seeks attunement with the natural world, "
    "giving you a kinship with beasts. At 3rd level when you adopt this path, you gain the "
    "ability to cast the Beast Sense and Speak with Animals spells, but only as rituals."),
    (2, 2, "Totem Spirit", 3, "At 3rd level, when you adopt this path, you choose a totem "
    "spirit and gain its feature. You must make or acquire a physical totem object – an "
    "amulet or similar adornment – that incorporates fur or feathers, claws, teeth, or bones "
    "of the totem animal. At your option, you also gain minor physical attributes that are "
    "reminiscent of your totem spirit. For example, if you have a bear totem spirit, you "
    "might be unusually hairy and thick-skinned, or if your totem is the eagle, your "
    "eyes turn bright yellow.\n\nYour totem animal might be an animal related to those "
    "listed here but more appropriate to your homeland. For example, you could choose a "
    "hawk or vulture in place of an eagle.\n\tBear. While raging, you have resistance to "
    "all damage except psychic damage. The spirit of the bear makes you tough enough "
    "to stand up to any punishment.\n\tEagle. While you're raging and aren't wearing "
    "heavy armor, other creatures have disadvantage on opportunity attack rolls against "
    "you, and you can use the Dash action as a bonus action on your turn. The spirit "
    "of the eagle makes you into a predator who can weave through the fray with ease.\n\tElk. "
    "While you're raging and aren't wearing heavy armor, your walking speed increases by "
    "15 feet. The spirit of the elk makes you extraordinarily swift.\n\tTiger. While raging, "
    "you can add 10 feet to your long jump distance and 3 feet to your high jump "
    "distance. The spirit of the tiger empowers your leaps.\n\tWolf. While you're raging, "
    "your friends have advantage on melee attack rolls against any creature within 5 "
    "feet of you that is hostile to you. The spirit of the wolf makes you a leader of hunters."),
    (2, 2, "Aspect of the Beast", 6, "At 6th level, you gain a magical benefit based on the "
    "totem animal of your choice. You can choose the same animal you selected at 3rd level "
    "or a different one.\n\tBear. You gain the might of a bear. Your carrying capacity (including "
    "maximum load and maximum lift) is doubled, and you have advantage on Strength checks made "
    "to push, pull, lift, or break objects.\n\tEagle. You gain the eyesight of an eagle. You can "
    "see up to 1 mile away with no difficulty, able to discern even fine details as though "
    "looking at something no more than 100 feet away from you. Additionally, dim light doesn't "
    "impose disadvantage on your Wisdom (Perception) checks.\n\tElk. Whether mounted or on foot, "
    "your travel pace is doubled, as is the travel pace of up to ten companions while they're "
    "within 60 feet of you and you're not incapacitated. The elk spirit helps you roam far and "
    "fast.\n\tTiger. You gain proficiency in two skills from the following list: Athletics, "
    "Acrobatics, Stealth, and Survival. The cat spirit hones your survival instincts.\n\tWolf. "
    "You gain the hunting sensibilities of a wolf. You can track other creatures while traveling "
    "at a fast pace, and you can move stealthily while traveling at a normal pace."),
    (2, 2, "Spirit Walker", 10, "At 10th level, you can cast the Commune with Nature spell, "
    "but only as a ritual. When you do so, a spiritual version of one of the animals you "
    "chose for Totem Spirit or Aspect of the Beast appears to you to convey the information you seek."),
    (2, 2, "Totemic Attunement", 14, "At 14th level, you gain a magical benefit based on a totem "
    "animal of your choice. You can choose the same animal you selected previously or a different "
    "one.\n\tBear. While you're raging, any creature within 5 feet of you that's hostile to you "
    "has disadvantage on attack rolls against targets other than you or another character with "
    "this feature. An enemy is immune to this effect if it can't see or hear you or if it can't "
    "be frightened.\n\tEagle. While raging, you have a flying speed equal to your current "
    "walking speed. This benefit works only in short bursts; you fall if you end your turn in "
    "the air and nothing else is holding you aloft.\n\tElk. While raging, you can use a bonus "
    "action during your move to pass through the space of a Large or smaller creature. That "
    "creature must succeed on a Strength saving throw (DC 8 + your Strength bonus + your "
    "proficiency bonus) or be knocked prone and take bludgeoning damage equal to 1d12 + your "
    "Strength modifier.\n\tTiger. While you're raging, if you move at least 20 feet in a "
    "straight line toward a Large or smaller target right before making a melee weapon "
    "attack against it, you can use a bonus action to make an additional melee weapon "
    "attack against it.\n\tWolf. While you're raging, you can use a bonus action on "
    "your turn to knock a Large or smaller creature prone when you hit it with melee "
    "weapon attack."),
    (3, 1, "Bonus Proficiencies", 3, "When you join the College of Lore at 3rd level, "
    "you gain proficiency with three skills of your choice."),
    (3, 1, "Cutting Words", 3, "Also at 3rd level, you learn how to use your wit to "
    "distract, confuse, and otherwise sap the confidence and competence of others. When "
    "a creature that you can see within 60 feet of you makes an attack roll, an ability "
    "check, or a damage roll, you can use your reaction to expend one of your uses of "
    "Bardic Inspiration, rolling a Bardic Inspiration die and subtracting the number "
    "rolled from the creature's roll. You can choose to use this feature after the "
    "creature makes its roll, but before the DM determines whether the attack roll or "
    "ability check succeeds or fails, or before the creature deals its damage. The "
    "creature is immune if it can't hear you or if it's immune to being charmed."),
    (3, 1, "Additional Magical Secrets", 6, "At 6th level, you learn two spells of your "
    "choice from any class. A spell you choose must be of a level you can cast, as shown "
    "on the Bard table, or a cantrip. The chosen spells count as bard spells for you but "
    "don't count against the number of bard spells you know."),
    (3, 1, "Peerless Skill", 14, "Starting at 14th level, when you make an ability check, "
    "you can expend one use of Bardic Inspiration. Roll a Bardic Inspiration die and add "
    "the number rolled to your ability check. You can choose to do so after you roll the "
    "die for the ability check, but before the DM tells you whether you succeed or fail."),
    (3, 2, "Bonus Proficiencies", 3, "When you join the College of Swords at 3rd level, "
    "you gain proficiency with medium armor and the scimitar.\n\nIf you’re proficient with "
    "a simple or martial melee weapon, you can use it as a spellcasting focus for your bard spells."),
    (3, 2, "Fighting Style", 3, "At 3rd level, you adopt a particular style of fighting as "
    "your specialty. Choose one of the following options. You can't take a Fighting Style "
    "option more than once, even if you later get to choose again.\n\t" + chr(9679) + "Dueling. "
    "When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 "
    "bonus to damage rolls with that weapon.\n\t" + chr(9679) + "Two-Weapon Fighting. When you "
    "engage in two-weapon fighting, you can add your ability modifier to the damage of the "
    "second attack."),
    (3, 2, "Blade Flourish", 3, "At 3rd level, you learn to conduct impressive displays of "
    "martial prowess and speed.\n\nWhenever you take the Attack action on your turn, your "
    "walking speed increases by 10 feet until the end of the turn, and if a weapon attack "
    "that you make as part of this action hits a creature, you can use one of the following "
    "Blade Flourish options of your choice. You can use only one Blade Flourish option per turn. "
    "\n\nDefensive Flourish. You can expend one use of your Bardic Inspiration to cause the "
    "weapon to deal extra damage to the target you hit. The damage equals the number you roll "
    "on the Bardic Inspiration die. You also add the number rolled to your AC until the start "
    "of your next turn.\n\nSlashing Flourish. You can expend one use of your Bardic Inspiration "
    "to cause the weapon to deal extra damage to the target you hit and to any other creature "
    "of your choice that you can see within 5 feet of you. The damage equals the number you "
    "roll on the Bardic Inspiration die.\n\nMobile Flourish. You can expend one use of your "
    "Bardic Inspiration to cause the weapon to deal extra damage to the target you hit. The "
    "damage equals the number you roll on the Bardic Inspiration die. You can also push the "
    "target up to 5 feet away from you, plus a number of feet equal to the number you roll "
    "on that die. You can then immediately use your reaction to move up to your walking "
    "speed to an unoccupied space within 5 feet of the target."),
    (3, 2, "Extra Attack", 6, "Starting at 6th level, you can attack twice, instead of once, "
    "whenever you take the Attack action on your turn."),
    (3, 2, "Master's Flourish", 14, "Starting at 14th level, whenever you use a Blade Flourish "
    "option, you can roll a d6 and use it instead of expending a Bardic Inspiration die."),
    (4, 1, "Bonus Proficiencies", 1, "When you choose this domain at 1st level, you gain "
    "proficiency with heavy armor."),
    (4, 1, "Disciple of Life", 1, "Also starting at 1st level, your healing spells are more "
    "effective. Whenever you use a spell of 1st level or higher to restore hit points to a "
    "creature, the creature regains additional hit points equal to 2 + the spell's level."),
    (4, 1, "Channel Divinity: Preserve Life", 2, "Starting at 2nd level, you can use your "
    "Channel Divinity to heal the badly injured.\n\nAs an action, you present your holy "
    "symbol and evoke healing energy that can restore a number of hit points equal to "
    "five times your cleric level. Choose any creatures within 30 feet of you, and divide "
    "those hit points among them. This feature can restore a creature to no more than half "
    "of its hit point maximum. You can't use this feature on an undead or a construct."),
    (4, 1, "Blessed Healer", 6, "Beginning at 6th level, the healing spells you cast on others "
    "heal you as well. When you cast a spell of 1st level or higher that restores hit points "
    "to a creature other than you, you regain hit points equal to 2 + the spell's level."),
    (4, 1, "Divine Strike", 8, "At 8th level, you gain the ability to infuse your weapon "
    "strikes with divine energy. Once on each of your turns when you hit a creature with a "
    "weapon attack, you can cause the attack to deal an extra 1d8 radiant damage to the "
    "target. When you reach 14th level, the extra damage increases to 2d8."),
    (4, 1, "Supreme Healing", 17, "Starting at 17th level, when you would normally roll one "
    "or more dice to restore hit points with a spell, you instead use the highest number "
    "possible for each die. For example, instead of restoring 2d6 hit points to a "
    "creature, you restore 12."),
    (4, 2, "Bonus Cantrip", 1, "When you choose this domain at 1st level, you gain the "
    "Light cantrip if you don't already know it. This cantrip doesn’t count against "
    "the number of cleric cantrips you know."),
    (4, 2, "Warding Flare", 1, "Also at 1st level, you can interpose divine light between "
    "yourself and an attacking enemy. When you are attacked by a creature within 30 feet "
    "of you that you can see, you can use your reaction to impose disadvantage on the "
    "attack roll, causing light to flare before the attacker before it hits or misses. "
    "An attacker that can't be blinded is immune to this feature.\n\nYou can use this "
    "feature a number of times equal to your Wisdom modifier (a minimum of once). You "
    "regain all expended uses when you finish a long rest."),
    (4, 2, "Channel Divinity: Radiance of the Dawn", 2, "Starting at 2nd level, you can "
    "use your Channel Divinity to harness sunlight, banishing darkness and dealing radiant "
    "damage to your foes.\n\nAs an action, you present your holy symbol, and any magical "
    "darkness within 30 feet of you is dispelled. Additionally, each hostile creature "
    "within 30 feet of you must make a Constitution saving throw. A creature takes "
    "radiant damage equal to 2d10 + your cleric level on a failed saving throw, and "
    "half as much damage on a successful one. A creature that has total cover from "
    "you is not affected."),
    (4, 2, "Improved Flare", 6, "Starting at 6th level, you can also use your Warding "
    "Flare feature when a creature that you can see within 30 feet of you attacks a "
    "creature other than you."),
    (4, 2, "Potent Spellcasting", 8, "Starting at 8th level, you add your Wisdom "
    "modifier to the damage you deal with any cleric cantrip."),
    (4, 2, "Corona of Light", 17, "Starting at 17th level, you can use your action "
    "to activate an aura of sunlight that lasts for 1 minute or until you dismiss "
    "it using another action. You emit bright light in a 60-foot radius and dim light "
    "30 feet beyond that. Your enemies in the bright light have disadvantage on saving "
    "throws against any spell that deals fire or radiant damage."),
    (5, 1, "Bonus Cantrip", 2, "When you choose this circle at 2nd level, you learn "
    "one additional druid cantrip of your choice. This cantrip doesn’t count against "
    "the number of druid cantrips you know."),
    (5, 1, "Natural Recovery", 2, "Starting at 2nd level, you can regain some of your "
    "magical energy by sitting in meditation and communing with nature. During a short "
    "rest, you choose expended spell slots to recover. The spell slots can have a "
    "combined level that is equal to or less than half your druid level (rounded up), "
    "and none of the slots can be 6th level or higher. You can't use this feature "
    "again until you finish a long rest.\n\nFor example, when you are a 4th-level "
    "druid, you can recover up to two levels worth of spell slots. You can recover "
    "either a 2nd-level slot or two 1st-level slots."),
    (5, 1, "Circle Spells", 3, "Your mystical connection to the land infuses you "
    "with the ability to cast certain spells. At 3rd, 5th, 7th, and 9th level you "
    "gain access to circle spells connected to the land where you became a druid. "
    "Choose that land – arctic, coast, desert, forest, grassland, mountain, swamp, "
    "or Underdark – and consult the associated list of spells.\n\nOnce you gain "
    "access to a circle spell, you always have it prepared, and it doesn't count "
    "against the number of spells you can prepare each day. If you gain access "
    "to a spell that doesn't appear on the druid spell list, the spell is "
    "nonetheless a druid spell for you."),
    (5, 1, "Land's Stride", 6, "Starting at 6th level, moving through nonmagical "
    "difficult terrain costs you no extra movement. You can also pass through "
    "nonmagical plants without being slowed by them and without taking damage "
    "from them if they have thorns, spines, or a similar hazard.\n\nIn addition, "
    "you have advantage on saving throws against plants that are magically created "
    "or manipulated to impede movement, such as those created by the Entangle spell."),
    (5, 1, "Nature's Ward", 10, "When you reach 10th level, you can't be charmed or "
    "frightened by elementals or fey, and you are immune to poison and disease."),
    (5, 1, "Nature's Sanctuary", "When you reach 14th level, creatures of the natural "
    "world sense your connection to nature and become hesitant to attack you. When a "
    "beast or plant creature attacks you, that creature must make a Wisdom saving "
    "throw against your druid spell save DC. On a failed save, the creature must "
    "choose a different target, or the attack automatically misses. On a successful "
    "save, the creature is immune to this effect for 24 hours.\n\nThe creature is "
    "aware of this effect before it makes its attack against you."),
    (5, 2, "Combat Wild Shape", 2, "When you choose this circle at 2nd level, you gain "
    "the ability to use Wild Shape on your turn as a bonus action, rather than as an "
    "action.\n\nAdditionally, while you are transformed by Wild Shape, you can use "
    "a bonus action to expend one spell slot to regain 1d8 hit points per level "
    "of the spell slot expended."),
    (5, 2, "Circle Forms", 2, "The rites of your circle grant you the ability to "
    "transform into more dangerous animal forms. Starting at 2nd level, you can use "
    "your Wild Shape to transform into a beast with a challenge rating as high as 1. "
    "You ignore the Max. CR column of the Beast Shapes table, but must abide by the "
    "other limitations there.\n\nStarting at 6th level, you can transform into a "
    "beast with a challenge rating as high as your druid level divided by 3, rounded down."),
    (5, 2, "Primal Strike", 6, "Starting at 6th level, your attacks in beast form "
    "count as magical for the purpose of overcoming resistance and immunity to nonmagical "
    "attacks and damage."),
    (5, 2, "Elemental Wild Shape", 10, "At 10th level, you can expend two uses of Wild Shape "
    "at the same time to transform into an air elemental, an earth elemental, a fire "
    "elemental, or a water elemental."),
    (5, 2, "Thousand Forms", 14, "By 14th level, you have learned to use magic to alter "
    "your physical form in more subtle ways. You can cast the Alter Self spell at will."),
    (6, 1, "Combat Superiority", 3, "When you choose this archetype at 3rd level, you learn "
    "maneuvers that are fueled by special dice called superiority dice.\n\nManeuvers. You "
    "learn three maneuvers of your choice. Many maneuvers enhance an attack in some way. "
    "You can use only one maneuver per attack. You learn two additional maneuvers of your "
    "choice at 7th, 10th, and 15th level. Each time you learn new maneuvers, you can also "
    "replace one maneuver you know with a different one.\n\nSuperiority Dice. You have four "
    "superiority dice, which are d8s. A superiority die is expended when you use it. You "
    "regain all of your expended superiority dice when you finish a short or long rest. "
    "You gain another superiority die at 7th level and one more at 15th level.\n\nSaving Throws. "
    "Some of your maneuvers require your target to make a saving throw to resist the "
    "maneuver's effects. The saving throw DC is calculated as follows:\n\nManeuver save DC "
    "= 8 + your proficiency bonus + your Strength or Dexterity modifier (your choice)"),
    (6, 1, "Student of War", 3, "At 3rd level, you gain proficiency with one type of "
    "artisan's tools of your choice."),
    (6, 1, "Know Your Enemy", 7, "Starting at 7th level, if you spend at least 1 minute "
    "observing or interacting with another creature outside combat, you can learn certain "
    "information about its capabilities compared to your own. The DM tells you if the "
    "creature is your equal, superior, or inferior in regard to two of the following "
    "characteristics of your choice:\n\t" + chr(9679) + "Strength score\n\t" + chr(9679) + 
    "Dexterity score\n\t" + chr(9679) + "Constitution score\n\t" + chr(9679) + "Armor Class\n\t"
    + chr(9679) + "Current hit points\n\t" + chr(9679) + "Total class levels, if any\n\t" + chr(9679)
    + "Fighter class levels, if any"),
    (6, 1, "Improved Combat Superiority", 10, "At 10th level, your superiority dice turn into "
    "d10s. At 18th level, they turn into d12s."),
    (6, 1, "Relentless", 15, "Starting at 15th level, when you roll initiative and have no superiority "
    "dice remaining, you regain 1 superiority die."),
    (6, 1, "Improved Combat Superiority(d12)", 18, "At 18th level, they turn into d12s."),
    (6, 2, "Improved Critical", 3, "Beginning when you choose this archetype at 3rd level, your "
    "weapon attacks score a critical hit on a roll of 19 or 20."),
    (6, 2, "Remarkable Athlete", 7, "Starting at 7th level, you can add half your proficiency "
    "bonus (rounded up) to any Strength, Dexterity, or Constitution check you make that doesn't "
    "already use your proficiency bonus.\n\nIn addition, when you make a running long jump, "
    "the distance you can cover increases by a number of feet equal to your Strength modifier."),
    (6, 2, "Additional Fighting Style", 10, "At 10th level, you can choose a second option from "
    "the Fighting Style class feature."),
    (6, 2, "Superior Critical", 15, "Starting at 15th level, your weapon attacks score a "
    "critical hit on a roll of 18-20."),
    (6, 2, "Survivor", 18, "At 18th level, you attain the pinnacle of resilience in battle. "
    "At the start of each of your turns, you regain hit points equal to 5 + your Constitution "
    "modifier if you have no more than half of your hit points left. You don't gain this "
    "benefit if you have 0 hit points.")
    (7, 1, "Open Hand Technique", 3, "Starting when you choose this tradition at 3rd level, "
    "you can manipulate your enemy's ki when you harness your own. Whenever you hit a creature "
    "with one of the attacks granted by your Flurry of Blows, you can impose one of the "
    "following effects on that target:\n\t" + chr(9679) + "It must succeed on a Dexterity saving "
    "throw or be knocked prone.\n\t" + chr(9679) + "It must make a Strength saving throw. "
    "If it fails, you can push it up to 15 feet away from you.\n\t" + chr(9679) + "It can't "
    "take reactions until the end of your next turn."),
    (7, 1, "Wholeness of Body", 6, "At 6th level, you gain the ability to heal yourself. As an "
    "action, you can regain hit points equal to three times your monk level. You must finish a "
    "long rest before you can use this feature again."),
    (7, 1, "Tranquility", 11, "Beginning at 11th level, you can enter a special meditation that "
    "surrounds you with an aura of peace. At the end of a long rest, you gain the effect of a "
    "Sanctuary spell that lasts until the start of your next long rest (the spell can end early "
    "as normal). The saving throw DC for the spell equals 8 + your Wisdom modifier + your "
    "proficiency bonus."),
    (7, 1, "Quivering Palm", 17, "At 17th level, you gain the ability to set up lethal "
    "vibrations in someone's body. When you hit a creature with an unarmed strike, you can "
    "spend 3 ki points to start these imperceptible vibrations, which last for a number of "
    "days equal to your monk level. The vibrations are harmless unless you use your action "
    "to end them. To do so, you and the target must be on the same plane of existence. "
    "When you use this action, the creature must make a Constitution saving throw. If it "
    "fails, it is reduced to 0 hit points. If it succeeds, it takes 10d10 necrotic damage.\n\nYou "
    "can have only one creature under the effect of this feature at a time. You can choose "
    "to end the vibrations harmlessly without using an action."),
    (7, 2, "Shadow Arts", 3, "Starting when you choose this tradition at 3rd level, you can "
    "use your ki to duplicate the effects of certain spells. As an action, you can spend "
    "2 ki points to cast darkness, darkvision, pass without trace, or silence, without "
    "providing material components. Additionally, you gain the minor illusion cantrip "
    "if you don't already know it."),
    (7, 2, "Shadow Step", 6, "At 6th level, you gain the ability to step from one shadow "
    "into another. When you are in dim light or darkness, as a bonus action you can "
    "teleport up to 60 feet to an unoccupied space you can see that is also in dim "
    "light or darkness. You then have advantage on the first melee attack you make before "
    "the end of the turn."),
    (7, 2, "Cloack of Shadows", 11, "By 11th level, you have learned to become one with "
    "the shadows. When you are in an area of dim light or darkness, you can use your "
    "action to become invisible. You remain invisible until you make an attack, cast a "
    "spell, or are in an area of bright light."),
    (7, 2, "Opportunist", 17, "At 17th level, you can exploit a creature's momentary "
    "distraction when it is hit by an attack. Whenever a creature within 5 feet of you "
    "is hit by an attack made by a creature other than you, you can use your reaction "
    "to make a melee attack against that creature."),
    (8, 1, "Tenets of the Ancients", 3, "The tenets of the Oath of the Ancients have "
    "been preserved for uncounted centuries. This oath emphasizes the principles of "
    "good above any concerns of law or chaos. Its four central principles are simple.\n\n"
    "Kindle the Light. Through your acts of mercy, kindness, and forgiveness, kindle "
    "the light of hope in the world, beating back despair.\n\nShelter the Light. Where "
    "there is good, beauty, love, and laughter in the world, stand against the wickedness "
    "that would swallow it. Where life flourishes, stand against the forces that would "
    "render it barren.\n\nPreserve Your Own Light. Delight in song and laughter, in "
    "beauty and art. If you allow the light to die in your own heart, you can't preserve "
    "it in the world.\n\nBe the Light. Be a glorious beacon for all who live in despair. "
    "Let the light of your joy and courage shine forth in all your deeds."),
    (8, 1, "Channel Divinity", 3, "When you take this oath at 3rd level, you gain the following "
    "two Channel Divinity options.\n\t" + chr(9679) + "Nature's Wrath. You can use your "
    "Channel Divinity to invoke primeval forces to ensnare a foe. As an action, you can "
    "cause spectral vines to spring up and reach for a creature within 10 feet of you that "
    "you can see. The creature must succeed on a Strength or Dexterity saving throw (its "
    "choice) or be restrained. While restrained by the vines, the creature repeats the "
    "saving throw at the end of each of its turns. On a success, it frees itself and "
    "the vines vanish.\n\t" + chr(9679) + "Turn the Faithless. You can use your Channel "
    "Divinity to utter ancient words that are painful for fey and fiends to hear. As "
    "an action, you present your holy symbol, and each fey or fiend within 30 feet of "
    "you that can hear you must make a Wisdom saving throw. On a failed save, the "
    "creature is turned for 1 minute or until it takes damage.\n\nA turned creature must "
    "spend its turns trying to move as far away from you as it can, and it can't willingly "
    "move to a space within 30 feet of you. It also can't take reactions. For its action, "
    "it can use only the Dash action or try to escape from an effect that prevents it "
    "from moving. If there's nowhere to move, the creature can use the Dodge action.\n\nIf "
    "the creature's true form is concealed by an illusion, shapeshifting, or other "
    "effect, that form is revealed while it is turned."),
    (8, 1, "Aura of Warding", 7, "Beginning at 7th level, ancient magic lies so heavily "
    "upon you that it forms an eldritch ward. You and friendly creatures within 10 "
    "feet of you have resistance to damage from spells.\n\nAt 18th level, the range "
    "of this aura increases to 30 feet."),
    (8, 1, "Undying Sentinel", 15, "Starting at 15th level, when you are reduced to "
    "0 hit points and are not killed outright, you can choose to drop to 1 hit point "
    "instead. Once you use this ability, you can't use it again until you finish a "
    "long rest.\n\nAdditionally, you suffer none of the drawbacks of old age, and "
    "you can't be aged magically."),
    (8, 1, "Aura of Warding (30 feet", 18, "At 18th level, the range of this aura "
    "increases to 30 feet."),
    (8, 1, "Elder Champion", 20, "At 20th level, you can assume the form of an "
    "ancient force of nature, taking on an appearance you choose. For example, your "
    "skin might turn green or take on a bark-like texture, your hair might become leafy "
    "or moss-like, or you might sprout antlers or a lion-like mane.\n\nUsing your "
    "action, you undergo a transformation. For 1 minute, you gain the following "
    "benefits:\n\t" + chr(9679) + "At the start of each of your turns, you regain "
    "10 hit points.\n\t" + chr(9697) + "Whenever you cast a paladin spell that has "
    "a casting time of 1 action, you can cast it using a bonus action instead.\n\t" + chr(9679) + 
    "Enemy creatures within 10 feet of you have disadvantage on saving throws against "
    "your paladin spells and Channel Divinity options.\n\nOnce you use this feature, "
    "you can't use it again until you finish a long rest."),
    (8, 2, "Tenets of Vengeance", 3, "The tenets of the Oath of Vengeance vary by "
    "paladin, but all the tenets revolve around punishing wrongdoers by any means "
    "necessary. Paladins who uphold these tenets are willing to sacrifice even their "
    "own righteousness to mete out justice upon those who do evil, so the paladins "
    "are often neutral or lawful neutral in alignment. The core principles of the "
    "tenets are brutally simple.\n\nFight the Greater Evil. Faced with a choice of "
    "fighting my sworn foes or combating a lesser evil, I choose the greater evil.\n\nNo "
    "Mercy for the Wicked. Ordinary foes might win my mercy, but my sworn enemies do "
    "not.\n\nBy Any Means Necessary. My qualms can't get in the way of exterminating "
    "my foes.\n\nRestitution. If my foes wreak ruin on the world, it is because I "
    "failed to stop them. I must help those harmed by their misdeeds."),
    (8, 2, "Channel Divinity", 3, "When you take this oath at 3rd level, you gain the "
    "following two Channel Divinity options.\n\t" + chr(9679) + "Abjure Enemy. As an "
    "action, you present your holy symbol and speak a prayer of denunciation, using "
    "your Channel Divinity. Choose one creature within 60 feet of you that you can "
    "see. That creature must make a Wisdom saving throw, unless it is immune to "
    "being frightened. Fiends and undead have disadvantage on this saving throw.\n\nOn "
    "a failed save, the creature is frightened for 1 minute or until it takes any "
    "damage. While frightened, the creature's speed is 0, and it can't benefit from "
    "any bonus to its speed.\n\nOn a successful save, the creature's speed is halved "
    "for 1 minute or until the creature takes any damage.\n\t" + chr(9679) + "Vow of "
    "Enmity. As a bonus action, you can utter a vow of enmity against a creature you 
    "can see within 10 feet of you, using your Channel Divinity. You gain advantage "
    "on attack rolls against the creature for 1 minute or until it drops to 0 hit "
    "points or falls unconscious."),
    (8, 2, "Relentless Avenger", 7, "By 7th level, your supernatural focus helps you "
    "close off a foe's retreat. When you hit a creature with an opportunity attack, "
    "you can move up to half your speed immediately after the attack and as part of "
    "the same reaction. This movement doesn't provoke opportunity attacks."),
    (8, 2, "Soul of Vengeance", 15, "Starting at 15th level, the authority with which "
    "you speak your Vow of Enmity gives you greater power over your foe. When a "
    "creature under the effect of your Vow of Enmity makes an attack, you can use "
    "your reaction to make a melee weapon attack against that creature if it is "
    "within range."),
    (8, 2, "Avenging Angel", 20, "At 20th level, you can assume the form of an "
    "angelic avenger. Using your action, you undergo a transformation. For 1 hour, "
    "you gain the following benefits:\n\t" + chr(9679) + "Wings sprout from your "
    "back and grant you a flying speed of 60 feet.\n\t" + chr(9679) + "You emanate "
    "an aura of menace in a 30-foot radius. The first time any enemy creature enters "
    "the aura or starts its turn there during a battle, the creature must succeed on "
    "a Wisdom saving throw or become frightened of you for 1 minute or until it takes "
    "any damage. Attack rolls against the frightened creature have advantage.\n\nOnce "
    "you use this feature, you can't use it again until you finish a long rest."),
    (9, 1, "Gloom Stalker Magic", 3, "Starting at 3rd level, you learn an additional "
    "spell when you reach certain levels in this class, as shown in the Gloom Stalker "
    "Spells table. The spell counts as a ranger spell for you, but it doesn't count "
    "against the number of ranger spells you know."),
    (9, 1, "Dread Ambusher", 3, "At 3rd level, you master the art of the ambush. You "
    "can give yourself a bonus to your initiative rolls equal to your Wisdom modifier.\n\nAt "
    "the start of your first turn of each combat, your walking speed increases by 10 "
    "feet, which lasts until the end of that turn. If you take the Attack action on "
    "that turn, you can make one additional weapon attack as part of that action. If "
    "that attack hits, the target takes an extra 1d8 damage of the weapon's damage type."),
    (9, 1, "Umbral Sight", 3, "At 3rd level, you gain darkvision out to a range of 60 "
    "feet. If you already have darkvision from your race, its range increases by 30 feet.\n\nYou "
    "are also adept at evading creatures that rely on darkvision. While in darkness, you "
    "are invisible to any creature that relies on darkvision to see you in that darkness."),
    (9, 1, "Iron Mind", 7, "By 7th level, you have honed your ability to resist the mind-"
    "altering powers of your prey. You gain proficiency in Wisdom saving throws. If you "
    "already have this proficiency, you instead gain proficiency in Intelligence or "
    "Charisma saving throws (your choice)."),
    (9, 1, "Stalker's Fury", 11, "At 11th level, you learn to attack with such unexpected "
    "speed that you can turn a miss into another strike. Once on each of your turns when "
    "you miss with a weapon attack, you can make another weapon attack as part of the same action."),
    (9, 1, "Shadowy Dodge", 15, "Starting at 15th level, you can dodge in unforeseen ways, "
    "with wisps of supernatural shadow around you. Whenever a creature makes an attack roll "
    "against you and doesn't have advantage on the roll, you can use your reaction to impose "
    "disadvantage on it. You must use this feature before you know the outcome of the attack roll."),
    (9, 2, "Hunter's Prey", 3 "At 3rd level, you gain one of the following features of your "
    "choice.\n\t" + chr(9697) + "Colossus Slayer. Your tenacity can wear down the most potent "
    "foes. When you hit a creature with a weapon attack, the creature takes an extra 1d8 damage "
    "if it’s below its hit point maximum. You can deal this extra damage only once per "
    "turn.\n\t" + chr(9679) + "Giant Killer. When a Large or larger creature within 5 feet "
    "of you hits or misses you with an attack, you can use your reaction to attack that "
    "creature immediately after its attack, provided that you can see the creature.\n\t" + chr(9679) +
    "Horde Breaker. Once on each of your turns when you make a weapon attack, you can make "
    "another attack with the same weapon against a different creature that is within 5 feet "
    "of the original target and within range of your weapon."),
    (9, 2, "Defensive Tactics", 7, "At 7th level, you gain one of the following features "
    "of your choice.\n\t" + chr(9679) + "Escape the Horde. Opportunity attacks against you "
    "are made with disadvantage.\n\t" + chr(9679) + "Multiattack Defense. When a creature "
    "hits you with an attack, you gain a +4 bonus to AC against all subsequent attacks made "
    "by that creature for the rest of the turn.\n\t" + chr(9679) + "Steel Will. You have "
    "advantage on saving throws against being frightened."),
    (9, 2, "Multiattack", 11, "At 11th level, you gain one of the following features of "
    "your choice.\n\t" + chr(9679), + "Volley. You can use your action to make a ranged "
    "attack against any number of creatures within 10 feet of a point you can see within "
    "your weapon’s range. You must have ammunition for each target, as normal, and you "
    "make a separate attack roll for each target." + chr(9679) + "Whirlwind Attack. You "
    "can use your action to make melee attacks against any number of creatures within "
    "5 feet of you, with a separate attack roll for each target."),
    (9, 2, "Superior Hunter's Defense", 15, "At 15th level, you gain one of the following "
    "features of your choice.\n\t" + chr(9679) + "Evasion. When you are subjected to an "
    "effect, such as a red dragon’s fiery breath or a lightning bolt spell, that allows you "
    "to make a Dexterity saving throw to take only half damage, you instead take no damage "
    "if you succeed on a saving throw, and only half damage if you fail.\n\t" + chr(9679) + "Stand "
    "Against the Tide. When a hostile creature misses you with a melee attack, you can use "
    "your reaction to force that creature to repeat the same attack against another "
    "creature (other than itself) of your choice.\n\t" + chr(9679) + "Uncanny Dodge. When "
    "an attacker that you can see hits you with an attack, you can use your reaction "
    "to halve the attack’s damage against you."),
    (10, 1, "Spellcasting", 3, "When you reach 3rd level, you augment your martial prowess "
    "with the ability to cast spells.\n\nCantrips\n\nYou learn three cantrips: Mage Hand "
    "and two other cantrips of your choice from the wizard spell list. You learn another "
    "wizard cantrip of your choice at 10th level.\n\nSpell Slots\n\nThe Arcane Trickster "
    "Spellcasting table shows how many spell slots you have to cast your wizard spells "
    "of 1st level and higher. To cast one of these spells, you must expend a slot of the "
    "spell's level or higher. You regain all expended spell slots when you finish a "
    "long rest.\n\nFor example, if you know the 1st-level spell Charm Person and have "
    "a 1st-level and a 2nd-level spell slot available, you can cast Charm Person using "
    "either slot.\n\nSpells Known of 1st Level and Higher\n\nYou know three 1st-level "
    "wizard spells of your choice, two of which you must choose from the enchantment "
    "and illusion spells on the wizard spell list.\n\nThe Spells Known column of the "
    "Arcane Trickster Spellcasting table shows when you learn more wizard spells of "
    "1st level or higher. Each of these spells must be an enchantment or illusion "
    "spell of your choice, and must be of a level for which you have spell slots. For "
    "instance, when you reach 7th level in this class, you can learn one new spell of "
    "1st or 2nd level.\n\nThe spells you learn at 8th, 14th, and 20th level can come "
    "from any school of magic.\n\nWhenever you gain a level in this class, you can "
    "replace one of the wizard spells you know with another spell of your choice from "
    "the wizard spell list. The new spell must be of a level for which you have spell "
    "slots, and it must be an enchantment or illusion spell, unless you're replacing "
    "the spell you gained at 3rd, 8th, 14th, or 20th level from any school of magic.\n\nSpellcasting "
    "Ability\n\nIntelligence is your spellcasting ability for your wizard spells, since "
    "you learn your spells through dedicated study and memorization. You use your Intelligence "
    "whenever a spell refers to your spellcasting ability. In addition, you use your "
    "Intelligence modifier when setting the saving throw DC for a wizard spell you "
    "cast and when making an attack roll with one.\n\tSpell save DC = 8 + your proficiency "
    "bonus + your Intelligence modifier\n\tSpell attack modifier = your proficiency "
    "bonus + your Intelligence modifier"),
    (10, 1, "Mage Hand Legerdemain", 3, "Starting at 3rd level, when you cast Mage Hand, "
    "you can make the spectral hand invisible, and you can perform the following "
    "additional tasks with it:\n\t" + chr(9679) + "You can stow one object the hand is "
    "holding in a container worn or carried by another creature.\n\t" + chr(9679) + "You can "
    "retrieve an object in a container worn or carried by another creature.\n\t" + chr(9679) + "You "
    "can use thieves' tools to pick locks and disarm traps at range.\n\nYou can perform one "
    "of these tasks without being noticed by a creature if you succeed on a Dexterity (Sleight "
    "of Hand) check contested by the creature's Wisdom (Perception) check.\n\nIn addition, "
    "you can use the bonus action granted by your Cunning Action to control the hand."),
    (10, 1, "Magical Ambush", 9, "Starting at 9th level, if you are hidden from a creature "
    "when you cast a spell on it, the creature has disadvantage on any saving throw it makes "
    "against the spell this turn."),
    (10, 1, "Versatile Trickster", 13, "At 13th level, you gain the ability to distract targets "
    "with your Mage Hand. As a bonus action on your turn, you can designate a creature within "
    "5 feet of the spectral hand created by the spell. Doing so gives you advantage on attack "
    "rolls against that creature until the end of the turn."),
    (10, 1, "Spell Thief", 17, "At 17th level, you gain the ability to magically steal the "
    "knowledge of how to cast a spell from another spellcaster.\n\nImmediately after a creature "
    "casts a spell that targets you or includes you in its area of effect, you can use your "
    "reaction to force the creature to make a saving throw with its spellcasting ability "
    "modifier. The DC equals your spell save DC. On a failed save, you negate the spell's "
    "effect against you, and you steal the knowledge of the spell if it is at least 1st "
    "level and of a level you can cast (it doesn't need to be a wizard spell). For the "
    "next 8 hours, you know the spell and can cast it using your spell slots. The creature "
    "can't cast that spell until the 8 hours have passed.\n\nOnce you use this feature, "
    "you can't use it again until you finish a long rest."),
    (10, 2, "Bonus Proficiencies", 3, "When you choose this archetype at 3rd level, you "
    "gain proficiency with the disguise kit and the poisoner's kit."),
    (10, 2, "Assassinate", 3 "Starting at 3rd level, you are at your deadliest when you "
    "get the drop on your enemies. You have advantage on attack rolls against any creature "
    "that hasn't taken a turn in the combat yet. In addition, any hit you score against "
    "a creature that is surprised is a critical hit."),
    (10, 2, "Infiltration Expertise", 9, "Starting at 9th level, you can unfailingly create "
    "false identities for yourself. You must spend seven days and 25 gp to establish the "
    "history, profession, and affiliations for an identity. You can't establish an identity "
    "that belongs to someone else. For example, you might acquire appropriate clothing, letters "
    "of introduction, and official- looking certification to establish yourself as a "
    "member of a trading house from a remote city so you can insinuate yourself into the company "
    "of other wealthy merchants.\n\nThereafter, if you adopt the new identity as a disguise, "
    "other creatures believe you to be that person until given an obvious reason not to."),
    (10, 2, "Imposter", 13, "At 13th level, you gain the ability to unerringly mimic another "
    "person's speech, writing, and behavior. You must spend at least three hours studying these "
    "three components of the person's behavior, listening to speech, examining handwriting, "
    "and observing mannerisms.\n\nYour ruse is indiscernible to the casual observer. If a "
    "wary creature suspects something is amiss, you have advantage on any Charisma (Deception) "
    "check you make to avoid detection."),
    (10, 2, "Death Strike", 17, "Starting at 17th level, you become a master of instant death. "
    "When you attack and hit a creature that is surprised, it must make a Constitution saving "
    "throw (DC 8 + your Dexterity modifier + your proficiency bonus). On a failed save, double "
    "the damage of your attack against the creature."),
    (11, 1, "Divine Magic", 1, "Your link to the divine allows you to learn spells normally "
    "associated with the cleric class. When your Spellcasting feature lets you learn a sorcerer "
    "cantrip or a sorcerer spell of 1st level or higher, you can choose the new spell from the "
    "cleric spell list or the sorcerer spell list. You must otherwise obey all the restrictions "
    "for selecting the spell, and it becomes a sorcerer spell for you.\n\nIn addition, choose an "
    "affinity for the source of your divine power: good, evil, law, chaos, or neutrality. You "
    "learn an additional spell based on that affinity, as shown below. It is a sorcerer spell "
    "for you, but it doesn't count against your number of sorcerer spells known. If you later "
    "replace this spell, you must replace it with a spell from the cleric spell list."),
    (11, 1, "Favored by the Gods", 1, "Starting at 1st level, divine power guards your destiny. "
    "If you fail a saving throw or miss with an attack roll, you can roll 2d4 and add it to "
    "the total, possibly changing the outcome.\n\nOnce you use this feature, you can't use "
    "it again until you finish a short or long rest"),
    (11, 1, "Empowered Healing", 6, "Starting at 6th level, the divine energy coursing through "
    "you can empower healing spells. Whenever you or an ally within 5 feet of you rolls "
    "dice to determine the number of hit points a spell restores, you can spend 1 sorcery "
    "point to reroll any number of those dice once, provided you aren't incapacitated. You "
    "can use this feature only once per turn."),
    (11, 1, "Angelic Form", 14, "Starting at 14th level, you can use a bonus action to "
    "manifest a pair of spectral wings from your back. While the wings are present, you have "
    "a flying speed of 30 feet. The wings last until you're incapacitated, you die, or you "
    "dismiss them as a bonus action.\n\nThe affinity you chose for your Divine Magic feature "
    "determines the appearance of the spectral wings: eagle wings for good or law, bat wings "
    "for evil or chaos, and dragonfly wings for neutrality."),
    (11, 1, "Unarthly Recovery", 18, "At 18th level, you gain the ability to overcome grievous "
    "injuries. As a bonus action when you have fewer than half of your hit points remaining, "
    "you can regain a number of hit points equal to half your hit point maximum.\n\nOnce you "
    "use this feature, you can’t use it again until you finish a long rest."),
    (11, 2, "At 1st level, you choose one type of dragon as your ancestor. The damage type "
    "associated with each dragon is used by features you gain later.\n\nYou can speak, read, "
    "and write Draconic. Additionally, whenever you make a Charisma check when interacting "
    "with dragons, your proficiency bonus is doubled if it applies to the check."),
    (11, 2, "Draconic Resilience", 1, "As magic flows through your body, it causes physical "
    "traits of your dragon ancestors to emerge. At 1st level, your hit point maximum increases "
    "by 1 and increases by 1 again whenever you gain a level in this class.\n\nAdditionally, "
    "parts of your skin are covered by a thin sheen of dragon-like scales. When you aren't "
    "wearing armor, your AC equals 13 + your Dexterity modifier."),
    (11, 2, "Elemental Affinity", 6, "Starting at 6th level, when you cast a spell that deals "
    "damage of the type associated with your draconic ancestry, add your Charisma modifier "
    "to one damage roll of that spell. At the same time, you can spend 1 sorcery point to "
    "gain resistance to that damage type for 1 hour."),
    (11, 2, "Dragon Wings", 14, "At 14th level, you gain the ability to sprout a pair of "
    "dragon wings from your back, gaining a flying speed equal to your current speed. You "
    "can create these wings as a bonus action on your turn. They last until you dismiss "
    "them as a bonus action on your turn.\n\nYou can't manifest your wings while wearing "
    "armor unless the armor is made to accommodate them, and clothing not made to accommodate "
    "your wings might be destroyed when you manifest them."),
    (11, 2, "Draconic Presence", 18, "Beginning at 18th level, you can channel the dread "
    "presence of your dragon ancestor, causing those around you to become awestruck or "
    "frightened. As an action, you can spend 5 sorcery points to draw on this power and "
    "exude an aura of awe or fear (your choice) to a distance of 60 feet. For 1 minute "
    "or until you lose your concentration (as if you were casting a concentration spell), "
    "each hostile creature that starts its turn in this aura must succeed on a Wisdom "
    "saving throw or be charmed (if you chose awe) or frightened (if you chose fear) until "
    "the aura ends. A creature that succeeds on this saving throw is immune to your aura for 24 hours."),
    (12, 1, "Expanded Spell List", 1, "The Fiend lets you choose from an expanded list of "
    "spells when you learn a warlock spell. The following spells are added to the warlock "
    "spell list for you."),
    (12, 1, "Dark One's Blessing", 1, "Starting at 1st level, when you reduce a hostile "
    "creature to 0 hit points, you gain temporary hit points equal to your Charisma modifier "
    "+ your warlock level (minimum of 1)."),
    (12, 1, "Dark One's Own Luck", 6, "Starting at 6th level, you can call on your patron "
    "to alter fate in your favor. When you make an ability check or a saving throw, you "
    "can use this feature to add a d10 to your roll. You can do so after seeing the initial "
    "roll but before any of the roll's effects occur.\n\nOnce you use this feature, you "
    "can't use it again until you finish a short or long rest."),
    (12, 1, "Fiendish Reslience", 10, "Starting at 10th level, you can choose one damage "
    "type when you finish a short or long rest. You gain resistance to that damage type "
    "until you choose a different one with this feature. Damage from magical weapons or "
    "silver weapons ignores this resistance."),
    (12, 1, "Hurl Through Hell", 14, "Starting at 14th level, when you hit a creature with "
    "an attack, you can use this feature to instantly transport the target through the "
    "lower planes. The creature disappears and hurtles through a nightmare landscape.\n\nAt "
    "the end of your next turn, the target returns to the space it previously occupied, or "
    "the nearest unoccupied space. If the target is not a fiend, it takes 10d10 psychic "
    "damage as it reels from its horrific experience.\n\nOnce you use this feature, you "
    "can't use it again until you finish a long rest."),
    (12, 2, "Expanded Spell List", 1, "The Hexblade lets you choose from an expanded list "
    "of spells when you learn a warlock spell. The following spells are added to the "
    "warlock spell list for you."),
    (12, 2, "Hexblade's Curse", 1, "Starting at 1st level, you gain the ability to place "
    "a baleful curse on someone. As a bonus action, choose one creature you can see within "
    "30 feet of you. The target is cursed for 1 minute. The curse ends early if the target "
    "dies, you die, or you are incapacitated. Until the curse ends, you gain the following "
    "benefits:\n\t" + chr(9679) + "You gain a bonus to damage rolls against the cursed "
    "target. The bonus equals your proficiency bonus.\n\t" + chr(9679) + "Any attack roll "
    "you make against the cursed target is a critical hit on a roll of 19 or 20 on the "
    "d20.\n\t" + chr(9679) + "If the cursed target dies, you regain hit points equal to "
    "your warlock level + your Charisma modifier (minimum of 1 hit point).\n\nYou can't use "
    "this feature again until you finish a short or long rest."),
    (12, 2, "Hex Warrior", 1, "At 1st level, you acquire the training necessary to effectively "
    "arm yourself for battle. You gain proficiency with medium armor, shields, and martial "
    "weapons.\n\nThe influence of your patron also allows you to mystically channel your "
    "will through a particular weapon. Whenever you finish a long rest, you can touch one "
    "weapon that you are proficient with and that lacks the two-handed property. When you "
    "attack with that weapon, you can use your Charisma modifier, instead of Strength or "
    "Dexterity, for the attack and damage rolls. This benefit lasts until you finish a "
    "long rest. If you later gain the Pact of the Blade feature, this benefit extends "
    "to every pact weapon you conjure with that feature, no matter the weapon's type."),
    (12, 2, "Accursed Spector", 6, "Starting at 6th level, you can curse the soul of a "
    "person you slay, temporarily binding it in your service. When you slay a humanoid, "
    "you can cause its spirit to rise from its corpse as a specter, the statistics of "
    "which are in the Monster Manual. When the specter appears, it gains temporary hit "
    "points equal to half your warlock level. Roll initiative for the specter, which "
    "has its own turns. It obeys your verbal commands, and it gains a special bonus "
    "to its attack rolls equal to your Charisma modifier (minimum of +0).\n\nThe specter "
    "remains in your service until the end of your next long rest, at which point it "
    "vanishes to the afterlife.\n\nOnce you bind a specter with this feature, you can't "
    "use the feature again until you finish a long rest."),
    (12, 2, "Armor of Hexes", 10, "At 10th level, your hex grows more powerful. If the "
    "target cursed by your Hexblade’s Curse hits you with an attack roll, you can use "
    "your reaction to roll a d6. On a 4 or higher, the attack instead misses you, "
    "regardless of its roll."),
    (12, 2, "Master of Hexes", 14, "Starting at 14th level, you can spread your Hexblade's "
    "Curse from a slain creature to another creature. When the creature cursed by your "
    "Hexblade's Curse dies, you can apply the curse to a different creature you can "
    "see within 30 feet of you, provided you aren't incapacitated. When you apply the "
    "curse in this way, you don't regain hit points from the death of the "
    "previously cursed creature."),
    (13, 1, "Abjuration Savant", 2, "Beginning when you select this school at 2nd "
    "level, the gold and time you must spend to copy an abjuration spell into your "
    "spellbook is halved."),
    (13, 1, "Arcane Ward", 2, "Starting at 2nd level, you can weave magic around "
    "yourself for protection. When you cast an abjuration spell of 1st level or "
    "higher, you can simultaneously use a strand of the spell's magic to create "
    "a magical ward on yourself that lasts until you finish a long rest. The ward "
    "has hit points equal to twice your wizard level + your Intelligence modifier. "
    "Whenever you take damage, the ward takes the damage instead. If this damage "
    "reduces the ward to 0 hit points, you take any remaining damage.\n\nWhile the "
    "ward has 0 hit points, it can't absorb damage, but its magic remains. Whenever "
    "you cast an abjuration spell of 1st level or higher, the ward regains a number "
    "of hit points equal to twice the level of the spell.\n\nOnce you create the "
    "ward, you can't create it again until you finish a long rest."),
    (13, 1, "Projected Ward", 6, "Starting at 6th level, when a creature that you "
    "can see within 30 feet of you takes damage, you can use your reaction to cause "
    "your Arcane Ward to absorb that damage. If this damage reduces the ward to 0 "
    "hit points, the warded creature takes any remaining damage."),
    (13, 1, "Improved Abjuration", 10, "Beginning at 10th level, when you cast an "
    "abjuration spell that requires you to make an ability check as a part of casting "
    "that spell (as in Counterspell and Dispel Magic), you add your proficiency bonus "
    "to that ability check."),
    (13, 1, "Spell Resistance", 14, "Starting at 14th level, you have advantage on "
    "saving throws against spells.\n\nFurthermore, you have resistance against the "
    "damage of spells."),
    (13, 2, "Evocation Savant", 2, "Beginning when you select this school at 2nd "
    "level, the gold and time you must spend to copy a Evocation spell into your "
    "spellbook is halved."),
    (13, 2, "Sculpt Spells", 2, "Beginning at 2nd level, you can create pockets "
    "of relative safety within the effects of your evocation spells. When you cast "
    "an evocation spell that affects other creatures that you can see, you can "
    "choose a number of them equal to 1 + the spell's level. The chosen creatures "
    "automatically succeed on their saving throws against the spell, and they "
    "take no damage if they would normally take half damage on a successful save."),
    (13, 2, "Potent Cantrip", 6, "Starting at 6th level, your damaging cantrips affect "
    "even creatures that avoid the brunt of the effect. When a creature succeeds on "
    "a saving throw against your cantrip, the creature takes half the cantrip's "
    "damage (if any) but suffers no additional effect from the cantrip."),
    (13, 2, "Empowered Evocation", 6, "Beginning at 10th level, you can add your "
    "Intelligence modifier (minimum of +1) to one damage roll of any wizard "
    "evocation spell that you cast."),
    (13, 2, "Overchannel", 14, "Starting at 14th level, you can increase the power "
    "of your simpler spells. When you cast a wizard spell of 1st through 5th level "
    "that deals damage, you can deal maximum damage with that spell.\n\nThe first time "
    "you do so, you suffer no adverse effect. If you use this feature again before "
    "you finish a long rest, you take 2d12 necrotic damage for each level of the "
    "spell, immediately after you cast it. Each time you use this feature again before "
    "finishing a long rest, the necrotic damage per spell level increases by 1d12. "
    "This damage ignores resistance and immunity."),
    ]
c.executemany('INSERT INTO subclass_features (class_id, subclass_id, feature_name, level, description) VALUES (?, ?, ?, ?, ?)', subclass_features)




# Commit changes and close the connection
conn.commit()
conn.close()




# Example: Fetch and display features for Fighter (class_id 6)
main()
