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
    
#     ]

# c.executemany('''INSERT INTO subclasses (class_id, subclass_id, name, description) VALUES (?, ?, ?, ?)''', subclasses)





# Commit changes and close the connection
conn.commit()
conn.close()




# Example: Fetch and display features for Fighter (class_id 6)
main()
