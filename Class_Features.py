
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
    'unarmed strike or a monk weapon on your turn, you can make one unarmed strike as a "
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
    (9, "Favored Enemy", 1, "Choose a type of favored enemy: aberrations, beasts, celestials, constructs, dragons, elementals, fey, fiends, giants, monstrosities, oozes, plants, or undead. You gain advantages in tracking and knowing about them."),
    (9, "Natural Explorer", 1, "You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions."),
    (9, "Fighting Style", 2, "You adopt a particular style of fighting as your specialty. Choose from Archery, Defense, Dueling, or Two-Weapon Fighting."),
    (9, "Spellcasting", 2, "You can cast Ranger spells, using Wisdom as your spellcasting ability."),
    (9, "Primeval Awareness", 3, "You can use your action and expend one Ranger spell slot to focus your awareness on the region around you."),
    (9, "Ranger Archetype", 3, "Choose an archetype that grants you features at 3rd, 7th, 11th, and 15th levels."),
    (9, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
    (9, "Extra Attack", 5, "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
    (9, "Land's Stride", 8, "Moving through nonmagical difficult terrain costs you no extra movement."),
    (9, "Hide in Plain Sight", 10, "You can spend 1 minute creating camouflage for yourself."),
    (9, "Vanish", 14, "You can use the Hide action as a bonus action."),
    (9, "Feral Senses", 18, "You gain preternatural senses that help you fight creatures you can't see."),
    (9, "Foe Slayer", 20, "You become an unparalleled hunter of your enemies."),
    (9, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
    (9, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
    (9, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
    (9, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', ranger_features)

rogue_features = [
    (10, "Sneak Attack", 1, "You know how to strike subtly and exploit a foe's"
    "distraction. Your attacks deal extra damage when you have advantage on the"
    "attack roll."),
    (10, "Thieves' Cant", 1, "During your rogue training you learned thieves' cant"
    ", a secret mix of dialect, jargon, and code that allows you to hide messages"
    "in seemingly normal conversation."),
    (10, "Cunning Action", 2, "Your quick thinking and agility allow you to move"
    "and act quickly. You can take a bonus action to Dash, Disengage, or Hide."),
    (10, "Roguish Archetype", 3, "At 3rd level, you choose an archetype that you"
    "emulate in the exercise of your rogue abilities: Thief, Assassin, or Arcane Trickster."),
    (10, "Ability Score Improvement", 4, "When you reach 4th level, you can"
    "increase one ability score of your choice by 2, or you can increase two ability"
    "scores of your choice by 1."),
    (10, "Uncanny Dodge", 5, "Starting at 5th level, when an attacker that you can"
    "see hits you with an attack, you can use your reaction to halve the attack's damage."),
    (10, "Expertise", 6, "At 6th level, choose two more of your proficiencies in skills"
    "or your proficiency with thieves' tools. Your proficiency bonus is doubled for any"
    "ability check you make that uses either of the chosen proficiencies."),
    (10, "Evasion", 7, "Beginning at 7th level, you can nimbly dodge out of the way"
    "of certain area effects, such as a red dragon's fiery breath or an ice storm spell."),
    (10, "Ability Score Improvement", 8, "When you reach 8th level, you can increase"
    "one ability score of your choice by 2, or you can increase two ability scores"
    "of your choice by 1."),
    (10, "Roguish Archetype Feature", 9, "At 9th level, you gain a feature granted by"
    "your Roguish Archetype."),
    (10, "Ability Score Improvement", 10, "When you reach 10th level, you can increase"
    "one ability score of your choice by 2, or you can increase two ability scores"
    "of your choice by 1."),
    (10, "Reliable Talent", 11, "By 11th level, you have refined your chosen skills"
    "until they approach perfection. Whenever you make an ability check that lets you"
    "add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10."),
    (10, "Ability Score Improvement", 12, "When you reach 12th level, you can increase"
    "one ability score of your choice by 2, or you can increase two ability scores' of your choice by 1."),
    (10, "Roguish Archetype Feature", 13, "At 13th level, you gain a feature granted"
    "by your Roguish Archetype."),
    (10, "Blindsense", 14, "If you are able to hear, you are aware of the location"
    "of any hidden or invisible creature within 10 feet of you."),
    (10, "Slippery Mind", 15, "By 15th level, you have acquired greater mental strength."
    "You gain proficiency in Wisdom saving throws."),
    (10, "Ability Score Improvement", 16, "When you reach 16th level, you can increase"
    "one ability score of your choice by 2, or you can increase two ability scores"
    "of your choice by 1."),
    (10, "Roguish Archetype Feature", 17, "At 17th level, you gain a feature granted"
    "by your Roguish Archetype."),
    (10, "Elusive", 18, "Beginning at 18th level, you are so evasive that attackers"
    "rarely gain the upper hand against you. No attack roll has advantage against"
    "you while you aren’t incapacitated."),
    (10, "Ability Score Improvement", 19, "When you reach 19th level, you can"
    "increase one ability score of your choice by 2, or you can increase two"
    "ability scores of your choice by 1."),
    (10, "Stroke of Luck", 20, "At 20th level, you have an uncanny knack for"
    "succeeding when you need to. If your attack misses a target within range,"
    "you can turn the miss into a hit.")
]
c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', rogue_features)



sorcerer_features = [
    (11, "Spellcasting", 1, "You can cast Sorcerer spells, using Charisma as your spellcasting ability."),
    (11, "Sorcerous Origin", 1, "Choose a sorcerous origin, which grants you features at 1st, 6th, 14th, and 18th levels."),
    (11, "Font of Magic", 2, "You can use sorcery points to create spell slots or fuel special abilities."),
    (11, "Metamagic", 3, "You can twist your spells to suit your needs. Choose two Metamagic options."),
    (11, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
    (11, "Sorcerous Origin Feature", 6, "You gain a feature from your chosen sorcerous origin."),
    (11, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
    (11, "Sorcerous Origin Feature", 14, "You gain a feature from your chosen sorcerous origin."),
    (11, "Sorcerous Origin Feature", 18, "You gain a feature from your chosen sorcerous origin."),
    (11, "Sorcerous Restoration", 20, "You regain 4 expended sorcery points whenever you finish a short rest."),
    (11, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
    (11, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
    (11, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', sorcerer_features)



warlock_features = [
    (12, "Otherworldly Patron", 1, "You have made a pact with an otherworldly being that grants you magical powers. Your choice grants you features at 1st, 6th, 10th, and 14th levels."),
    (12, "Pact Magic", 1, "You can cast Warlock spells, using Charisma as your spellcasting ability. You regain expended spell slots after a short or long rest."),
    (12, "Eldritch Invocations", 2, "You gain two eldritch invocations of your choice, which enhance your abilities or give you new powers."),
    (12, "Pact Boon", 3, "Choose a boon from your patron that grants you features at 3rd level."),
    (12, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
    (12, "Mystic Arcanum (6th level)", 11, "You can cast one 6th-level spell once without expending a spell slot."),
    (12, "Mystic Arcanum (7th level)", 13, "You can cast one 7th-level spell once without expending a spell slot."),
    (12, "Mystic Arcanum (8th level)", 15, "You can cast one 8th-level spell once without expending a spell slot."),
    (12, "Mystic Arcanum (9th level)", 17, "You can cast one 9th-level spell once without expending a spell slot."),
    (12, "Eldritch Master", 20, "You can spend 1 minute entreating your patron to regain all your expended spell slots."),
    (12, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
    (12, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
    (12, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
    (12, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
]

c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', warlock_features)


wizard_features = [
    (13, "Spellcasting", 1, "You can cast Wizard spells, using Intelligence as your spellcasting ability."),
    (13, "Arcane Recovery", 1, "You can regain some of your magical energy by studying your spellbook during a short rest."),
    (13, "Arcane Tradition", 2, "Choose a school of magic to focus on, which grants you features at 2nd, 6th, 10th, and 14th levels."),
    (13, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
    (13, "Spell Mastery", 18, "You can cast a 1st-level or 2nd-level spell from your spellbook at its lowest level without expending a spell slot."),
    (13, "Signature Spells", 20, "You gain two 3rd-level Wizard spells that you can cast without expending spell slots."),
    (13, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
    (13, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
    (13, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
    (13, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
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
    (1, 3, "Artillerist", "You focus on crafting and using magical cannons and other artillery. By"
    "summoning arcane turrets, you can deal significant damage from a distance or provide defensive"
    "support to your allies, making you effective in both offensive and defensive strategies."),
    (1, 4, "Battle Smith", "You forge a strong bond with a clockwork animal construct that you create"
    "and command in battle. Along with some minor combat abilities, you also gain the ability to repair"
    "and reinforce both your construct and other equipment."),
    (2, 1, "Path of the Ancestral Guardian", "You invoke the spirits of your ancestors to protect yourself"
    "and your allies in battle. These ancestral spirits can shield your allies and deal extensive damage to your enemies."),
    (2, 2, "Path of the Battlerager", "Available only for dwarves, you harness your rage into a reckless and frenzied"
    "fighting style, using unique spiked armor as a weapon. This path allows you to excel in close combat, dealing"
    "additional damage to anyone foolish enough to come within your reach."),
    (2, 3, "Path of the Beast", "You channel the power of wild creatures, transforming physical aspects of your"
    "body to unleash devastating attacks. This includes sprouting claws, fangs or even a tail, offering unique ways"
    "to damage foes and interact with the battlefield."),
    (2, 4, "Path of the Berserker", "You give in to the fury of combat, allowing you to fight with a primal ferocity."
    "While in the grips of your battle rage, you can make extra attacks and ignore effects that would otherwise"
    "cause damage or slow you down."),
    (2, 5, "Path of the Giant", "You draw on the might of legendary giants, gaining their strength and abilities."
    "This path allows you to embody different aspects of giantkind, such as frost or fire, with each option"
    "enhancing your combat abilities in unique ways."),
    (2, 6, "Path of the Storm Herald", "You tap into the power of the storm, generating a magical aura"
    "that affects everything around you. Depending on the environment you choose—tundra, desert, or"
    "sea—your aura can chill, scorch or lash your enemies with storm-like fury."),
    (2, 7, "Path of the Totem Warrior", "You forge a spiritual bond with a totem animal spirit,"
    "emulating the aspects of that being. Each animal spirit—be it bear, eagle, elk, tiger or"
    "wolf—provides unique strengths and supernatural abilities to aid you and your allies."),
    (2, 8, "Path of Wild Magic", "Your rage taps into the chaotic force of wild magic, resulting in"
    "unpredictable arcane side-effects. This path is unique in that that can be both incredibly"
    "powerful but also relies heavily on random dice roles."),
    (2, 9, "Path of the Zealot", "You are driven by a divine fury, bolstered by the power of the gods. This"
    "path not only increases your combat prowess with divine energy but also makes you nearly impossible"
    "to kill while raging."),
    (3, 1, "College of Creation", "You harness the magic of creation, channeling the raw chaos that formed"
    "the universe. This subclass allows you to animate inanimate objects, create performance-enhancing motes"
    "and summon items temporarily into existence."),
    (3, 2, "College of Eloquence", "You are a master the art of persuasion, using your words to charm, inspire"
    "and manipulate others. This subclass grants you abilities that make your speech almost impossible to"
    "resist and reduce the effectiveness of enemies."),
    (3, 3, "College of Glamour", "You weave a magic of enchantment and allure, captivating those around you."
    "This subclass provides you with abilities to charm audiences, command attention and manipulate others’ emotions."),
    (3, 4, "College of Lore", "You collect bits of knowledge from all manner of stories, songs and spells. This"
    "subclass enhances your versatility by granting additional proficiencies, magical secrets from other classes"
    "and the ability to use your knowledge to limit enemy attacks."),
    (3, 5, "College of Spirits", "You channel the tales and powers of the spirits through your performances. This"
    "subclass gives you the ability to summon spirits to convey storied fables, granting you and your"
    "allies a variety of magical effects."),
    (3, 6, "College of Swords", "You blend performance with martial prowess, using your weapon as both an instrument"
    "and a conduit for your bardic spells. This subclass focuses on enhancing your combat abilities, allowing for"
    "flourishes that deal extra damage and bolster your defenses."),
    (3, 7, "College of Valor", "You inspire others in battle through your courage and prowess. This subclass bolsters"
    "your martial capabilities, providing an Extra attack and allowing you protect your allies and"
    "enhance group combat tactics."),
    (3, 8, "College of Whispers", "You traffic in secrets and fear, using your performances to unsettle and manipulate."
    "This subclass grants you the power to psychically harm your foes, steal identities and sow paranoia,"
    "turning your art into a weapon of psychological warfare."),
    (4, 1, "Arcana Domain", "You blend divine and arcane magic, focusing on spells that manipulate"
    "and reveal the mysteries of the universe. This domain grants you powerful magical abilities,"
    "including the use of arcane spells usually reserved for wizards."),
    (4, 2, "Death Domain", "You harness the powers of death and the undead, focusing on spells"
    "that cause decay and manipulate life forces. This domain grants abilities that enhance your"
    "damage against the living and allow you to control the dead."),
    (4, 3, "Forge Domain", "You are a divine artisan, specializing in the creation and"
    "manipulation of metal and fire. This domain bestows abilities that enhance your crafting skills,"
    "protect you with divine armor, and imbuing your weapons with fiery power."),
    (4, 4, "Grave Domain", "You oversee the line between life and death, aiming to ensure balance and"
    "respect for the dead. This domain grants abilities to hinder the undead, protect allies on the brink"
    "of death and maximum the impact of restorative spells."),
    (4, 5, "Knowledge Domain", "You are a seeker of truth, using your divine magic to uncover secrets and"
    "enhance your wisdom. This domain provides powers to read thoughts, learn hidden knowledge and become"
    "proficient in numerous skills and languages."),
    (4, 6, "Life Domain", "You are a conduit of healing and vitality, specializing in spells that restore"
    "and sustain life. This domain increases the effectiveness of your healing spells and grants you"
    "abilities to protect and bolster your allies."),
    (4, 7, "Light Domain", "You channel the power of light and fire, wielding these elements against the darkness."
    "This domain provides powerful options to scorch your enemies, dispel darkness, and protect allies with radiant energy."),
    (4, 8, "Nature Domain", "You are a guardian of the natural world, commanding its elements and creatures."
    "This domain gives you abilities to charm animals and plants, reshape the terrain and summon nature’s"
    "wrath to aid you in battle."),
    (4, 9, "Order Domain", "You impose divine order, using your abilities to control the battlefield"
    "and bolster lawful actions. This domain allows you to enchant allies with bonus attacks and"
    "slow the advance of enemy forces."),
    (4, 10, "Peace Domain", "You promote harmony and tranquility, diffusing conflict and healing"
    "strife. This domain provides abilities that link allies together, allowing shared healing and protection in battle."),
    (4, 11, "Tempest Domain", "You command the elements of storms, wielding thunder, lightning"
    "and wind. This domain grants you control over these elements to shock and push back"
    "enemies while protecting yourself."),
    (4, 12, "Trickery Domain", "You revel in deception and mischief, using your divine gifts"
    "to confuse and mislead. This domain provides stealth and illusion powers, enhancing your"
    "ability to confuse foes and aid allies covertly."),
    (4, 13, "Twilight Domain", "You guard against the fears of the night and guide others"
    "through darkness. This domain bestows powers to comfort allies, manipulate shadows"
    "and see through the deepest gloom."),
    (4, 14, "War Domain", "You are a divine warrior, a crusader in the cause of your deity."
    "This domain blesses you with martial prowess, the ability to make extra attacks and powers"
    "that boost your strength and endurance in battle."),
    (5, 1, "Circle of Dreams", "You are a guardian of the border between the Feywild and the"
    "mortal world, tapping into the magic of nature to heal and aid your allies. This subclass"
    "grants you abilities to cure wounds, provide safe rest and offer protection."),
    (5, 2, "Circle of the Land", "You have a deep connection to a specific natural terrain,"
    "such as forests, mountains or coastlines. This subclass enhances your magical abilities,"
    "allowing you to draw upon the arcane essence of your chosen land for additional spells."),
    (5, 3, "Circle of the Moon", "You specialize in transforming into more powerful animals"
    "and even elemental forms. This subclass focuses on improving your combat effectiveness"
    "in beast form, granting you the ability to become larger, stronger and more formidable creatures."),
    (5, 4, "Circle of the Shepherd", "You are a protector of nature’s creatures, communicating with"
    "and nurturing them. This subclass gives you powers to summon and strengthen spirit totems,"
    "enhancing the abilities of your allies and conjured beasts."),
    (5, 5, "Circle of Spores", "You harness the life and decay aspects of nature, using fungal"
    "spores to fuel your magic. This subclass allows you to animate dead plants and creatures,"
    "deal necrotic damage to enemies and gain temporary health boosts."),
    (5, 6, "Circle of Stars", "You draw on the mystic power of the stars and constellations, using"
    "them to guide and protect. This subclass provides abilities to transform starlight into protective"
    "and restorative magic or harness it for divination and attacks."),
    (5, 6, "Circle of Wildfire", "You believe in renewal through fire, using flames to clear decay"
    "and make way for new life. This subclass lets you summon a wildfire spirit, cast fire-related spells"
    "and heal or bolster your allies with the purifying power of fire."),
    (6, 1, "Arcane Archer", "You infuse your arrows with magical properties, using arcane elvish magic"
    "to create a variety of special effects. This subclass allows you to choose from magical arrow types"
    "that can entangle, banish or even strike hidden targets."),
    (6, 2, "Battle Master", "You are a master of combat techniques and tactics, using maneuvers to"
    "outsmart and defeat your enemies. This subclass grants you abilities to enhance your attacks,"
    "control the battlefield and provide tactical advantages to your allies."),
    (6, 3, "Cavalier", "You excel in mounted combat and are dedicated to protecting others, especially"
    "when riding your steed. This subclass boosts your effectiveness while mounted and on foot, focusing"
    "on defensive tactics and controlling enemies to protect your allies."),
    (6, 4, "Champion", "You focus on refining your martial prowess, becoming a formidable warrior. This"
    "subclass enhances your ability to land critical hits more often and increases your physical capabilities,"
    "making you a relentless fighter."),
    (6, 5, "Echo Knight", "You manipulate time and space to summon an echo of yourself from a parallel"
    "dimension. This subclass allows you to fight from multiple positions, attack from a distance with"
    "your echo, and even swap places with it for strategic maneuvers."),
    (6, 6, "Eldritch Knight", "You blend martial prowess with magical ability, casting spells while"
    "also engaging in hand-to-hand combat. This subclass allows you to summon weapons, cast protective"
    "spells, and use magic to enhance your combat effectiveness."),
    (6, 7, "Rune Knight", "You use mystical runes to enhance your combat skills and manipulate"
    "various magical effects. This subclass allows you to inscribe runes onto your equipment, granting"
    "you and your allies enhanced abilities, protection, or offensive power."),
    (6, 8, "Samurai", "You are a warrior who combines fierce determination with meticulous skill."
    "This subclass provides you with bonuses to accuracy, the ability to withstand damage, and a resolute"
    "will that can keep you fighting even when severely wounded."),
    (7, 1, "Way of the Ascendant Dragon", "You channel the power of dragons, using their mythical"
    "essence to enhance your martial arts prowess. This subclass grants you abilities to breathe"
    "elemental energy, manipulate the battlefield with draconic force and inspire awe or fear like a dragon."),
    (7, 2, "Way of the Astral Self", "You summon an astral projection of yourself, enhancing your combat"
    "capabilities. This subclass allows you to extend your reach, deal extra damage and use your astral form"
    "to shield and strike at your enemies."),
    (7, 3, "Way of the Drunken Master", "You incorporate unpredictable movements into your fighting"
    "style, mimicking a drunkard. This subclass provides you with superior evasion, sudden strikes"
    "and the ability to redirect attacks, making you a slippery target in combat."),
    (7, 4, "Way of the Four Elements", "You harness the power of elemental forces, using them"
    "to cast spells and augment your martial arts. This subclass allows you to manipulate earth,"
    "air, fire and water to attack your foes, defend yourself and control the environment."),
    (7, 5, "Way of the Kensei", "You master the use of weapons as an extension of your body,"
    "integrating them into your martial practice. This subclass enhances your proficiency with"
    "specific weapons, making them more effective and allowing you to use them in conjunction with other monk abilities."),
    (7, 6, "Way of the Long Death", "You are fascinated with the meaning and mechanics of dying, using this"
    "knowledge to your advantage in battle. This subclass grants you the ability to siphon"
    "life force from those you kill to heal yourself and instill fear in your enemies."),
    (7, 7, "Way of Mercy", "You balance between harm and healing, using your knowledge"
    "of anatomy to both cure and cause pain. This subclass provides you with abilities"
    "to heal and harm with your touch, choosing to restore health or drain it as you see fit."),
    (7, 8, "Way of the Open Hand", "You focus on the pure techniques of martial arts, perfecting"
    "strikes that incapacitate your foes. This subclass gives you powerful techniques to"
    "knock enemies prone, push them away or deny them reactions, exemplifying the art of hand-to-hand combat."),
    (7, 9, "Way of the Shadow", "You embrace the stealth and cunning of the shadow, using darkness to"
    "conceal your movements and strike unseen. This subclass allows you to teleport into shadows, become"
    "invisible in dim light and use the dark as a weapon against your enemies."),
    (7, 10, "Way of the Sun Soul", "You channel your inner light into searing bolts of light, similar"
    "to the rays of the sun. This subclass allows you to hurl radiant energy from your hands, use it to"
    "create barriers or radiate light to damage and disrupt your foes."),
    (8, 1, "Oath of Conquest", "Aimed at dominating enemies, this subclass grants spells and"
    "abilities to instill fear and control over the battlefield, allowing you to intimidate and overpower foes."),
    (8, 2, "Oath of Devotion", "Centered on the ideals of honesty and courage, this subclass offers protective"
    "magic, the power to purge evil and the ability to protect and heal allies."),
    (8, 3, "Oath of Glory", "Focused on the pursuit of fame and the embodiment of heroism,"
    "this subclass provides enhancements to physical prowess and leadership, allowing you to excel"
    "in athletic feats and inspire others during battle."),
    (8, 4, "Oath of Redemption", "Focused on nonviolent solutions, you are able to access spells and"
    "abilities to protect yourself and your allies, while also using non-lethal attacks to slow enemies down."),
    (8, 5, "Oath of the Ancients", "Dedicated to preserving the light and life found in nature, you can"
    "access abilities that heal and protect, as well as tapping into offensive spells that harness nature’s wrath."),
    (8, 6, "Oath of the Crown", "Committed to the ideals of civilization and leadership, you are"
    "dedicated to protecting the lawful authority and those who serve it. Your abilities emphasize"
    "defense and control in combat."),
    (8, 7, "Oath of the Watchers", "Designed to guard against the threats of extraplanar entities,"
    "you are able to hinder and combat creatures from other realms, with abilities centered around"
    "detection, containment and banishment."),
    (8, 8, "Oath of Vengeance", "Focused on punishing evildoers, this subclass offers aggressive"
    "tactics and powers that enhance your ability to hunt down and destroy your enemies, emphasizing"
    "relentless offensive attacks."),
    (8, 9, "Oathbreaker", "Tailored for paladins who have forsaken their oaths, this evil subclass"
    "provides powers to control and manipulate the undead, wield dread magics and command the shadows."),
    (9, 1, "Beast Master", "You bond with a loyal beast companion, commanding it in battle to fight by"
    "your side. Your connection allows you to work seamlessly as a team, enhancing your combat abilities and coordination."),
    (9, 2, "Drakewarden", "You form a mystical bond with a drake, a dragon-like creature that assists you in battle."
    "As you grow in power, your drake evolves, gaining new abilities that complement your own."),
    (9, 3, "Fey Wanderer", "You draw on the mysterious magic of the Feywild, using enchantments and tricks to bewilder your"
    "foes and charm others. Your abilities also strengthen your mind, providing resilience against mental assaults."),
    (9, 4, "Gloom Stalker", "You excel in darkness and ambush, using your skills to become nearly invisible in the shadows."
    "Your attacks are swift and deadly, particularly at the onset of battle, giving you a critical advantage in the first"
    "moments of combat."),
    (9, 5, "Horizon Walker", "You protect the world from extraplanar threats, gaining abilities that allow you to manipulate"
    "space and even teleport. Your attacks can bypass defenses as you harness the energies of the multiverse."),
    (9, 6, "Hunter", "You specialize in tracking and defeating a variety of creatures, adapting your tactics based on the"
    "nature of your prey. In addition, you gain specific abilities that enhance your effectiveness against certain types"
    "of enemies."),
    (9, 7, "Monster Slayer", "You focus on hunting down the most dangerous creatures, gaining supernatural abilities that"
    "help you track, confront and destroy these threats. Your skills make you particularly adept at disrupting your"
    "enemies’ abilities and resisting their magic."),
    (9, 8, "Swarmkeeper", "You are surrounded by a swarm of tiny creatures or spirits that assist you in battle."
    "This mystical connection to these creatures grants you a range of combat tactics, with both offensive and"
    "defensive capabilities."),
    (10, 1, "Arcane Trickster", "You enhance your skills as a rogue with the subtle magic of illusion and"
    "enchantment. This subclass grants you the ability to cast spells that can manipulate others, hide your"
    "movements or confuse your foes."),
    (10, 2, "Assassin", "You specialize in infiltration and the art of the kill, becoming a master"
    "of disguise and deadly strikes. This subclass provides you with bonuses for attacking unaware"
    "opponents, allowing you to deal significant damage in the first moments of combat."),
    (10, 3, "Inquisitive", "You have a sharp eye for detail and excel at deducing clues"
    "and lies. This subclass allows you to use your keen observation to uncover hidden truths, spot"
    "weaknesses in your opponents and gain an advantage in social and combat encounters."),
    (10, 4, "Mastermind", "You are a strategist and manipulator, skilled at pulling the strings from"
    "the shadows. This subclass grants you the ability to mimic speech, forge documents and direct allies in combat."),
    (10, 5, "Phantom", "You channel the powers of the dead, gaining abilities linked to shadows and spirits. This"
    "subclass allows you to steal aspects of the deceased to gain temporary benefits and leave behind spectral"
    "tokens to spy or communicate."),
    (10, 6, "Scout", "You are adept at wilderness survival and reconnaissance, using your skills to navigate"
    "and track. This subclass enhances your mobility and ability to avoid danger, making you formidable"
    "in stealth and surprise."),
    (10, 7, "Soulknife", "You manifest psychic blades from your mind, using them as weapons. This subclass"
    "grants you the ability to create and wield these ethereal blades, attack from a distance and use"
    "your psychic power to deliver devestating mental assaults."),
    (10, 8, "Swashbuckler", "You thrive in fast-paced duels and charismatic interactions, embodying"
    "the daring rogue with a flair for dramatic combat. This subclass enhances your ability"
    "to engage foes one-on-one, dodge attacks and charm individuals in social situations."),
    (10, 9, "Thief", "You excel at climbing, sneaking and stealing, using your agility"
    "and cunning to gain access to places others can’t go. This subclass provides you"
    "with enhanced abilities to perform sleight of hand, disarm traps and make the most of your"
    "ill-gotten goods."),
    (11, 1, "Aberrant mind", "You are imbued with psychic powers derived from an alien"
    "influence. This subclass grants you the ability to telepathically communicate, manipulate"
    "thoughts and cast spells without verbal or somatic components."),
    (11, 2, "Clockwork Soul", "Influenced by the orderly mechanisms of Mechanus, you"
    "can manipulate probabilities and ensure that events unfold according to plan. This subclass"
    "allows you to impose order on chaotic situations, prevent alterations to conditions and"
    "repair both magical and mundane items."),
    (11, 3, "Divine Soul", "With a touch of the divine in your bloodline, you blend sorcerous"
    "magic with divine power. This subclass provides you access to both sorcerer and cleric"
    "spell lists, enhancing your healing and protective capabilities alongside your natural sorcery."),
    (11, 4, "Draconic Bloodline", "Your magical powers derive from a dragon ancestor, granting you"
    "scales, fearsome presence and elemental affinities related to your dragon’s nature. This"
    "subclass enhances your durability, charisma, and grants abilities based on the type of dragon from which you descend."),
    (11, 5, "Shadow Magic", "Born from the Plane of Shadow, you harness dark energies to create illusions,"
    "summon shadow, and occasionally slip through the veil between life and death. This subclass"
    "provides you with resilience against death and the ability to summon a shadowy hound to harry your foes."),
    (11, 6, "Storm Sorcery", "Your magic crackles with the raw energy of tempests, giving you"
    "control over wind, lightning and thunder. This subclass enhances your mobility, allowing you"
    "to ride gusts of wind and channel your spells with the power of a storm."),
    (11, 7, "Wild Magic", "Your magic is unpredictable and explosive, resulting from a chaotic"
    "surge of magical energy. This subclass leads to random magical effects that can either"
    "dramatically benefit or hamper you and your allies, adding an element of chance to every spell you cast."),
    (12, 1, "Archfey", "You have made a pact with a powerful being of the Feywild, gaining powers that enchant"
    "and bewilder. This subclass provides you with abilities to charm and frighten others, teleport short "
    "distances and manipulate the minds and emotions of those around you."),
    (12, 2, "Celestial", "Your patron is a creature of good, imbuing you with powers of healing and radiance."
    "This subclass allows you to cure wounds, channel celestial energy into destructive power and provide"
    "resilience against death for you and your allies."),
    (12, 3, "Fathomless", "Bound to a mysterious entity from the watery depths, you command"
    "the crushing pressure and cold darkness of the sea. This subclass grants you tentacle"
    "attacks, watery teleportation and the ability to breathe underwater as well as resist cold."),
    (12, 4, "Fiend", "Your patron is a creature of the lower planes, bestowing upon you the"
    "ability to channel fiery wrath and curses upon your foes. This subclass enhances your resilience,"
    "provides bonuses to certain types of spells and allows you to temporarily gain hit points"
    "when you reduce a foe to 0 hit points."),
    (12, 5, "Genie", "You serve a powerful genie, gaining magic that reflects"
    "the genie’s elemental nature—be it air, fire, earth or water. This subclass"
    "allows you to craft a magical vessel linked to your genie, gain resistance related to"
    "your genie’s type and manipulate the battlefield with elemental power."),
    (12, 6, "Great Old One", "Linked to a mysterious, otherworldly entity, your"
    "powers include telepathy and mental manipulation. This subclass provides you with"
    "the ability to communicate thoughts, sow madness among your enemies and protect your"
    "mind against intrusions."),
    (12, 7, "Hexblade", "You are connected to a magical weapon borne from the Shadowfell,"
    "which grants you combat prowess and the ability to curse your foes. This subclass"
    "enhances your melee capabilities, allows you to use charisma for weapon attacks and"
    "provides spells related to combat and protection."),
    (12, 8, "Undead", "You derive your power from a bond with the undead, embracing necrotic"
    "energies and manipulating the forces of death. This subclass allows you to adopt"
    "ghostly traits, terrify your enemies and eventually even defy death itself."),
    (12, 9, "Undying", "Your patron is an immortal being who has mastered the secrets"
    "of longevity, sharing with you the magic of endurance and preservation. This subclass"
    "gives you abilities to avoid death, resist disease and restore health."),
    (13, 1, "Bladesinger", "Almost entirely exclusive to elves and half-elves,"
    "you blend expert swordplay with arcane magic, enhancing your agility, concentration"
    "and combat spells through a mystical battle ritual known as the Bladesong."),
    (13, 2, "Chronurgy", "You manipulate the flow of time through your magic, gaining"
    "abilities that allow you to adjust initiative, hasten or slow spells and creatures, and even"
    "alter the course of events as they occur."),
    (13, 3, "Graviturgy", "Specializing in the manipulation of gravity, you can make"
    "objects heavier or lighter, pin foes to the spot or use gravitational force to"
    "enhance your own mobility and offensive capabilities."),
    (13, 4, "Order of Scribes", "You magically awaken your spellbook, turning"
    "it into a valuable assistant. This subclass provides unique ways to cast and"
    "store spells, swap spell properties and even resurrect your spellbook if it’s destroyed."),
    (13, 5, "School of Abjuration", "You specialize in protective magic, strengthening"
    "your defenses and banishing enemies. This school enhances your ability to cast wards,"
    "counterspells and protective enchantments, making you and your allies more resilient against attacks."),
    (13, 6, "School of Conjuration", "You specialize in summoning creatures, objects and phenomena from"
    "other places, mastering the art of teleportation and conjuration. This subclass grants"
    "you the ability to instantly transport and create items and allies to aid in various situations."),
    (13, 7, "School of Divination", "You focus on foresight and information, using your spells to"
    "reveal secrets, predict events and gain insights that others cannot perceive. This school"
    "provides abilities that manipulate dice rolls and provide additional information."),
    (13, 8, "School of Enchantment", "You wield magic that charms and beguiles, influencing"
    "and controlling the behavior of others. This school grants powers to charm individuals, erase"
    "memories and dominate minds."),
    (13, 9, "School of Evocation", "You channel raw elemental power into destructive spells"
    "to control and maximize damage. This school allows you to shape spells to protect allies,"
    "augment attacks and target enemies from afar."),
    (13, 10, "School of Illusion", "You create convincing illusions and deceptive images that"
    "can trick the senses. This school develops your skills to manipulate illusions, making"
    "them interact with the environment and even become real for a short time."),
    (13, 11, "School of Necromancy", "You tap into the energies of life and death,"
    "using your spells to drain energy, control undead and manipulate existence. This"
    "school enhances your abilities related to the undead and grants you necrotic"
    "powers that sap strength from your enemies."),
    (13, 12, "School of Transmutation", "You master the art of changing energy and matter,"
    "transforming the physical properties of creatures, objects and yourself. This"
    "school allows you to alter your physical form, enhance combat abilities and"
    "manipulate the natural world."),
    (13, 13, "War Magic", "A blend of defensive and offensive magic, you focus on"
    "quick thinking and rapid responses to maintain superior control in battle. This"
    "school enhances your ability to maintain concentration, boost defenses and deliver powerful counterattacks.")
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
    "if that attack hits, the target takes an extra 1d6 lightning damage.")
        
    ]
#c.executemany('INSERT INTO subclass_features (class_id, subclass_features, feature_name, level, description) VALUES (?, ?, ?, ?, ?)', subclass_features)




# Commit changes and close the connection
conn.commit()
conn.close()




# Example: Fetch and display features for Fighter (class_id 6)
main()
