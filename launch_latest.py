#!/home/makayo/.virtualenvs/boto3/bin/python
import boto3
import time
s = boto3.Session()
ec2 = s.resource('ec2')
myid='557612902255'
images = list(ec2.images.filter(Owners=[myid]))
def getdate(datestr):
    ix=datestr.replace('T',' ')
    ix=ix[0:len(ix)-5]
    idx=time.strptime(ix,'%Y-%m-%d %H:%M:%S')
    return(idx)
zz=sorted(images, key=lambda images: getdate(images.creation_date))
latestAmi=zz[len(zz)-1]

"""
[{u'DeviceName': '/dev/sda1',  u'Ebs': {u'DeleteOnTermination': True,   u'Encrypted': False,   u'SnapshotId': 'snap-d8de3adb',   u'VolumeSize': 50,   u'VolumeType': 'gp2'}}]
"""



#http://boto3.readthedocs.io/en/latest/guide/migrationec2.html
#https://gist.github.com/iMilnb/0ff71b44026cfd7894f8

# Let's use Amazon ec2
#ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

#myimageId='ami-42870a55'
myimageId=latestAmi.id
mysubnetId='subnet-80cdeed8'
myinstanceType='c4.2xlarge'
mykeyName='spot-coursera'
mycount=1
myprice='5.0'
mytype='one-time'
myipAddr='52.205.199.249'
myallocId='eipalloc-d22618e8'
mysecurityGroups=['WebServerSG']
mydisksize=70
mygroupId='sg-14356e6f'
#mygroupId='WebServerSG'
myzone='us-east-1a'
myvpcId='vpc-503dba37'
latestAmi.block_device_mappings[0]['Ebs']['VolumeSize']=mydisksize
#diskSpec=latestAmi.block_device_mappings[0]['Ebs']['VolumeSize']
response = client.request_spot_instances(
            DryRun=False,
                SpotPrice=myprice,
                    ClientToken='string',
                        InstanceCount=1,
                            Type='one-time',
                                LaunchSpecification={
                                        'ImageId': myimageId,
                                                'KeyName': mykeyName,
                                                'SubnetId':mysubnetId,
                                                        #'SecurityGroups': mysecurityGroups,
                                                                'InstanceType': myinstanceType,
                                                                        'Placement': {
                                                                                        'AvailabilityZone': myzone,
                                                                                                }
#                                                                        'BlockDeviceMappings':latestAmi.block_device_mappings
#                                                                                'BlockDeviceMappings': [
#                                                                                                {
#                                                                                                                    'Ebs': {
#                                                                                                                                            'SnapshotId': 'snap-f70deff0',
#                                                                                                                                                                'VolumeSize': 100,
#                                                                                                                                                                                    'DeleteOnTermination': True,
#                                                                                                                                                                                                        'VolumeType': 'gp2',
#                                                                                                                                                                                                                            'Iops': 300,
#                                                                                                                                                                                                                                                'Encrypted': False
#                                                                                                                                                                                                                                                                },
#                                                                                                                                },
#                                                                                                        ],
#
#                                                                                        'EbsOptimized': True,
#                                                                                                'Monitoring': {
#                                                                                                                'Enabled': True
#                                                                                                                        },
#                                                                                                        'SecurityGroupIds': [
#                                                                                                                        'sg-709f8709',
#                                                                                                                                ]
                                                                                                            }
                                )

print(response)
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
while( len(list(instances))==0):
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type);
    response = instance.modify_attribute(Groups=[mygroupId]);
    print(response);


for instance in instances:
    response = client.associate_address(
        #DryRun=True|False,
        DryRun=False,
        #InstanceId='string',
        InstanceId=instance.id,
        #PublicIp='string',
        #AllocationId='string',
        AllocationId=myallocId,
        #NetworkInterfaceId='string',
        #PrivateIpAddress='string',
        #AllowReassociation=True|False
        AllowReassociation=True
    );
    print (response);


# Boto 3
"""
gateway.attach_to_vpc(VpcId=vpc.id)
gateway.detach_from_vpc(VpcId=vpc.id)
"""
#vpc-503dba37 | tst2-20160706
"""
address = ec2.VpcAddress(myvpcId)
address.associate(myallocId)
address.association.delete()
"""








"""
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







"""
