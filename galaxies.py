#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from pymisp import MISPEvent
from keys import misp_url, misp_key, misp_verifycert


def check_geolocation_galaxy(cluster):
    relevant_geolocations = ["Brazil","brazil","Ukraine"]

    if cluster in relevant_geolocations:
        return True
    else:
        return False    


if __name__ == '__main__':

    ## IDs CEPESC:
    ## 12 = Country
    ## 53 = Target Information
    #relevant_galaxy_ids = ["12","53"]   

    ## IDs MPH:
    ## 12 = Country
    ## 53 = Target Information

    relevant_galaxy_ids = ["11","52"]   

    misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)

    events = misp.search(org='CUDESO', metadata=True)

    for event in events:
        for galaxy in event['Event']['Galaxy']:
            if galaxy['id'] in relevant_galaxy_ids:
                for cluster in galaxy['GalaxyCluster']:
                    if check_geolocation_galaxy(cluster['value']):
                        event_test = misp.get_event(event['Event']['id'], pythonify=True)
                        print(event_test.info)
                        event_test.add_tag('BitRAT')
                        print(event_test.info)
                        misp.update_event(event_test)
                        print(event['Event']['id'])
                        print(cluster['value'])

