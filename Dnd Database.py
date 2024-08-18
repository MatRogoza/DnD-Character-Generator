#allows access to sqlite database
import sqlite3

#connects to the database dnd_character_generator
conn = sqlite3.connect('dnd_character_generator.db')

#needed to be able to navigate the database
c = conn.cursor()

#creates a new table called classes and add a number id, name of class, hit_die number, and short description
# c.execute("""Create Table classes (
#             id INTEGER PRIMARY KEY,
#             name text NOT NULL,
#             hit_die TEXT NOT NULL,
#             description TEXT
#             )""")

#created tuples for each class in the format of the classes table
classes = [
    (1, 'Artificer', 'd8', 
     'A master of invention, creating magical objects and technology.'),
    (2, 'Barbarian', 'd12', 
     'A fierce warrior of primitive background who can enter a battle rage.'),
    (3, 'Bard', 'd8', 
     'An inspiring magician whose power echoes the music of creation.'),
    (4, 'Cleric', 'd8', 
     'A priestly champion who wields divine magic in service of a higher power.'),
    (5, 'Druid', 'd8', 
     'A priest of the Old Faith, wielding the powers of nature and adopting '
     'animal forms.'),
    (6, 'Fighter', 'd10', 
     'A master of martial combat, skilled with a variety of weapons and armor.'),
    (7, 'Monk', 'd8', 
     'A master of martial arts, harnessing the power of the body in pursuit of '
     'physical and spiritual perfection.'),
    (8, 'Paladin', 'd10', 
     'A holy warrior bound to a sacred oath.'),
    (9, 'Ranger', 'd10', 
     'A warrior who uses martial prowess and nature magic to combat threats '
     'on the edges of civilization.'),
    (10, 'Rogue', 'd8', 
     'A scoundrel who uses stealth and trickery to overcome obstacles and enemies.'),
    (11, 'Sorcerer', 'd6', 
     'A spellcaster who draws on inherent magic from a gift or bloodline.'),
    (12, 'Warlock', 'd8', 
     'A wielder of magic that is derived from a bargain with an extraplanar entity.'),
    (13, 'Wizard', 'd6', 
     'A scholarly magic-user capable of manipulating the structures of reality.')
]
# Saving each class to the database
for cls in classes:
    cls.save_to_db(conn)


#printing the info of the class tables
# def fetch_class_data(class_name):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM classes WHERE name = ?", (class_name,))
#     result = cursor.fetchone()  # Fetches the first row that matches the query
    
#     if result:
#         print("ID:", result[0])
#         print("Name:", result[1])
#         print("Hit Die:", result[2])
#         print("Description:", result[3])
#     else:
#         print(f"No class found with the name '{class_name}'.")

# Example: Fetch and print data for the 'Wizard' class
# fetch_class_data('Wizard')












#created a table for class features, 
# c.execute("""CREATE TABLE features (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     description TEXT NOT NULL,
#     level_acquired INTEGER NOT NULL,
#     class_id INTEGER NOT NULL,
#     FOREIGN KEY (class_id) REFERENCES classes(id)
#     )""")

# features = [
#     (1, 'Second Wind', 'You have a limited well of stamina that you can draw on'
#     'to protect yourself from harm. On your turn, you can use a bonus action to'
#     'regain hit points equal to 1d10 + your fighter level. \nOnce you use this'
#     'feature, you must finish a short or long rest before you can use it again.', 1, 6),
#     (2, 'Action Surge (1 use)', 'Starting at 2nd level, you can push yourself'
#     'beyond your normal limits for a moment. On your turn, you can take one'
#     'additional action. \nOnce you use this feature, you must finish a short'
#     'or long rest before you can use it again. Starting at 17th level, you'
#     'can use it twice before a rest, but only once on the same turn.', 2, 6),
#     (3, 'Martial Archetype', 'You choose an archetype that you strive to'
#     'emulate in your combat styles and techniques.', 3, 6),
#     (4, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 4, 6),
#     (5, 'Extra Attack (1)', 'Beginning at 5th level, you can attack twice,'
#     'instead of once, whenever you take the Attack action on your turn. \nThe'
#     'number of attacks increases to three when you reach 11th level in this'
#     'class and to four when you reach 20th level in this class.', 5, 6),
#     (6, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 6, 6),
#     (7, 'Martial Archetype Feature', 'You gain a feature from your chosen'
#     'Martial Archetype.', 7, 6),
#     (8, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 8, 6),
#     (9, 'Indomitable (1 use)', "Beginning at 9th level, you can reroll a"
#     "saving throw that you fail. If you do so, you must use the new roll,"
#     "and you can't use this feature again until you finish a long rest. \nYou"
#     "can use this feature twice between long rests starting at 13th level"
#     "and three times between long rests starting at 17th level.", 9, 6),
#     (10, 'Martial Archetype Feature', 'You gain a feature from your chosen'
#     'Martial Archetype.', 10, 6),
#     (11, 'Extra Attack (2)', 'You can attack three times whenever you take'
#     'the Attack action on your turn.', 11, 6),
#     (12, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 12, 6),
#     (13, 'Indomitable (2 uses)', 'You can reroll a saving throw that you'
#     'fail twice per long rest.', 13, 6),
#     (14, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 14, 6),
#     (15, 'Martial Archetype Feature', 'You gain a feature from your chosen'
#     'Martial Archetype.', 15, 6),
#     (16, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 16, 6),
#     (17, 'Action Surge (2 uses)', 'You can use Action Surge twice per short'
#     'or long rest.', 17, 6),
#     (18, 'Indomitable (3 uses)', 'You can reroll a saving throw that you'
#     'fail three times per long rest.', 17, 6),
#     (19, 'Martial Archetype Feature', 'You gain a feature from your chosen'
#     'Martial Archetype.', 18, 6),
#     (20, 'Ability Score Improvement', 'You can increase one ability score'
#     'by 2, or you can increase two ability scores by 1 each.', 19, 6),
#     (21, 'Extra Attack (3)', 'You can attack four times whenever you take'
#     'the Attack action on your turn.', 20, 6)
# ]

# Insert data into Features
#c.executemany('INSERT INTO features VALUES (?, ?, ?, ?, ?)', features)



#saves data into the dnd_character_generator file
conn.commit()

#closes out the dnd_character_generator file
conn.close()
