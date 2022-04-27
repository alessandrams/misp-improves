import json

f = open("teste.json")

data = json.load(f)
print(type(data))


for g in data['Galaxy']:
    for gc in g['GalaxyCluster']:
        print(gc['galaxy_id'])
        print(gc['value'])