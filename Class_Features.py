import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('dnd_character_info.db')
c = conn.cursor()

# Create table for DnD classes
# c.execute('''
#     CREATE TABLE IF NOT EXISTS classes (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         hit_die TEXT NOT NULL,
#         description TEXT NOT NULL
#     )
# ''')

# Insert all 13 DnD classes into the table in alphabetical order
# dnd_classes = [
#     (1, "Artificer", "1d8", "A master of invention, Artificers use ingenuity and magic to unlock extraordinary capabilities in objects."),
#     (2, "Barbarian", "1d12", "A fierce warrior of primitive background who can enter a battle rage."),
#     (3, "Bard", "1d8", "An inspiring magician whose power echoes the music of creation."),
#     (4, "Cleric", "1d8", "A priestly champion who wields divine magic in service of a higher power."),
#     (5, "Druid", "1d8", "A priest of the Old Faith, wielding the powers of nature and adopting animal forms."),
#     (6, "Fighter", "1d10", "A master of martial combat, skilled with a variety of weapons and armor."),
#     (7, "Monk", "1d8", "A master of martial arts, harnessing the power of the body in pursuit of physical and spiritual perfection."),
#     (8, "Paladin", "1d10", "A holy warrior bound to a sacred oath."),
#     (9, "Ranger", "1d10", "A warrior who uses martial prowess and nature magic to combat threats on the edges of civilization."),
#     (10, "Rogue", "1d8", "A scoundrel who uses stealth and trickery to overcome obstacles and enemies."),
#     (11, "Sorcerer", "1d6", "A spellcaster who draws on inherent magic from a gift or bloodline."),
#     (12, "Warlock", "1d8", "A wielder of magic that is derived from a bargain with an extraplanar entity."),
#     (13, "Wizard", "1d6", "A scholarly magic-user capable of manipulating the structures of reality."),
# ]

# # Insert classes into the database
# c.executemany('INSERT OR IGNORE INTO classes VALUES (?, ?, ?, ?)', dnd_classes)

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


# # Create table for class features
# c.execute('''
#     CREATE TABLE IF NOT EXISTS features (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         class_id INTEGER NOT NULL,
#         feature_name TEXT NOT NULL,
#         level INTEGER NOT NULL,
#         description TEXT NOT NULL,
#         FOREIGN KEY (class_id) REFERENCES classes(id)
#     )
# ''')


# # Artificer features from level 1 to 20
# artificer_features = [
#     (1, "Magical Tinkering", 1, "You learn to invest a spark of magic in mundane objects, giving them various effects."),
#     (1, "Spellcasting", 1, "You gain the ability to cast spells through your innate understanding of magic and invention."),
#     (1, "Infuse Item", 2, "You gain the ability to infuse mundane items with magic, giving them special properties."),
#     (1, "Artificer Specialist", 3, "Choose a specialty in a specific area of invention, such as Alchemist, Armorer, Artillerist, or Battle Smith."),
#     (1, "The Right Tool for the Job", 3, "You can create one set of artisan's tools in an unoccupied space."),
#     (1, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (1, "Tool Expertise", 6, "Your proficiency bonus is doubled for any ability check you make that uses your proficiency with a tool."),
#     (1, "Flash of Genius", 7, "When you or another creature you can see within 30 feet makes an ability check or a saving throw, you can use your reaction to add your Intelligence modifier to the roll."),
#     (1, "Magic Item Adept", 10, "You can attune to up to four magic items at once, and you can craft magic items more easily."),
#     (1, "Spell-Storing Item", 11, "You can store a spell in a chosen object, which can be cast by a creature holding the object."),
#     (1, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (1, "Magic Item Savant", 14, "You can attune to up to five magic items at once, and you can ignore all class, race, spell, and level requirements on attuning to or using a magic item."),
#     (1, "Magic Item Master", 18, "You can attune to up to six magic items at once."),
#     (1, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
#     (1, "Soul of Artifice", 20, "You gain a +1 bonus to all saving throws per magic item you are currently attuned to, and if you are reduced to 0 hit points but not killed outright, you can end one of your artificer infusions to drop to 1 hit point instead."),
# ]

# # Insert Artificer features into the database
# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', artificer_features)


