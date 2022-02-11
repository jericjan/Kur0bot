import json

f = open('modules/commands.json')
data = json.load(f)
comm_list = []
for i in data:
  comm_list +=data[i]

print(','.join(comm_list))
f.close()
