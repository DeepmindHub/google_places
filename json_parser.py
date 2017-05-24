import json
import pandas as pd
import time


def main():

    json_data = open('delhi_places_json_v3.csv')
    data = pd.DataFrame([], columns=['rating', 'permanently_closed', 'name', 'reference',
                                     'price_level', 'lat', 'lng', 'opening_hours', 'place_id',
                                     'vicinity', 'scope', 'id', 'types', 'icon'])
    st = time.time()
    line = json_data.readline()
    count = 1
    while line and (count <= 1000):
        if (count % 100) == 0:
            print count
        row = parse(line)
        data = data.append(row, ignore_index=True)
        line = json_data.readline()
        count += 1

    end = time.time()
    print 'processing time:', end - st
    # # print keys
    # data = pd.read_csv('delhi_places_v3.csv')
    print len(data), 'records before deduplication'
    data.drop_duplicates('place_id', inplace=True)
    p rint len(data), 'records after deduplication'
    data.to_csv('delhi_places_v3.csv', index=False, encoding='utf-8')


def parse(line):
    # global keys
    line = json.loads(line)
    row = line.copy()
    if 'geometry' in row.keys():
        del row['geometry']
        row.update(line['geometry']['location'])
    if 'types' in row.keys():
        row['types'] = ', '.join(row['types'])
    if 'photos' in row.keys():
        del row['photos']
    # photos = line['photos']
    return row

    # keys.update(line.keys())

# keys = set()
if __name__ == '__main__':
    main()
