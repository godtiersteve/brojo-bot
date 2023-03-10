import nextcord as nc
import utilities as ut

def formatFrameData(row, characterName):
    if(characterName is None):
        characterName = ""
    name = characterName + " (" + ut.getValueOrEmptyString(row, "input") + ut.getValueOrEmptyString(row, "button") + ")" + " - " + ut.getValueOrEmptyString(row, "name")
    if(row["name"] is None):
        name = characterName + " - " + row["input"] + row["button"]
    embed = nc.Embed(title=name)
    embed.add_field(name="Input", value=row["input"], inline=True)
    embed.add_field(name="Guard", value=row["guardType"], inline=True)
    embed.add_field(name="Damage", value=row["damage"], inline=True)
    embed.add_field(name="Startup", value=row["startup"], inline=True)
    embed.add_field(name="Active", value=row["active"], inline=True)
    embed.add_field(name="Recovery", value=row["recovery"], inline=True)
    embed.add_field(name="On Hit", value=row["onHit"], inline=True)
    embed.add_field(name="On Block", value=row["onBlock"], inline=True)
    embed.add_field(name="Attack Level", value=row["level"], inline=True)
    embed.add_field(name="Invincibility", value=row["invuln"], inline=True)
    return embed
    
def fetchFrameDataEmbed(character, command, cursor):       
    characterCode = getCharacterCode(cursor, character)
    characterName = getCharacterName(cursor, characterCode)     
    if(character is not None and command is not None):
        row = getMoveData(cursor, command, character, characterCode)
        if(row is not None):                        
            return formatFrameData(row, characterName)
    return None    

def fetchFrameDataText(character, command, cursor):    
    characterCode = getCharacterCode(cursor, character)
    characterName = getCharacterName(cursor, characterCode)    
    if(character is not None and command is not None):
        row = getMoveData(cursor, command, character, characterCode)
        return getMoveText(characterName, row)        

def getMoveData(cursor, inputCommand, characterCommand, characterCode):        
    command = inputCommand    
    if(ut.getLastCharacter(inputCommand) == ']'):
        bracket = command.find('[')
        command = cleanInput(cursor, command[0:bracket])
        button = inputCommand[bracket:bracket + 3]
    else:
        command = cleanInput(cursor, inputCommand[:-1])    
        button = ut.getLastCharacter(inputCommand)
    print("Input: " + inputCommand)
    print("Output: " + command + button)
    select = ""
    values = ""
    dot = characterCommand.find('.')
    if(dot != -1):
        stance = characterCommand[dot + 1:]        
        select = "SELECT * FROM Moves WHERE characterCode LIKE ? AND input LIKE ? AND button LIKE ? AND stance LIKE ?"        
        values = (characterCode, command, button, stance)     
    else:
        select = "SELECT * FROM Moves WHERE characterCode LIKE ? AND input LIKE ? AND button LIKE ?"
        values = (characterCode, command, button)
    print(select)
    print(values)
    result = cursor.execute(select, values).fetchone()
    if(result is None):
        select = "SELECT * FROM Moves WHERE characterCode LIKE ? AND name LIKE ?"
        values = (characterCode, inputCommand)
        return cursor.execute(select, values).fetchone()
    else:
        return result

def cleanInput(cursor, command):
    if(command.isnumeric()):
        return command;
    result = cursor.execute("SELECT realInput FROM AlternateInputs WHERE alternateInput LIKE ?", (command,)).fetchone()
    if result is not None:
        return result[0]
    return command

def getCharacterCode(cursor, query):
    result = None
    dot = query.find('.')
    if(dot != -1):        
        query = query[:dot]        

    result = cursor.execute("SELECT characterCode FROM Characters WHERE characterName LIKE ? OR characterCode LIKE ?", (query, query)).fetchone()
    if result is not None:
        return result[0]    
    result = cursor.execute('SELECT characterCode FROM characterAlias WHERE alias LIKE ?', (query,)).fetchone()
    if result is not None:
        print(result[0])
        return result[0]   
    return ""

def getCharacterName(cursor, charCode):
    dot = charCode.find('.')
    if(dot != -1):        
        charCode = charCode[:dot]    
    result = cursor.execute("SELECT characterName FROM Characters WHERE characterCode LIKE ?", (charCode,)).fetchone()
    if result is not None:
        return result[0]
    return None

def getMoveText(name, row):
    moveName = ut.emptyStringIfNull(row["name"])
    motion = ut.emptyStringIfNull(row["input"])
    button = ut.emptyStringIfNull(row["button"]) 
    startup = ut.dashIfNull(row["startup"])
    active = ut.dashIfNull(row["active"])
    recovery = ut.dashIfNull(row["recovery"])
    onBlock = ut.dashIfNull(row["onBlock"])
    onHit = ut.dashIfNull(row["onHit"])
    ret = ""
    if(moveName != ""):
        ret =  name + " - (" + moveName + " - " 
    else:
        ret =  name + " - ("
    ret = ret + motion + button + ") - [Startup]: " + startup + " [Active]: " + active + " [Recovery]: " + recovery + " [On Hit]: " + onHit + " [On Block]: " + onBlock
    return ret
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    