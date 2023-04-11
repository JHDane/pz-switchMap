import shutil
import os
import random
import subprocess
import time

subprocess.Popen(['pzserver', 'kill'])

time.sleep(15)

print("lancement du script")

os.remove("/home/pzserver2/pzserver/steamapps/workshop/appworkshop_108600.acf")
dir_delete = ["/home/pzserver2/pzserver/steamapps/workshop/content/108600", "/home/pzserver2/Zomboid/Saves/Multiplayer/servertest"]

shutil.copyfile('/home/pzserver2/Zomboid/db/servertest2.db', '/home/pzserver2/Zomboid/db/servertest.db')

for dir in dir_delete:
    try:
        shutil.rmtree(dir)
    except OSError as erreur:
        print(f"Erreur lors de la suppression du dossier {dir}: {erreur}")


filename = "/home/pzserver2/Zomboid/Server/listmap.txt"

with open(filename, "r") as f:
    lines = f.readlines()
    random_line = random.choice(lines)


map_selected = random_line.split(";")

print("MAP SELECTED : "+map_selected[0])

filename = '/home/pzserver2/Zomboid/Server/servertest.ini'
tempfile = filename + '.tmp'
search_strings = ['Mods=', 'Map=','WorkshopItems=','PublicName=']
new_string = ['PublicName=MAPS ANARCHY - '+map_selected[2].rstrip("\n"),'Mods='+map_selected[0]+'\n', 'Map='+map_selected[2],'WorkshopItems='+map_selected[1]+'\n']

with open(filename, 'r') as f_input, open(tempfile, 'w') as f_output:
    skip_next_line = False
    for line in f_input:
        if skip_next_line:
            skip_next_line = False
            continue
        for i, search_string in enumerate(search_strings):
            if line.startswith(search_string):
                f_output.write(new_string[i])
                break
        else:
            f_output.write(line)

os.replace(tempfile, filename)

map_selected[2] = map_selected[2].rstrip("\n")

with open('/home/pzserver2/Zomboid/Server/servertest_spawnregions.lua', 'r') as f:

    lines = f.readlines()

for i, line in enumerate(lines):
    if "return {" in line:
        start_index = i + 1

for i, line in enumerate(lines):
    if "}" in line and i > start_index:
        end_index = i

new_lines = lines[:start_index]
new_lines.append(f'    {{ name = "{map_selected[0]}", file = "media/maps/{map_selected[2]}/spawnpoints.lua" }},\n')
new_lines.append('}\n')
new_lines.extend(lines[end_index+1:])

with open('/home/pzserver2/Zomboid/Server/servertest_spawnregions.lua', 'w') as f:
    f.writelines(new_lines)

subprocess.Popen(['pzserver', 'start'])
