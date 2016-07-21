#!/home/makayo/.virtualenvs/boto3/bin/python

#import boto3

#from datetime import datetime

#s = boto3.Session()

#ec2 = s.resource('ec2')


#images = ec2.images.filter(  Filters=[{'id' : 'Owners', 'Values': ['557612902255']}])

#for i in images.all():
    #print(i);


#def get_latest(items): latest = max(items, key=itemgetter('Timestamp')); return {'Timestamp': latest['Timestamp'], 'id': latest['id']}
s = boto3.Session()
ec2 = s.resource('ec2')
myid='557612902255'
#client=boto3.client('ec2')
images = list(ec2.images.filter(Owners=[myid]))
"""
#from datetime import datetime
#2016-07-15T22:46:33.000Z
#newstr = oldstr.replace("M", "")
#date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
#date_object = datetime.strptime(images[0].creation_date.replace("T","").replace("Z",""), '%Y-%m-%d %H:%M:%S')
#images[0].creation_date.replace('T',' ').replace('Z','')
"""
def getdate(datestr):
    ix=datestr.replace('T',' ')
    ix=ix[0:len(ix)-5]
    idx=datetime.strptime(ix,'%Y-%m-%d %H:%M:%S')
    return(idx)
"""
import operator as op
s = sorted(student_objects, key=op.attrgetter('age'))
"""
#y=sorted(images, key=lambda images: images.creation_date)
#y=sorted(images, key=lambda images: images.creation_date)
zz=sorted(images, key=lambda images: getdate(images.creation_date))
latestAmi=zz[len(zz)-1]
#key=lambda student: student.age
#s=sorted(images, key=lambda images: getdate(images))
#s=sorted(images, key=op.attrgetter(creation_date))
#ec2 = boto3.resource('ec2')
#image = ec2.Image('id')
for i in images:
    print(i.id);
    image=ec2.Image(i.id);
    desc=image.describe_attribute( DryRun=False,Attribute="description");
    print(desc);
    print(str(desc));
    print(type(desc));
    print(desc['ResponseMetadata']);
    print(type(desc['ResponseMetadata']));
    print(desc['ResponseMetadata'].keys());
    print(desc['ResponseMetadata']['HTTPHeaders']);
    print(desc['ResponseMetadata']['HTTPHeaders']['date']);
    sort_by_desc_timestamp = partial(sorted, key=lambda item: item['latest']['Timestamp'], reverse=True)


    #ec2.
    #client.describe_images.im_self.describe_image_attribute(ImageId=i.id,Attribute=["Creation_Date"])
    #client.describe_images.im_self.describe_image_attribute(ImageId=i.id,Attribute="•creation_date");
    #client.describe_images.im_self.describe_image_attribute(ImageId=i.id)




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