# barbarian_features = [
#     (2, "Rage", 1, "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action."
#     "While raging, you gain the following benefits if you aren’t wearing heavy armor: \n\t*You have advantage on"
#     "Strength checks and Strength saving throws. \n\t*When you make a melee weapon attack using Strength, you"
#     "gain a bonus to the damage roll that increases as you gain levels as a \tbarbarian, as shown in the Rage"
#     "Damage column of the Barbarian table. \n\t*You have resistance to bludgeoning, piercing, and slashing damage."
#     "\n\nIf you are able to cast spells, you can’t cast them or concentrate on them while raging.\n\nYour rage"
#     "lasts for 1 minute. It ends early if you are knocked unconscious or if your turn ends and you haven’t"
#     "attacked a hostile creature since your last turn or taken damage since then. You can also end your rage"
#     "on your turn as a bonus action. \n\nOnce you have raged the number of times shown for your barbarian level"
#     "in the Rages column of the Barbarian table, you must finish a long rest before you can rage again."),
#     (2, "Unarmored Defense", 1, "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity"
#     "modifier + your Constitution modifier. You can use a shield and still gain this benefit."),
#     (2, "Reckless Attack", 2, "Starting at 2nd level, you can throw aside all concern for defense to attack"
#     "with fierce desperation. When you make your first attack on your turn, you can decide to attack"
#     "recklessly, giving you advantage on melee weapon attacks using Strength."),
#     (2, "Danger Sense", 2, "You gain an uncanny sense of when things nearby aren't as they should be, giving"
#     "you advantage on Dexterity saving throws against effects you can see."),
#     (2, "Primal Path", 3, "Choose a primal path that shapes the nature of your rage. Your choice grants"
#     "you features at 3rd level, 6th level, 10th level, and 14th level."),
#     (2, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (2, "Extra Attack", 5, "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
#     (2, "Fast Movement", 5, "Your speed increases by 10 feet while you aren’t wearing heavy armor."),
#     (2, "Feral Instinct", 7, "Your instincts are so honed that you have advantage on initiative rolls."
#     "Additionally, if you are surprised at the beginning of combat and aren't incapacitated, you can act"
#     "normally on your first turn, but only if you enter your rage before doing anything else."),
#     (2, "Brutal Critical (1 die)", 9, "You can roll one additional weapon damage die when determining"
#     "the extra damage for a critical hit with a melee attack."),
#     (2, "Relentless Rage", 11, "If you drop to 0 hit points while you’re raging and don’t die outright,"
#     "you can make a DC 10 Constitution saving throw. If you succeed, you drop to 1 hit point instead."),
#     (2, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (2, "Brutal Critical (2 dice)", 13, "You can roll two additional weapon damage dice when determining"
#     "the extra damage for a critical hit with a melee attack."),
#     (2, "Persistent Rage", 15, "Your rage is so fierce that it ends early only if you fall unconscious or"
#     "choose to end it."),
#     (2, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (2, "Brutal Critical (3 dice)", 17, "You can roll three additional weapon damage dice when determining"
#     "the extra damage for a critical hit with a melee attack."),
#     (2, "Indomitable Might", 18, "If your total for a Strength check is less than your Strength score, you"
#     "can use that score in place of the total."),
#     (2, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
#     (2, "Primal Champion", 20, "Your Strength and Constitution scores increase by 4. Your maximum for those"
#     "scores is now 24."),
# ]


# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', barbarian_features)

# bard_features = [
#     (3, "Spellcasting", 1, "You have learned to untangle and reshape the fabric of reality in harmony with your wishes and music."),
#     (3, "Bardic Inspiration (d6)", 1, "You can inspire others through stirring words or music. As a bonus action, a creature within 60 feet that can hear you gains an inspiration die (a d6)."),
#     (3, "Jack of All Trades", 2, "You can add half your proficiency bonus, rounded down, to any ability check you make that doesn’t already include your proficiency bonus."),
#     (3, "Song of Rest (d6)", 2, "You can use soothing music or oration to help revitalize your wounded allies during a short rest, allowing them to regain an extra 1d6 hit points."),
#     (3, "Bard College", 3, "You choose a bardic college that shapes your approach to magic and performance. Your choice grants you features at 3rd level and again at 6th and 14th level."),
#     (3, "Expertise", 3, "Choose two of your skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."),
#     (3, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (3, "Bardic Inspiration (d8)", 5, "Your Bardic Inspiration die becomes a d8."),
#     (3, "Font of Inspiration", 6, "You regain all of your expended uses of Bardic Inspiration when you finish a short or long rest."),
#     (3, "Countercharm", 6, "You gain the ability to use musical notes or words of power to disrupt mind-influencing effects. As an action, you can start a performance that lasts until the end of your next turn."),
#     (3, "Magical Secrets", 10, "You have plundered magical knowledge from a wide spectrum of disciplines. Choose two spells from any class, including this one."),
#     (3, "Bardic Inspiration (d10)", 10, "Your Bardic Inspiration die becomes a d10."),
#     (3, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (3, "Magical Secrets", 14, "Choose two additional spells from any class."),
#     (3, "Bardic Inspiration (d12)", 15, "Your Bardic Inspiration die becomes a d12."),
#     (3, "Superior Inspiration", 20, "When you roll initiative and have no uses of Bardic Inspiration left, you regain one use."),
# ]

