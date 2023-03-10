import parse_funcs as pf
import sqlite3
import json

def loadCharacterData(character, URL, sections, cursor, game):
    print('Generating data for ' + character['name'] + '...')    
    if('sections' not in character):
        for section in sections:            
            pf.parseAndInsertMoves(character['name'], character['code'], URL, section['id'], section['name'], cursor, game)
    else:
        for section in character['sections']:            
            pf.parseAndInsertMoves(character['name'], character['code'], URL, section['id'], section['name'], cursor, game)

conn = sqlite3.connect('granblue.db')
cursor = conn.cursor()

#f = open('granblue_characters.json')
f = open('blazblue_characters.json')
json = json.load(f)
URL = json['url']
game = json['game']

cursor.execute('DELETE FROM Characters WHERE game = ?', (json['game'],))
for character in json['characters']:
    cursor.execute('DELETE FROM Moves WHERE characterCode = ?', (character['code'],))
    pf.insertCharacterData(cursor, character, game, URL)
    loadCharacterData(character, URL, json['sections'], cursor, game)
    if("aliases" in character):
        aliases = character['aliases'].split(', ')
        cursor.execute('DELETE FROM CharacterAlias WHERE characterCode = ?', (character['code'],))
        for alias in aliases:
            insert = 'INSERT INTO CharacterAlias(characterCode, alias) VALUES(?, ?)'
            values = (character['code'], alias)
            cursor.execute(insert, values)
            
if('updateScripts' in json):
    for script in json['updateScripts']:
        cursor.execute(script['script'])
        
conn.commit()
conn.close()