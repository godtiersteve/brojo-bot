import utilities as ut

command = "236U lvl2"
command = command.replace("[k]", "").replace("[g]", "")
motion = ""
if(command[len(command) -1] == ']'):
    bracket = command.find('[')
    motion = command[0:bracket]
    button = command[bracket:bracket + 3]
    print("Original Input: " + command)
    print("Motion: " + motion + " Button: " + button)
    
if(command.find('lvl')):
    command = ut.moveSubstringToStart(command, 'lvl')
    print(command)
    
query = 'narm.kagura'
dot = query.find('.')
if(dot != -1):
    stance = query[dot + 1:]
    character = query[:dot]
    print(stance)
    print(character)