# # Insert Artificer features into the database
# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', bard_features)

# cleric_features = [
#     (4, "Spellcasting", 1, "As a conduit for divine power, you can cast cleric spells that you have prepared."),
#     (4, "Divine Domain", 1, "Choose a domain related to your deity, which grants you special features at levels 1, 2, 6, 8, and 17."),
#     (4, "Channel Divinity (1/rest)", 2, "You can channel divine energy to fuel magical effects. You start with two such effects: Turn Undead and an effect determined by your domain."),
#     (4, "Channel Divinity: Turn Undead", 2, "As an action, you present your holy symbol and speak a prayer censuring the undead, forcing them to flee."),
#     (4, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (4, "Destroy Undead (CR 1/2)", 5, "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below 1/2."),
#     (4, "Divine Intervention", 10, "You can call on your deity to intervene on your behalf when your need is great. Your chance of success is equal to your cleric level."),
#     (4, "Destroy Undead (CR 1)", 8, "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below 1."),
#     (4, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (4, "Destroy Undead (CR 2)", 11, "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below 2."),
#     (4, "Divine Intervention Improvement", 18, "When you use your Divine Intervention feature, it automatically succeeds without needing to roll."),
#     (4, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (4, "Destroy Undead (CR 3)", 14, "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below 3."),
#     (4, "Destroy Undead (CR 4)", 17, "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below 4."),
#     (4, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (4, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
#     (4, "Divine Intervention: Automatic Success", 20, "When you use your Divine Intervention feature, it automatically succeeds, no roll required."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', cleric_features)


# druid_features = [
#     (5, "Druidic", 1, "You know Druidic, the secret language of druids. You can speak the language and use it to leave hidden messages."),
#     (5, "Spellcasting", 1, "You can cast druid spells, using Wisdom as your spellcasting ability."),
#     (5, "Wild Shape", 2, "You can use your action to magically assume the shape of a beast that you have seen before. You can use this feature twice, regaining expended uses after a short or long rest."),
#     (5, "Druid Circle", 2, "Choose a druid circle that grants you features at levels 2, 6, 10, and 14."),
#     (5, "Wild Shape Improvement", 4, "You can transform into a beast with a challenge rating as high as 1/2 (no flying speed)."),
#     (5, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (5, "Wild Shape Improvement", 8, "You can transform into a beast with a challenge rating as high as 1 (no flying speed)."),
#     (5, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (5, "Timeless Body", 18, "You no longer suffer the effects of aging, and you can't be aged magically."),
#     (5, "Beast Spells", 18, "You can cast many of your druid spells in any shape you assume using Wild Shape."),
#     (5, "Archdruid", 20, "You can use Wild Shape an unlimited number of times, and you ignore the verbal and somatic components of your druid spells."),
#     (5, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (5, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (5, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', druid_features)

# fighter_features = [
#     (6, 'Second Wind', 1, 'You have a limited well of stamina that you can draw on'
#     'to protect yourself from harm. On your turn, you can use a bonus action to'
#     'regain hit points equal to 1d10 + your fighter level. \nOnce you use this'
#     'feature, you must finish a short or long rest before you can use it again.'),
#     (6, 'Action Surge (1 use)', 2, 'Starting at 2nd level, you can push yourself'
#     'beyond your normal limits for a moment. On your turn, you can take one'
#     'additional action. \nOnce you use this feature, you must finish a short'
#     'or long rest before you can use it again. Starting at 17th level, you'
#     'can use it twice before a rest, but only once on the same turn.'),
#     (6, 'Martial Archetype', 3, 'You choose an archetype that you strive to'
#     'emulate in your combat styles and techniques.'),
#     (6, 'Ability Score Improvement', 4, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Extra Attack (1)', 5, 'Beginning at 5th level, you can attack twice,'
#     'instead of once, whenever you take the Attack action on your turn. \nThe'
#     'number of attacks increases to three when you reach 11th level in this'
#     'class and to four when you reach 20th level in this class.'),
#     (6, 'Ability Score Improvement', 6, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Martial Archetype Feature', 7, 'You gain a feature from your chosen'
#     'Martial Archetype.'),
#     (6, 'Ability Score Improvement', 8, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Indomitable (1 use)', 9, "Beginning at 9th level, you can reroll a"
#     "saving throw that you fail. If you do so, you must use the new roll,"
#     "and you can't use this feature again until you finish a long rest. \nYou"
#     "can use this feature twice between long rests starting at 13th level"
#     "and three times between long rests starting at 17th level."),
#     (6, 'Martial Archetype Feature', 10, 'You gain a feature from your chosen'
#     'Martial Archetype.'),
#     (6, 'Extra Attack (2)', 11, 'You can attack three times whenever you take'
#     'the Attack action on your turn.'),
#     (6, 'Ability Score Improvement', 12, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Indomitable (2 uses)', 13, 'You can reroll a saving throw that you'
#     'fail twice per long rest.'),
#     (6, 'Ability Score Improvement', 14, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Martial Archetype Feature', 15, 'You gain a feature from your chosen'
#     'Martial Archetype.'),
#     (6, 'Ability Score Improvement', 16, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Action Surge (2 uses)', 17, 'You can use Action Surge twice per short'
#     'or long rest.'),
#     (6, 'Indomitable (3 uses)', 17, 'You can reroll a saving throw that you'
#     'fail three times per long rest.'),
#     (6, 'Martial Archetype Feature', 18, 'You gain a feature from your chosen'
#     'Martial Archetype.'),
#     (6, 'Ability Score Improvement', 19, 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.'),
#     (6, 'Extra Attack (3)', 20, 'You can attack four times whenever you take'
#     'the Attack action on your turn.')
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', fighter_features)



