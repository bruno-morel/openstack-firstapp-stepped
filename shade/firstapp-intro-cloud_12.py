from shade import *

flavor_id 						= 'A1.1'
image_id 						= '3c76334f-9644-4666-ac3c-fa090f175655'
keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

networks = conn.list_networks()
for network in networks:
    if "WAN" in network["name"]:
        netWAN_id = network["id"]

print('Checking for controller instance...')
for instance in conn.list_servers():
    if instance.name == appcontroller_name:
        controller_instance = instance

if controller_instance:
    if controller_instance.public_v4:
        controller_ip = controller_instance.public_v4
    else:
        controller_ip = controller_instance.public_v6

userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
    ''' % {'ip_controller': controller_ip}

print( 'Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = conn.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=image_id,
    network=netWAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[worker_security_group_name],
    userdata=userdata)
print( instance_worker_1 )

if len(instance_worker_1.public_v4):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v4))
elif len(instance_worker_1.public_v6):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v6))
else:
    print('No fractals app worker deployed')

print( 'Done! Congrats!')
