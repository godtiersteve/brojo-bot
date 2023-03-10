import sqlite3
import utilities as ut

def getCharacterName(cursor, charCode):
    return cursor.execute("SELECT characterName FROM Characters WHERE characterCode LIKE ?", (charCode,)).fetchone()[0]
    
def getMoveText(name, row):
    return name + " - (" + row["name"] + " - " + row["input"] + row["button"]  + ") [Startup]: " + row["startup"] + "[Active]: " + row["active"] + "[Recovery]: " + row["recovery"]           

def cleanInput(cursor, command):
    if(command.isnumeric()):
        return command;
    return cursor.execute("SELECT realInput FROM AlternateInputs WHERE alternateInput LIKE ?", (command,)).fetchone()[0]

def getCharacterCode(cursor, query):
    return cursor.execute("SELECT characterCode FROM Characters WHERE characterName LIKE ? OR characterCode LIKE ?", (query, query)).fetchone()[0]
    
conn = sqlite3.connect('granblue.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
conn.set_trace_callback(print)

name = getCharacterName(cursor, "NARM")

query = "236L"
characterCode = "NARM"
command = cleanInput(cursor, query[:-1])
button = ut.getLastCharacter(query)
select = "SELECT * FROM Moves WHERE characterCode LIKE ? AND input LIKE ? AND button LIKE ?"
values = (characterCode, command, button)
rows = cursor.execute(select, values)
for row in rows:
    print(getMoveText(name, row))