# monk_features = [
#     (7, "Unarmored Defense", 1, "Your AC equals 10 + your Dexterity modifier + your Wisdom modifier when you aren’t wearing armor."),
#     (7, "Martial Arts", 1, "You can use Dexterity instead of Strength for attack and damage rolls of your unarmed strikes and monk weapons."),
#     (7, "Ki", 2, "You can channel inner energy to fuel special techniques. You have a number of ki points equal to your monk level."),
#     (7, "Unarmored Movement", 2, "Your speed increases by 10 feet while you aren’t wearing armor or wielding a shield."),
#     (7, "Monastic Tradition", 3, "Choose a monastic tradition that grants you features at levels 3, 6, 11, and 17."),
#     (7, "Deflect Missiles", 3, "You can use your reaction to deflect or catch a missile when you are hit by a ranged weapon attack."),
#     (7, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (7, "Slow Fall", 4, "You can use your reaction when you fall to reduce any falling damage you take by an amount equal to five times your monk level."),
#     (7, "Extra Attack", 5, "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
#     (7, "Stunning Strike", 5, "You can interfere with the flow of ki in an opponent's body. When you hit another creature with a melee weapon attack, you can spend 1 ki point to attempt a stunning strike."),
#     (7, "Ki-Empowered Strikes", 6, "Your unarmed strikes count as magical for the purpose of overcoming resistance and immunity to nonmagical attacks and damage."),
#     (7, "Evasion", 7, "When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed, and only half if you fail."),
#     (7, "Stillness of Mind", 7, "You can use your action to end one effect on yourself that is causing you to be charmed or frightened."),
#     (7, "Purity of Body", 10, "Your mastery of the ki flowing through you makes you immune to disease and poison."),
#     (7, "Tongue of the Sun and Moon", 13, "You can understand all spoken languages and any creature that can understand a language can understand you."),
#     (7, "Diamond Soul", 14, "You gain proficiency in all saving throws."),
#     (7, "Timeless Body", 15, "Your ki sustains you so that you suffer none of the frailty of old age, and you can't be aged magically."),
#     (7, "Empty Body", 18, "You can use your action to spend 4 ki points to become invisible for 1 minute. You also gain resistance to all damage except force damage."),
#     (7, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (7, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (7, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (7, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
#     (7, "Perfect Self", 20, "When you roll for initiative and have no ki points remaining, you regain 4 ki points."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', monk_features)

# paladin_features = [
#     (8, "Divine Sense", 1, "The presence of strong evil registers on your senses like a noxious odor, and powerful good rings like heavenly music in your ears."),
#     (8, "Lay on Hands", 1, "You have a pool of healing power that replenishes when you take a long rest. With that pool, you can restore a total number of hit points equal to your paladin level x 5."),
#     (8, "Fighting Style", 2, "You adopt a particular style of fighting as your specialty. Choose a fighting style such as Defense, Dueling, Great Weapon Fighting, or Protection."),
#     (8, "Spellcasting", 2, "You can cast Paladin spells. Charisma is your spellcasting ability for these spells."),
#     (8, "Divine Smite", 2, "When you hit a creature with a melee weapon attack, you can expend one spell slot to deal radiant damage to the target, in addition to the weapon's damage."),
#     (8, "Divine Health", 3, "The divine magic flowing through you makes you immune to disease."),
#     (8, "Sacred Oath", 3, "Choose a Sacred Oath that binds you as a paladin forever. The Oath grants you special abilities at 3rd, 7th, 15th, and 20th levels."),
#     (8, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (8, "Extra Attack", 5, "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
#     (8, "Aura of Protection", 6, "Whenever you or a friendly creature within 10 feet of you must make a saving throw, the creature gains a bonus to the saving throw equal to your Charisma modifier (with a minimum bonus of +1)."),
#     (8, "Aura of Courage", 10, "You and friendly creatures within 10 feet of you can’t be frightened while you are conscious."),
#     (8, "Improved Divine Smite", 11, "Your melee weapon attacks deal an extra 1d8 radiant damage whenever you hit."),
#     (8, "Cleansing Touch", 14, "You can use your action to end one spell on yourself or on one willing creature that you touch."),
#     (8, "Aura Improvements", 18, "Your auras now affect friendly creatures within 30 feet of you, rather than 10 feet."),
#     (8, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (8, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (8, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (8, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
#     (8, "Sacred Oath Feature", 20, "You gain a feature determined by your Sacred Oath."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', paladin_features)


