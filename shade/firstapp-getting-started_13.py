from shade import *



simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

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

# step-13
print('Checking for Private IPs...')
if len(testing_instance.private_v4):
    print(' private IPV4 found: {}'.format(testing_instance.private_v4))
elif len(testing_instance.private_v6):
    print(' private IPV4 found: {}'.format(testing_instance.private_v6))
else:
    print(' no Private IP found')

print( 'Done! Congrats!')