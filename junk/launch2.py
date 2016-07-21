#!/home/makayo/.virtualenvs/boto/bin/python

import boto.ec2.connection as conn

myimageId='ami-a80486bf'
mysubnetId='subnet-80cdeed8'
myinstanceType='c4.2xlarge'
mykeyName='spot-coursera'
mycount=1
myprice=5.0
mytype='one-time'
myipAddr='52.205.199.249'
myallocId='eipalloc-d22618e8'
#class boto.ec2.connection.EC2Connection


#conn = boto.ec2.connect_to_region("us-east-4")

xx=conn.EC2Connection();
resp=xx.request_spot_instances(price=myprice, image_id=myimageId, count=mycount, type=mytype ,key_name=mykeyName, instance_type=myinstanceType,subnet_id=mysubnetId )
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