# ranger_features = [
#     (9, "Favored Enemy", 1, "Choose a type of favored enemy: aberrations, beasts, celestials, constructs, dragons, elementals, fey, fiends, giants, monstrosities, oozes, plants, or undead. You gain advantages in tracking and knowing about them."),
#     (9, "Natural Explorer", 1, "You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions."),
#     (9, "Fighting Style", 2, "You adopt a particular style of fighting as your specialty. Choose from Archery, Defense, Dueling, or Two-Weapon Fighting."),
#     (9, "Spellcasting", 2, "You can cast Ranger spells, using Wisdom as your spellcasting ability."),
#     (9, "Primeval Awareness", 3, "You can use your action and expend one Ranger spell slot to focus your awareness on the region around you."),
#     (9, "Ranger Archetype", 3, "Choose an archetype that grants you features at 3rd, 7th, 11th, and 15th levels."),
#     (9, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (9, "Extra Attack", 5, "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
#     (9, "Land's Stride", 8, "Moving through nonmagical difficult terrain costs you no extra movement."),
#     (9, "Hide in Plain Sight", 10, "You can spend 1 minute creating camouflage for yourself."),
#     (9, "Vanish", 14, "You can use the Hide action as a bonus action."),
#     (9, "Feral Senses", 18, "You gain preternatural senses that help you fight creatures you can't see."),
#     (9, "Foe Slayer", 20, "You become an unparalleled hunter of your enemies."),
#     (9, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (9, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (9, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (9, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', ranger_features)

# rogue_features = [
#     (10, "Sneak Attack", 1, "You know how to strike subtly and exploit a foe's"
#     "distraction. Your attacks deal extra damage when you have advantage on the"
#     "attack roll."),
#     (10, "Thieves' Cant", 1, "During your rogue training you learned thieves' cant"
#     ", a secret mix of dialect, jargon, and code that allows you to hide messages"
#     "in seemingly normal conversation."),
#     (10, "Cunning Action", 2, "Your quick thinking and agility allow you to move"
#     "and act quickly. You can take a bonus action to Dash, Disengage, or Hide."),
#     (10, "Roguish Archetype", 3, "At 3rd level, you choose an archetype that you"
#     "emulate in the exercise of your rogue abilities: Thief, Assassin, or Arcane Trickster."),
#     (10, "Ability Score Improvement", 4, "When you reach 4th level, you can"
#     "increase one ability score of your choice by 2, or you can increase two ability"
#     "scores of your choice by 1."),
#     (10, "Uncanny Dodge", 5, "Starting at 5th level, when an attacker that you can"
#     "see hits you with an attack, you can use your reaction to halve the attack's damage."),
#     (10, "Expertise", 6, "At 6th level, choose two more of your proficiencies in skills"
#     "or your proficiency with thieves' tools. Your proficiency bonus is doubled for any"
#     "ability check you make that uses either of the chosen proficiencies."),
#     (10, "Evasion", 7, "Beginning at 7th level, you can nimbly dodge out of the way"
#     "of certain area effects, such as a red dragon's fiery breath or an ice storm spell."),
#     (10, "Ability Score Improvement", 8, "When you reach 8th level, you can increase"
#     "one ability score of your choice by 2, or you can increase two ability scores"
#     "of your choice by 1."),
#     (10, "Roguish Archetype Feature", 9, "At 9th level, you gain a feature granted by"
#     "your Roguish Archetype."),
#     (10, "Ability Score Improvement", 10, "When you reach 10th level, you can increase"
#     "one ability score of your choice by 2, or you can increase two ability scores"
#     "of your choice by 1."),
#     (10, "Reliable Talent", 11, "By 11th level, you have refined your chosen skills"
#     "until they approach perfection. Whenever you make an ability check that lets you"
#     "add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10."),
#     (10, "Ability Score Improvement", 12, "When you reach 12th level, you can increase"
#     "one ability score of your choice by 2, or you can increase two ability scores' of your choice by 1."),
#     (10, "Roguish Archetype Feature", 13, "At 13th level, you gain a feature granted"
#     "by your Roguish Archetype."),
#     (10, "Blindsense", 14, "If you are able to hear, you are aware of the location"
#     "of any hidden or invisible creature within 10 feet of you."),
#     (10, "Slippery Mind", 15, "By 15th level, you have acquired greater mental strength."
#     "You gain proficiency in Wisdom saving throws."),
#     (10, "Ability Score Improvement", 16, "When you reach 16th level, you can increase"
#     "one ability score of your choice by 2, or you can increase two ability scores"
#     "of your choice by 1."),
#     (10, "Roguish Archetype Feature", 17, "At 17th level, you gain a feature granted"
#     "by your Roguish Archetype."),
#     (10, "Elusive", 18, "Beginning at 18th level, you are so evasive that attackers"
#     "rarely gain the upper hand against you. No attack roll has advantage against"
#     "you while you aren’t incapacitated."),
#     (10, "Ability Score Improvement", 19, "When you reach 19th level, you can"
#     "increase one ability score of your choice by 2, or you can increase two"
#     "ability scores of your choice by 1."),
#     (10, "Stroke of Luck", 20, "At 20th level, you have an uncanny knack for"
#     "succeeding when you need to. If your attack misses a target within range,"
#     "you can turn the miss into a hit.")
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', rogue_features)



