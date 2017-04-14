import boto
from boto.ec2.regioninfo import RegionInfo

#set the region
region=RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

#connect to nectar by using keys
#go nectar security - API - download ec2 credentials -ec2rc.sh - copy the keys
ec2_conn = boto.connect_ec2(aws_access_key_id='16a9a9a7d53441268ddbaaf8fc275030',
aws_secret_access_key='844cd078793546ce9fa97d05d21645af', is_secure=True, region=region, port=8773, path='/services/Cloud', validate_certs=False)

#List images
i=0
images = ec2_conn.get_all_images()
for img in images:
	print 'id: ', img.id, 'name: ', img.name
	i+=1
	if(i>4):
		break

#Launch image
#ec2_conn.run_instances(<ami_id>, key_name=<key_name>,
#instance_type=<instance_type>,

#Get reservations:
reservations = ec2_conn.get_all_reservations()

#Show reservation details:
for idx, res in enumerate(reservations):
	print idx, res.id, res.instances


#Show instance details:
print reservations[0].instances[0].ip_address
print reservations[0].instances[0].placement