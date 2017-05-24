import pandas as pd
import re
from geopy.geocoders import GoogleV3


def main():
    addresses = pd.read_csv('reverse_addresses.csv')
    print addresses.shape
    # print addresses[:5]
    addresses['cleaned_address'] = addresses.address.apply(cleanAddress)
    addresses[['standard_address', 'latitude', 'longitude']
              ] = addresses.cleaned_address.apply(getLatLng)
    addresses.to_csv('reverse_addresses_v2.csv', index=False)


def cleanAddress(address):
    address = address.lower()
    address = re.sub(r'(behind)|(near)|(off)|(opp(osite)?)|(above)|(landmark:?)|' +
                     r'(next([ ]*to)?)|(close([ ]*to)?)|(nr)|(infront([ ]*of)?)|(besides?)|' +
                     r'(close[ ]*to)|(\bnull\b)|(pick[ ]*up)', '', address)
    address = re.sub(r'(\A\W+)|(\W+\Z)', '', address)
    # address = re.sub(r'([a-z0-9])[ ]*([1-8][0-9]{2}[ ]*[0-9]{3})', r'\1, \2', address)
    address = re.sub(r'[\s]*[,;\n]+[,\s]*', ', ', address)
    address = re.sub(r'\s+', ' ', address)
    address = address.replace('|', '')
    return address


def getLatLng(address):
    try:
        loc = geolocator.geocode(address)
        if loc:
            return pd.Series([loc.address, loc.latitude, loc.longitude],
                             index=['standard_address', 'latitude', 'longitude'])
        else:
            return pd.Series(['', -1, -1],
                             index=['standard_address', 'latitude', 'longitude'])
    except geopy.exc.GeocoderTimedOut, e:
        print 'Cannot geocode', address
        print 'Service timed out'
        return pd.Series(['', -1, -1],
                         index=['standard_address', 'latitude', 'longitude'])

geolocator = GoogleV3('AIzaSyAdDHu8-X-20qcuOd4Pe_5dAMSTSNkUeB0')
if __name__ == "__main__":
    main()
