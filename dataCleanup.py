import sqlite3
import json

def cleandataGranblue(cursor):
	select = 'SELECT * FROM Moves WHERE characterCode = ?'
    params = ('VIRA')
    result = cursor.execute()
    
    UPDATE Moves
    SET input = SUBSTRING(input, 5, LENGTH(input)), stance = 'grand'
    WHERE characterCode = 'VIRA' AND input LIKE 'grand%'
    