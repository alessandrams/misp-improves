#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from pymisp import MISPEvent
from keys import misp_url, misp_key, misp_verifycert
from datetime import date, timedelta


def check_geolocation_galaxy(cluster):
    with open('geolocations.txt', 'r') as f:
        relevant_geolocations = f.read().splitlines()

    if cluster in relevant_geolocations:
        return True
    else:
        return False    

def check_sector_galaxy(cluster):
    with open('sectors.txt', 'r') as f:
        relevant_sectors = f.read().splitlines()

    if cluster in relevant_sectors:
        return True
    else:
        return False    


if __name__ == '__main__':

    ## IDs MPH:
    ## 11 = Country
    ## 52 = Target Information
    ## 47 = Sector

    date_search = date.today() - timedelta(26)

    with open('galaxies_ids.txt', 'r') as f:
        relevant_galaxy_ids = f.read().splitlines()  

    misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)

    events = misp.search(date_from=date_search, metadata=True)

    for event in events:
        for galaxy in event['Event']['Galaxy']:
            if galaxy['id'] in relevant_galaxy_ids:
                for cluster in galaxy['GalaxyCluster']:
                    if check_geolocation_galaxy(cluster['value']) or check_sector_galaxy(cluster['value']):
                        event_test = misp.get_event(event['Event']['id'], pythonify=True)
                        event_test.add_tag('import:opencti')
                        misp.update_event(event_test)

