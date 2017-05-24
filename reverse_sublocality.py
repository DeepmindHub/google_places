import pandas as pd
import re
import time
import geopy
import json
from geopy.geocoders import GoogleV3


def main():
    locations = pd.read_csv('LT_duplicate_sl_names_v2.csv')
    print locations.shape
    # print locations.head(10)
    # exit(-1)
    # locations['address'] = locations.lat_lng.apply(getAddress)
    # locations.to_csv('LT_duplicate_sl_names_v2.csv', encoding='utf-8', index=False)
    locations['sublocality'] = locations.address.apply(getSublocality)
    print locations.sublocality.head(10)
    locations.to_csv('LT_duplicate_sl_names_v2.csv', encoding='utf-8', index=False)


def getAddress(loc):
    try:
        return json.dumps(geolocator.reverse(loc, True)._raw)
    except geopy.exc.GeocoderTimedOut:
        # time.sleep(1)
        # return str(geolocator.reverse(loc, True)._raw)
        return ''


def getSublocality(address):
    if len(address) == 0:
        return ''
    # try:
    #     address = json.loads(address)
    # except:
    #     print address
    #     exit(-1)
    address = json.loads(address)
    components = ['sublocality_level_3', 'sublocality_level_2', 'sublocality_level_1']
    sublocality = ''
    for comp in components:
        text = [x['long_name'] for x in
                address['address_components'] if (comp in x['types'])]
        if len(text):
            if len(sublocality):
                sublocality += ', '
            sublocality += text[0]
    return sublocality

geolocator = GoogleV3('AIzaSyAdDHu8-X-20qcuOd4Pe_5dAMSTSNkUeB0')
if __name__ == "__main__":
    main()
