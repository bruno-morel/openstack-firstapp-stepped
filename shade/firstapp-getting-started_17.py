from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

instance_name = 'all-in-one'

print('Checking for existing instance...')
instance_exists = False
for instance in conn.list_servers():
    if instance.name == instance_name:
        testing_instance = instance
        instance_exists = True

if instance_exists:
    print( testing_instance )
else:
    print( 'No instance found' )

print('Checking for Public IPs...')
public_ip = None
if len(testing_instance.public_v4):
    public_ip = testing_instance.public_v4
elif len(testing_instance.public_v6):
    public_ip = testing_instance.public_v6
else:
    print(' no Public IP found')

print('The Fractals app is deployed to http://{}'.format(public_ip))

print( 'Done! Congrats!')
