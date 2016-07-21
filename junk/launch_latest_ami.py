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
#latestAmi=zz[0]




#http://boto3.readthedocs.io/en/latest/guide/migrationec2.html
#https://gist.github.com/iMilnb/0ff71b44026cfd7894f8
                # Let's use Amazon ec2
client = boto3.client('ec2')
#myimageId='ami-42870a55'
myimageId=latestAmi.id
mysubnetId='subnet-80cdeed8'
myinstanceType='c4.4xlarge'
mykeyName='spot-coursera'
mycount=1
myprice=5
mytype='one-time'
myipAddr='52.205.199.249'
myallocId='eipalloc-d22618e8'
mysecurityGroups=['WebServerSG']
mydisksize=70
mygroupId='sg-14356e6f'
#mygroupId='WebServerSG'
myzone='us-east-1a'
myvpcId='vpc-503dba37'
