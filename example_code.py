if(command.find('lvl')):
    level = command[command.find('lvl'):command.find('lvl')+4]
    command = command.replace(level, '')
    command = command.replace(' ', '')
    command = level + "." + command
print(command)    