# sorcerer_features = [
#     (11, "Spellcasting", 1, "You can cast Sorcerer spells, using Charisma as your spellcasting ability."),
#     (11, "Sorcerous Origin", 1, "Choose a sorcerous origin, which grants you features at 1st, 6th, 14th, and 18th levels."),
#     (11, "Font of Magic", 2, "You can use sorcery points to create spell slots or fuel special abilities."),
#     (11, "Metamagic", 3, "You can twist your spells to suit your needs. Choose two Metamagic options."),
#     (11, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (11, "Sorcerous Origin Feature", 6, "You gain a feature from your chosen sorcerous origin."),
#     (11, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (11, "Sorcerous Origin Feature", 14, "You gain a feature from your chosen sorcerous origin."),
#     (11, "Sorcerous Origin Feature", 18, "You gain a feature from your chosen sorcerous origin."),
#     (11, "Sorcerous Restoration", 20, "You regain 4 expended sorcery points whenever you finish a short rest."),
#     (11, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (11, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (11, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', sorcerer_features)



# warlock_features = [
#     (12, "Otherworldly Patron", 1, "You have made a pact with an otherworldly being that grants you magical powers. Your choice grants you features at 1st, 6th, 10th, and 14th levels."),
#     (12, "Pact Magic", 1, "You can cast Warlock spells, using Charisma as your spellcasting ability. You regain expended spell slots after a short or long rest."),
#     (12, "Eldritch Invocations", 2, "You gain two eldritch invocations of your choice, which enhance your abilities or give you new powers."),
#     (12, "Pact Boon", 3, "Choose a boon from your patron that grants you features at 3rd level."),
#     (12, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (12, "Mystic Arcanum (6th level)", 11, "You can cast one 6th-level spell once without expending a spell slot."),
#     (12, "Mystic Arcanum (7th level)", 13, "You can cast one 7th-level spell once without expending a spell slot."),
#     (12, "Mystic Arcanum (8th level)", 15, "You can cast one 8th-level spell once without expending a spell slot."),
#     (12, "Mystic Arcanum (9th level)", 17, "You can cast one 9th-level spell once without expending a spell slot."),
#     (12, "Eldritch Master", 20, "You can spend 1 minute entreating your patron to regain all your expended spell slots."),
#     (12, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (12, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (12, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (12, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', warlock_features)


# wizard_features = [
#     (13, "Spellcasting", 1, "You can cast Wizard spells, using Intelligence as your spellcasting ability."),
#     (13, "Arcane Recovery", 1, "You can regain some of your magical energy by studying your spellbook during a short rest."),
#     (13, "Arcane Tradition", 2, "Choose a school of magic to focus on, which grants you features at 2nd, 6th, 10th, and 14th levels."),
#     (13, "Ability Score Improvement", 4, "Increase one ability score by 2, or two ability scores by 1."),
#     (13, "Spell Mastery", 18, "You can cast a 1st-level or 2nd-level spell from your spellbook at its lowest level without expending a spell slot."),
#     (13, "Signature Spells", 20, "You gain two 3rd-level Wizard spells that you can cast without expending spell slots."),
#     (13, "Ability Score Improvement", 8, "Increase one ability score by 2, or two ability scores by 1."),
#     (13, "Ability Score Improvement", 12, "Increase one ability score by 2, or two ability scores by 1."),
#     (13, "Ability Score Improvement", 16, "Increase one ability score by 2, or two ability scores by 1."),
#     (13, "Ability Score Improvement", 19, "Increase one ability score by 2, or two ability scores by 1."),
# ]

