import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import utilities as ut

def getStrengthFromButton(button):
    if(button == ""):
        return ""
    if(button == "L" or button == "l"):
        return "light"
    if(button == "M" or button == "m"):
        return "medium"
    if(button == "H" or button == "h"):
        return "heavy"

def parseDustloop(characterName, URL, section, moveType, game):
    characterPage = characterName.replace(' ', '_')
    page = game + '/' + characterPage + '/Frame_Data'
    PARAMS = {"page":page, "action":"parse", "prop":"text", "format":"json", "formatversion":2, "section":section, "prop":"text" }    
    r = requests.get(URL, params = PARAMS)

    if "parse" not in r.json():
        print("Could not locate page for " + characterName)
        return;
    html = r.json()["parse"]["text"]    

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')
    if(table is None):
        print("The character " + characterName + " is missing the page " + moveType)
        return
    df = pd.read_html(str(table))    
    df = pd.DataFrame(df[0])
    if len(df.index) > 1:
        df.drop(df.index[-1], inplace=True)
    return df.reset_index()
    
def insertCharacterData(cursor, character, game, URL):
    insert = 'INSERT INTO Characters (characterCode, characterName, health, prejump, backdash, game) VALUES(?, ?, ?, ?, ?, ?)'
    df = parseDustloop(character['name'],  URL, 2, 'System Data', game)
    values = (
        character['code'],
        character['name'], 
        '', '', '',
        #ut.getValueOrNull(df, df.iloc[0], 'health'),
        #ut.getValueOrNull(df, df.iloc[0], 'prejump'),
        #ut.getValueOrNull(df, df.iloc[0], 'backdash'),
        game
    )
    cursor.execute(insert, values)

def insertMoves(df, cursor, characterCode, moveType):
    if(df is None):
        return
    for index, row in df.iterrows():
        insert = """INSERT INTO Moves (characterCode, input, button, name, damage, guardType, startup, active, recovery, onBlock, onHit, level, invuln, moveType, strength) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""        
        command = getMotionAndInput(ut.getValueOrNull(df, row, 'input'))   
        values = (characterCode
                  ,command[0]
                  ,command[1]
                  ,ut.getValueOrNull(df, row, 'name')
                  ,ut.getValueOrNull(df, row, 'damage')
                  ,ut.getValueOrNull(df, row, 'guard')
                  ,ut.getValueOrNull(df, row, 'startup')
                  ,ut.getValueOrNull(df, row, 'active')
                  ,ut.getValueOrNull(df, row, 'recovery')
                  ,ut.getValueOrNull(df, row, 'onBlock')
                  ,ut.getValueOrNull(df, row, 'onHit')
                  ,ut.getValueOrNull(df, row, 'level')
                  ,ut.getValueOrNull(df, row, 'invuln')                  
                  ,moveType                  
                  ,getStrengthFromButton(command[1])
                  )        
        cursor.execute(insert, values)

def parseAndInsertMoves(characterName, characterCode, URL, section, moveType, cursor, game):
    df = parseDustloop(characterName, URL, section, moveType, game)
    insertMoves(df, cursor, characterCode, moveType)

def getMotionAndInput(command):
    if(command is None):
        return ("", "")
    if(command.find('lvl') != -1):
        command = ut.moveSubstringToStart(command, 'lvl')
    elif(command.find('lv') != -1):
        command = ut.moveSubstringToStart(command, 'lv')
    if(command[len(command) -1] == ']'):
        bracket = command.find('[')
        closeBracket = command.find(']')
        return(command[0:bracket], command[bracket:bracket + closeBracket - bracket + 1])
    else:
        return (command[:-1].replace(' ', '.'), ut.getLastCharacter(command))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        