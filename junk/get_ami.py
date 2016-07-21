#!/home/makayo/.virtualenvs/boto3/bin/python

#import boto3

#from datetime import datetime

#s = boto3.Session()

#ec2 = s.resource('ec2')


#images = ec2.images.filter(  Filters=[{'id' : 'Owners', 'Values': ['557612902255']}])

#for i in images.all():
    #print(i);


#def get_latest(items): latest = max(items, key=itemgetter('Timestamp')); return {'Timestamp': latest['Timestamp'], 'id': latest['id']}

#images = list(ec2.images.filter(Owners=['557612902255']))

# must set aws credentials
import boto3
from datetime import datetime
from dateutil.tz import tzutc
from operator import itemgetter
from functools import partial
from pipe import Pipe

def get_region_history(region):
        remove_windows = partial(filter, lambda item: item['ProductDescription'] != 'Windows')

        items = boto3.client('ec2', region_name=region).describe_spot_price_history(StartTime=datetime.now(tzutc()), InstanceTypes=['g2.2xlarge'])['SpotPriceHistory']
        return items | Pipe(remove_windows)

def get_region_histories():
        regions = [region_description['RegionName'] for region_description in boto3.client('ec2').describe_regions()['Regions']]

        remove_empty_histories = partial(filter, lambda region_history: region_history['history'] != [])

        region_histories = [{'name': region, 'history': get_region_history(region)} for region in regions]
        return region_histories | Pipe(remove_empty_histories)

def get_latest_for_regions():
        region_histories = get_region_histories()

        def get_latest(items): latest = max(items, key=itemgetter('Timestamp')); return {'Timestamp': latest['Timestamp'], 'SpotPrice': latest['SpotPrice']}

        sort_by_desc_timestamp = partial(sorted, key=lambda item: item['latest']['Timestamp'], reverse=True)

        latest_for_region = [{ 'name': region_history['name'], 'latest': get_latest(region_history['history']) } for region_history in region_histories]
        return latest_for_region | Pipe(sort_by_desc_timestamp)

for item in get_latest_for_regions(): print item
print "now: ", datetime.now(tzutc())








