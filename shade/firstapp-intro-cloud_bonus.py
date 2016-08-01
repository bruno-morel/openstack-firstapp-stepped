from shade import *

flavor_id 						= 'A1.1'
nyjimage_id 					= '3c76334f-9644-4666-ac3c-fa090f175655'
amsimage_id                     = 'b9ba51bb-1852-4759-b80e-e588f40784db'
keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


#simple_logging(debug=True)
connNYJ = openstack_cloud(cloud='internapNYJ')
connAMS = openstack_cloud(cloud='internapAMS')


networksNYJ = connNYJ.list_networks()
for network in networksNYJ:
    if "WAN" in network["name"]:
        netNYJWAN = network
        netNYJWAN_id = network["id"]
    if "LAN" in network["name"]:
        netNYJLAN = network
        netNYJLAN_id = network["id"]

networksAMS = connAMS.list_networks()
for network in networksAMS:
    if "WAN" in network["name"]:
        netAMSWAN = network
        netAMSWAN_id = network["id"]
    if "LAN" in network["name"]:
        netAMSLAN = network
        netAMSLAN_id = network["id"]


userdata = '''#!/usr/bin/env bash
curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i messaging -i faafo -r api
'''

print( 'Creating the instance ' + appcontroller_name + ' with userdata ' + userdata )
instance_controller_1 = connAMS.create_server(wait=True, auto_ip=False,
    name=appcontroller_name,
    image=amsimage_id,
    flavor=flavor_id,
    key_name=keypair_name,
    userdata=userdata,
    network=netAMSWAN_id)
print( instance_controller_1 )

if instance_controller_1.public_v4:
    controller_ip = instance_controller_1.public_v4
else:
    controller_ip = instance_controller_1.public_v6

if len(controller_ip):
    print('The Fractals app controller will be deployed to http://{}'.format(controller_ip))
else:
    print('No fractals app controller deployed')


userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
    ''' % {'ip_controller': controller_ip}

print( 'Creating the instance AMS ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = connAMS.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=amsimage_id,
    network=netAMSWAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    userdata=userdata)
print( instance_worker_1 )

if len(instance_worker_1.public_v4):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v4))
elif len(instance_worker_1.public_v6):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v6))
else:
    print('No fractals app worker deployed')

print( 'Creating the instance in NYJ ' + appworker_name + ' with userdata ' + userdata )
instance_worker_2 = connNYJ.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=nyjimage_id,
    network=netNYJWAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    userdata=userdata)
print( instance_worker_2 )

if len(instance_worker_2.public_v4):
    print('The worker will be available through SSH at {}'.format(instance_worker_2.public_v4))
elif len(instance_worker_2.public_v6):
    print('The worker will be available through SSH at {}'.format(instance_worker_2.public_v6))
else:
    print('No fractals app worker deployed')

print( 'Done! Congrats!')
