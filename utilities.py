import pandas as pd

def getLastCharacter(str):
	return str[len(str) - 1]
    
def moveSubstringToStart(str, sub):    
    sub = str[str.find(sub):str.find(sub) + len(sub)]    
    str = str.replace(sub, '')
    str = str.replace(' ', '')
    return sub + "." + str    
    
def getValueOrNull(df, row, keyName):
    if(keyName in df.columns.tolist()):
        return row[keyName]
    return None
    
def getValueOrEmptyString(row, keyName):
    if(keyName in row):
        return row[keyName]
    return ""

def emptyStringIfNull(value):
    if(value is None):
        return ""
    return value
    
def dashIfNull(value):
    if(value is None):
        return "-"
    return value