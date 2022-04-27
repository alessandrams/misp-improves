#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from pymisp import MISPEvent
from keys import misp_url, misp_key, misp_verifycert
import argparse
import os
import json

def check_geolocation_galaxy(cluster):
    relevant_geolocations = ["Brazil","brazil","Ukraine"]

    if cluster in relevant_geolocations:
        return True
    else:
        return False    


if __name__ == '__main__':

    ## IDs:
    ## 12 = Country
    ## 53 = Target Information

    relevant_galaxy_ids = ["12","53"]   

#    parser = argparse.ArgumentParser(description='Get an event from a MISP instance.')
#    parser.add_argument("-e", "--event", required=True, help="Event ID to get.")
#    parser.add_argument("-o", "--output", help="Output file")

#    args = parser.parse_args()

#    if args.output is not None and os.path.exists(args.output):
#        print('Output file already exists, abort.')
#        exit(0)

    misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)

    events = misp.search(org='ICS-CSIRT.io', metadata=True)
    print(type(events))

    for event in events:
        #print(event)
        event_result = json.dumps(event, indent=2)
        print(event_result)
        # for g in event_result['Galaxy']:
        #     for gc in g['GalaxyCluster']:
        #         galaxy_id = gc['galaxy_id']
        #         if galaxy_id in relevant_galaxy_ids:
        #             if check_geolocation_galaxy(gc['value']):
        #                 print(type(event))
        #                 print(event.info)
        #                 event.add_tag('Buer')
        #                 print(gc['value'])
        #                 event.publish()

    



    # event = misp.get_event(args.event, pythonify=True)
    # if args.output:
    #     with open(args.output, 'w') as f:
    #         f.write(event.to_json())
    # else:
    #     event_result = json.loads(event.to_json())
    #     for g in event_result['Galaxy']:
    #         for gc in g['GalaxyCluster']:
    #             galaxy_id = gc['galaxy_id']
    #             if galaxy_id in relevant_galaxy_ids:
    #                 if check_geolocation_galaxy(gc['value']):
    #                     print(type(event))
    #                     print(event.info)
    #                     event.add_tag('Buer')
    #                     print(gc['value'])
    #                     event.publish()

    #             #print(gc['galaxy_id'])
    #             #print(gc['value'])
    #             #print(json.dumps(event_result, indent=2))
