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


# step-11
print('Creating security group for ' + worker_security_group_name)
worker_group = conn.create_security_group(worker_security_group_name, 'for services that run on a worker node')
conn.create_security_group_rule(worker_group['name'], 22, 22, 'TCP')

print('Creating security group for ' + controller_security_group_name)
controller_group = conn.create_security_group(controller_security_group_name, 'for services that run on a control node')
conn.create_security_group_rule(controller_group['name'], 22, 22, 'TCP')
conn.create_security_group_rule(controller_group['name'], 80, 80, 'TCP')
conn.create_security_group_rule(controller_group['name'], 5672, 5672, 'TCP', remote_group_id=worker_group['id'])

userdata = '''#!/usr/bin/env bash
curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i messaging -i faafo -r api
'''

print( 'Creating the instance ' + appcontroller_name + ' with userdata ' + userdata )
instance_controller_1 = conn.create_server(wait=True, auto_ip=False,
    name=appcontroller_name,
    image=image_id,
    network=netWAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[controller_group['name']],
    userdata=userdata)
print( instance_controller_1 )

if len(instance_controller_1.public_v4):
    print('The Fractals app will be deployed to http://{}'.format(instance_controller_1.public_v4))
elif len(instance_controller_1.public_v6):
    print('The Fractals app will be deployed to http://{}'.format(instance_controller_1.public_v6))
else:
    print('No fractals app controller deployed')

print( 'Done! Congrats!')
