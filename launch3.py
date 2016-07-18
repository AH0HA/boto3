#!/home/makayo/.virtualenvs/boto3/bin/python
import boto3


#http://boto3.readthedocs.io/en/latest/guide/migrationec2.html

#https://gist.github.com/iMilnb/0ff71b44026cfd7894f8

# Let's use Amazon ec2
#ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

myimageId='ami-42870a55'
mysubnetId='subnet-80cdeed8'
myinstanceType='c4.2xlarge'
mykeyName='spot-coursera'
mycount=1
myprice='5.0'
mytype='one-time'
myipAddr='52.205.199.249'
myallocId='eipalloc-d22618e8'
mysecurityGroups=['WebServerSG']
mygroupId='sg-14356e6f'
myzone='us-east-1a'
myvpcId='vpc-503dba37'
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
                                                #        'SecurityGroups': mysecurityGroups,
                                                                'InstanceType': myinstanceType,
                                                                        'Placement': {
                                                                                        'AvailabilityZone': myzone,
                                                                                                }
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


#for q in ec2.instances.all():
    #print(q.id);
    #print(type(q));
    #response = q.modify_attribute(Groups=[mygroupId]);

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type);
    response = instance.modify_attribute(Groups=[mygroupId]);
    print(response);
    #respnse = instance.modify_attribute(public_ip_address=myipAddr);
    #print(response);
    #response =

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

#resp=ec2.request_spot_instances(price=myprice, image_id=myimageId, count=mycount, type=mytype ,key_name=mykeyName, instance_type=myinstanceType,subnet_id=mysubnetId )

"""
#!/home/makayo/.virtualenvs/boto/bin/python

import boto.ec2.connection as conn

#class boto.ec2.connection.EC2Connection


#conn = boto.ec2.connect_to_region("us-east-4")

xx=conn.EC2Connection();
reservations = xx.get_all_instances()  # could limit results with filters
mystat = xx.get_all_instance_status()
latest=mystat[len(mystat)-1]
latestIns=str(latest).split(':')[1]

#cant get allocation id !!!
#addresses = xx.get_all_addresses()
#cant get allocation id !!!

#for addr in addresses:
    #print('%s - %s' % (addr.public_ip, addr.allocation_id)

xx.associate_address(instance_id=latestIns, public_ip=None,allocation_id=myallocId)

#to_do how to find allocation_id given an ip_address ??
#to_do how to associate a security group with an instance ??
"""



