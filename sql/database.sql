BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Moves" (
	"moveID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"characterCode"	TEXT,
	"input"	TEXT,
	"button"	TEXT,
	"name"	TEXT,
	"damage"	TEXT,
	"guardType"	TEXT,
	"startup"	TEXT,
	"active"	TEXT,
	"recovery"	TEXT,
	"onBlock"	TEXT,
	"onHit"	TEXT,
	"level"	TEXT,
	"invuln"	TEXT,
	"stance"	TEXT,
	"moveType"	TEXT,
	"strength"	TEXT
);
CREATE TABLE IF NOT EXISTS "Characters" (
	"characterCode"	TEXT NOT NULL UNIQUE,
	"characterName"	TEXT,
	"health"	TEXT,
	"prejump"	TEXT,
	"backdash"	TEXT,
	"notes"	TEXT,
	"game"	TEXT,
	PRIMARY KEY("characterCode")
);
CREATE TABLE IF NOT EXISTS "CharacterAlias" (
	"characterCode"	TEXT,
	"alias"	TEXT
);
CREATE TABLE IF NOT EXISTS "AlternateInputs" (
	"inputID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"realInput"	TEXT,
	"alternateInput"	TEXT
);
COMMIT;
