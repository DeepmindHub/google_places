import pandas as pd
import re
import geopy
from geopy.geocoders import GoogleV3


def main():
    addresses = pd.read_csv('../limetray_sublocality/cleaned_sl_chennai.csv')
    print addresses.shape
    addresses['full_address'] = addresses.apply(addCity, axis=1)
    # print addresses.head()
    # exit(-1)
    # addresses['full_address'] = addresses.apply(encode, axis=1)
    addresses['cleaned_address'] = addresses.full_address.apply(cleanAddress)
    addresses[['standard_address', 'new_latitude', 'new_longitude']
              ] = addresses.cleaned_address.apply(getLatLng)
    # addresses['standard_address'] = addresses.standard_address.apply(
    #     lambda x: x.decode('utf=8').encode('utf-8', 'ignore'))
    addresses.to_csv(
        '../limetray_sublocality/cleaned_sl_chennai_v2.csv', encoding='utf-8', index=False)


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
    except (geopy.exc.GeocoderTimedOut, geopy.exc.GeocoderQueryError) as e:
        print 'Cannot geocode', address
        # print 'Service timed out'
        print e
        return pd.Series(['', -1, -1],
                         index=['standard_address', 'latitude', 'longitude'])


def addCity(address_row):
    if (address_row.city in address_row.sublocality) or (address_row.sublocality == ''):
        return address_row.sublocality
    else:
        return address_row.sublocality + ", " + address_row.city


def encode(address):
    try:
        return address['full_address'].decode('utf=8').encode('utf-8', 'ignore')
    except UnicodeDecodeError, e:
        print address
        print e
        exit(-1)

geolocator = GoogleV3('############')
if __name__ == "__main__":
    main()
