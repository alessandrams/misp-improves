#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from pymisp import MISPEvent
from keys import misp_url, misp_key, misp_verifycert
from datetime import date, timedelta

## Funcao para fazer o match de cluster de geolocalizacoes relevantes
#### Verifica se o evento possui em suas galaxias algum dos paises listados no arquivo ./key-words/geolocations.txt
#### *IMPORTANTE*: 1- os paises devem ser adicionados ao arquivo "geolocations.txt" com todas as letras minusculas;
####               2- cada linha deve conter apenas um pais;
####               3- o nome do pais deve ser igual ao cluster já existente no MISP (em ingles)

def check_geolocation_galaxy(cluster):
    with open('key-words/geolocations.txt', 'r') as f:
        relevant_geolocations = f.read().splitlines()

    if cluster.casefold() in relevant_geolocations:
        return True
    else:
        return False    


## Funcao para fazer o match de cluster de verticais de negocio relevantes
#### Verifica se o evento possui em suas galaxias algum dos setores listados no arquivo ./key-words/sectors.txt
#### *IMPORTANTE*: 1- os setores devem ser adicionados ao arquivo "sectors.txt" com todas as letras minusculas;
####               2- cada linha deve conter apenas um setor;
####               3- o nome do setor deve ser igual ao cluster já existente no MISP 

def check_sector_galaxy(cluster):
    with open('key-words/sectors.txt', 'r') as f:
        relevant_sectors = f.read().splitlines()

    if cluster.casefold() in relevant_sectors:
        return True
    else:
        return False    


if __name__ == '__main__':

    ## IDs Galaxies MPH:
    ## 11 = Country
    ## 52 = Target Information
    ## 47 = Sector

    ## Subtracao de datas para coletar apenas eventos do dia anterior a execucao do script 

    date_search = date.today() - timedelta(35)


    ## Verifica as galaxias que devem ser consideradas
    ## Caso seja necessario considerar novas galaxias, basta adicionar o ID da galaxia no arquivo ./key-words/galaxies_ids.txt 
    
    with open('key-words/galaxies_ids.txt', 'r') as f:
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