# c.executemany('INSERT INTO features (class_id, feature_name, level, description) VALUES (?, ?, ?, ?)', wizard_features)


# c.execute('''CREATE TABLE subclasses(
#             class_id INTEGER,
#             subclass_id INTEGER NOT NULL,
#             name TEXT NOT NULL,
#             description TEXT NOT NULL)
#     ''')

# subclasses = [
#     (1, 1, "Alchemist", "You specialize in experimental potion-making, using your alchemical mastery to"
#     "craft powerful elixirs. These potions can heal, bolster defenses or provide various enhancements"
#     "to you and your allies."),
#     (1, 2, "Armorer", "You channel your expertise into crafting magical armor, transforming it"
#     "into a powerful exosuit. This suit enhances your combat abilities, offers exceptional protection"
#     "and can be customized with various magical effects to suit different combat roles."),
#     (1, 3, "Artillerist", "You focus on crafting and using magical cannons and other artillery. By"
#     "summoning arcane turrets, you can deal significant damage from a distance or provide defensive"
#     "support to your allies, making you effective in both offensive and defensive strategies."),
#     (1, 4, "Battle Smith", "You forge a strong bond with a clockwork animal construct that you create"
#     "and command in battle. Along with some minor combat abilities, you also gain the ability to repair"
#     "and reinforce both your construct and other equipment."),
#     (2, 1, "Path of the Ancestral Guardian", "You invoke the spirits of your ancestors to protect yourself"
#     "and your allies in battle. These ancestral spirits can shield your allies and deal extensive damage to your enemies."),
#     (2, 2, "Path of the Battlerager", "Available only for dwarves, you harness your rage into a reckless and frenzied"
#     "fighting style, using unique spiked armor as a weapon. This path allows you to excel in close combat, dealing"
#     "additional damage to anyone foolish enough to come within your reach."),
#     (2, 3, "Path of the Beast", "You channel the power of wild creatures, transforming physical aspects of your"
#     "body to unleash devastating attacks. This includes sprouting claws, fangs or even a tail, offering unique ways"
#     "to damage foes and interact with the battlefield."),
#     (2, 4, "Path of the Berserker", "You give in to the fury of combat, allowing you to fight with a primal ferocity."
#     "While in the grips of your battle rage, you can make extra attacks and ignore effects that would otherwise"
#     "cause damage or slow you down."),
#     (2, 5, "Path of the Giant", "You draw on the might of legendary giants, gaining their strength and abilities."
#     "This path allows you to embody different aspects of giantkind, such as frost or fire, with each option"
#     "enhancing your combat abilities in unique ways."),
#     (2, 6, "Path of the Storm Herald", "You tap into the power of the storm, generating a magical aura"
#     "that affects everything around you. Depending on the environment you choose—tundra, desert, or"
#     "sea—your aura can chill, scorch or lash your enemies with storm-like fury."),
#     (2, 7, "Path of the Totem Warrior", "You forge a spiritual bond with a totem animal spirit,"
#     "emulating the aspects of that being. Each animal spirit—be it bear, eagle, elk, tiger or"
#     "wolf—provides unique strengths and supernatural abilities to aid you and your allies."),
#     (2, 8, "Path of Wild Magic", "Your rage taps into the chaotic force of wild magic, resulting in"
#     "unpredictable arcane side-effects. This path is unique in that that can be both incredibly"
#     "powerful but also relies heavily on random dice roles."),
#     (2, 9, "Path of the Zealot", "You are driven by a divine fury, bolstered by the power of the gods. This"
#     "path not only increases your combat prowess with divine energy but also makes you nearly impossible"
#     "to kill while raging."),
#     (3, 1, "College of Creation", "You harness the magic of creation, channeling the raw chaos that formed"
#     "the universe. This subclass allows you to animate inanimate objects, create performance-enhancing motes"
#     "and summon items temporarily into existence."),
#     (3, 2, "College of Eloquence", "You are a master the art of persuasion, using your words to charm, inspire"
#     "and manipulate others. This subclass grants you abilities that make your speech almost impossible to"
#     "resist and reduce the effectiveness of enemies."),
#     (3, 3, "College of Glamour", "You weave a magic of enchantment and allure, captivating those around you."
#     "This subclass provides you with abilities to charm audiences, command attention and manipulate others’ emotions."),
#     (3, 4, "College of Lore", "You collect bits of knowledge from all manner of stories, songs and spells. This"
#     "subclass enhances your versatility by granting additional proficiencies, magical secrets from other classes"
#     "and the ability to use your knowledge to limit enemy attacks."),
#     (3, 5, "College of Spirits", "You channel the tales and powers of the spirits through your performances. This"
#     "subclass gives you the ability to summon spirits to convey storied fables, granting you and your"
#     "allies a variety of magical effects."),
#     (3, 6, "College of Swords", "You blend performance with martial prowess, using your weapon as both an instrument"
#     "and a conduit for your bardic spells. This subclass focuses on enhancing your combat abilities, allowing for"
#     "flourishes that deal extra damage and bolster your defenses."),
#     (3, 7, "College of Valor", "You inspire others in battle through your courage and prowess. This subclass bolsters"
#     "your martial capabilities, providing an Extra attack and allowing you protect your allies and"
#     "enhance group combat tactics."),
#     (3, 8, "College of Whispers", "You traffic in secrets and fear, using your performances to unsettle and manipulate."
#     "This subclass grants you the power to psychically harm your foes, steal identities and sow paranoia,"
#     "turning your art into a weapon of psychological warfare."),
#     (4, 1, "Arcana Domain", "You blend divine and arcane magic, focusing on spells that manipulate"
#     "and reveal the mysteries of the universe. This domain grants you powerful magical abilities,"
#     "including the use of arcane spells usually reserved for wizards."),
#     (4, 2, "Death Domain", "You harness the powers of death and the undead, focusing on spells"
#     "that cause decay and manipulate life forces. This domain grants abilities that enhance your"
#     "damage against the living and allow you to control the dead."),
#     (4, 3, "Forge Domain", "You are a divine artisan, specializing in the creation and"
#     "manipulation of metal and fire. This domain bestows abilities that enhance your crafting skills,"
#     "protect you with divine armor, and imbuing your weapons with fiery power."),
#     (4, 4, "Grave Domain", "You oversee the line between life and death, aiming to ensure balance and"
#     "respect for the dead. This domain grants abilities to hinder the undead, protect allies on the brink"
#     "of death and maximum the impact of restorative spells."),
#     (4, 5, "Knowledge Domain", "You are a seeker of truth, using your divine magic to uncover secrets and"
#     "enhance your wisdom. This domain provides powers to read thoughts, learn hidden knowledge and become"
#     "proficient in numerous skills and languages."),
#     (4, 6, "Life Domain", "You are a conduit of healing and vitality, specializing in spells that restore"
#     "and sustain life. This domain increases the effectiveness of your healing spells and grants you"
#     "abilities to protect and bolster your allies."),
#     (4, 7, "Light Domain", "You channel the power of light and fire, wielding these elements against the darkness."
#     "This domain provides powerful options to scorch your enemies, dispel darkness, and protect allies with radiant energy."),
#     (4, 8, "Nature Domain", "You are a guardian of the natural world, commanding its elements and creatures."
#     "This domain gives you abilities to charm animals and plants, reshape the terrain and summon nature’s"
#     "wrath to aid you in battle."),
#     (4, 9, "Order Domain", "You impose divine order, using your abilities to control the battlefield"
#     "and bolster lawful actions. This domain allows you to enchant allies with bonus attacks and"
#     "slow the advance of enemy forces."),
#     (4, 10, "Peace Domain", "You promote harmony and tranquility, diffusing conflict and healing"
#     "strife. This domain provides abilities that link allies together, allowing shared healing and protection in battle."),
#     (4, 11, "Tempest Domain", "You command the elements of storms, wielding thunder, lightning"
#     "and wind. This domain grants you control over these elements to shock and push back"
#     "enemies while protecting yourself."),
#     (4, 12, "Trickery Domain", "You revel in deception and mischief, using your divine gifts"
#     "to confuse and mislead. This domain provides stealth and illusion powers, enhancing your"
#     "ability to confuse foes and aid allies covertly."),
#     (4, 13, "Twilight Domain", "You guard against the fears of the night and guide others"
#     "through darkness. This domain bestows powers to comfort allies, manipulate shadows"
#     "and see through the deepest gloom."),
#     (4, 14, "War Domain", "You are a divine warrior, a crusader in the cause of your deity."
#     "This domain blesses you with martial prowess, the ability to make extra attacks and powers"
#     "that boost your strength and endurance in battle."),
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
    'your echo, and even swap places with it for strategic maneuvers."),
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
    'abilities to protect yourself and your allies, while also using non-lethal attacks to slow enemies down."),
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
    (13, 1, "Bladesinger", "Almost entirely exclusive to elves and half-elves,'
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
    
    
#     ]

# c.executemany('''INSERT INTO subclasses (class_id, subclass_id, name, description) VALUES (?, ?, ?, ?)''', subclasses)





# Commit changes and close the connection
conn.commit()
conn.close()




# Example: Fetch and display features for Fighter (class_id 6)
main()
