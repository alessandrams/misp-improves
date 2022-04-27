import json

with open('geolocations.txt', 'r') as f:
    relevant_geolocations = f.read().splitlines()

print(relevant_geolocations)
