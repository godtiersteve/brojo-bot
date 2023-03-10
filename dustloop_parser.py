import parse_funcs as pf
import sqlite3
import json

def loadCharacterData(character, URL, sections, cursor, game):
    print('Generating data for ' + character['name'] + '...')    
    if('sections' not in character):
        for section in sections:            
            pf.parseAndInsertMoves(character['name'], character['code'], URL, section['id'], section['name'], cursor)
    else:
        for section in character['sections']:            
            pf.parseAndInsertMoves(character['name'], character['code'], URL, section['id'], section['name'], cursor)

conn = sqlite3.connect('granblue.db')
cursor = conn.cursor()

f = open('granblue_characters.json')
data = json.load(f)
URL = data['url']
game = data['game']
cursor.execute('DELETE FROM Characters WHERE game = ?', (data['game'],))
pf.parseSection('Narmaya', URL, 4, 'Normal')
for character in data['characters']:
    cursor.execute('DELETE FROM Moves WHERE characterCode = ?', (character['code'],))
    pf.insertCharacterData(cursor, character, game, URL)
    loadCharacterData(character, URL, data['sections'], cursor, game)
    if("aliases" in character):
        aliases = character['aliases'].split(', ')
        cursor.execute('DELETE FROM CharacterAlias WHERE characterCode = ?', (character['code'],))
        for alias in aliases:
            insert = 'INSERT INTO CharacterAlias(characterCode, alias) VALUES(?, ?)'
            values = (character['code'], alias)
            cursor.execute(insert, values)

conn.commit()
conn.close()