import json
import urllib
import time
import pandas as pd

base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
# key = 'AIzaSyAdDHu8-X-20qcuOd4Pe_5dAMSTSNkUeB0'
key = 'AIzaSyBfbwmJ8l316yK8AmRvWHIVrWp1wm8YepM'


def main():
    global next_page
    # loc = '12.928562,77.6135046'
    # radius = 5000
    # getPlaces(loc, radius)
    radius = 315
    # data = pd.read_csv('../visualization/grid.csv')[390:400]
    data = pd.read_csv('delhi_grid.csv')
    data['location'] = data.lat.astype(str) + ',' + data.lng.astype(str)
    print len(data), 'locations'

    for ind in data.index:
        getPlaces(ind, data.loc[ind, 'location'], radius)
    pg = 1
    while (1):
        time.sleep(20)
        page = next_page[:]
        if len(page) == 0:
            break
        pg += 1
        next_page = []
        print len(page), 'locations in page', pg
        for i in xrange(len(page)):
            getPlaces(i, pagetoken=page[i])

        #     page3 = next_page[:]
        #     next_page = []
        #     print len(page3), 'locations in page 3'
        #     for i in xrange(len(page3)):
        #         getPlaces(i, pagetoken=page2[i])
        #     print len(next_page), 'locations in page4'
        # print '\n'.join(next_page)
    print 'Process complete'


def getPlaces(ind, loc='', radius=500, pagetoken=''):
    global next_page
    if len(loc):
        args = {'key': key, 'location': loc, 'radius': radius}
    elif len(pagetoken):
        args = {'key': key, 'pagetoken': pagetoken}
    else:
        return
    url = base_url + urllib.urlencode(args)
    result = urllib.urlopen(url)
    result = json.load(result)

    # c = 'print'
    # while (c != ''):
    #     c = raw_input()
    #     exec c

    if result['status'] == 'OK':
        write(result)
        if len(loc):
            print 'Debug: id =', ind, ', location =', loc, ', address count =', \
                len(result['results']), ' next_page_token =', 1 * \
                (len(result.get('next_page_token', '')) > 0)
        else:
            print 'Debug: id =', ind, ', address count =', len(result['results']), \
                ' next_page_token =', 1*(len(result.get('next_page_token', '')) > 0)
    else:
        print 'Error: id =', ind, ', pagetoken =', pagetoken
        print result

    if result.has_key('next_page_token'):
        next_page.append(result['next_page_token'])


# def write(result, fname, mode='w'):
#     f = open(fname, mode)
#     fields = result['results'][0].keys()
#     fields.remove('geometry')
#     # print fields
#     if mode == 'w':
#         f.write(','.join(fields) + ',lat,lng,ne_lat,ne_lng,sw_lat,sw_lng\n')
#     for row in result['results']:
#         # print row
#         f.write('"' + '","'.join(str(row[x]) for x in fields) + '",')
#         f.write('"' + '","'.join(str(x) for x in [row['geometry']['location']['lat'],
#                                                   row['geometry']['location']['lng'],
#                                                   row['geometry']['viewport'][
#                                                       'northeast']['lat'],
#                                                   row['geometry']['viewport'][
#                                                       'northeast']['lng'],
#                                                   row['geometry']['viewport'][
#                                                       'southwest']['lat'],
#                                                   row['geometry']['viewport'][
#            `                                           'southwest']['lng']]) + '"\n')

#     f.close()

def write(result):
    for row in result['results']:
        print >> f, json.dumps(row)

if __name__ == "__main__":
    # f = open('mumbai_places_json_test.csv', 'w')
    f = open('delhi_places_json_v3.csv', 'w')
    next_page = []
    main()
    f.close()
