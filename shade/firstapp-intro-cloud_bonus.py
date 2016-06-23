from shade import *

flavor_id 						= 'A1.1'
image_id 						= '3c76334f-9644-4666-ac3c-fa090f175655'
keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

servers = conn.list_servers()
for server in servers:
    if appcontroller_name in server[ "name" ] or appworker_name in server[ "name" ]:
        print( '--> Deleting server :' + server[ "name"] )
        conn.delete_server( server[ "id" ] )

networks = conn.list_networks()
for network in networks:
    if "WAN" in network["name"]:
        netWAN = network
        netWAN_id = network["id"]
    if "LAN" in network["name"]:
        netLAN = network
        netLAN_id = network["id"]


worker_group = conn.search_security_groups(worker_security_group_name)
if worker_group:
    conn.delete_security_group(worker_security_group_name)

print('Creating security group for ' + worker_security_group_name)
worker_group = conn.create_security_group(worker_security_group_name, 'for services that run on a worker node')
conn.create_security_group_rule(worker_group['name'], 22, 22, 'TCP')


controller_group = conn.search_security_groups(controller_security_group_name)
if worker_group:
    conn.delete_security_group(controller_security_group_name)

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
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[controller_group['name']],
    userdata=userdata,
    nics=[{"id":netWAN_id,"id":netLAN_id}])
print( instance_controller_1 )

if controller_instance.public_v4:
    controller_ip = controller_instance.public_v4
else:
    controller_ip = controller_instance.public_v6

if len(controller_ip):
    print('The Fractals app controller will be deployed to http://{}'.format(controller_ip))
else:
    print('No fractals app controller deployed')


userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
    ''' % {'ip_controller': controller_ip}

print( 'Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = conn.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=image_id,
    network=netLAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[worker_group['name']],
    userdata=userdata)
print( instance_worker_1 )

if len(instance_worker_1.public_v4):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v4))
elif len(instance_worker_1.public_v6):
    print('The worker will be available through SSH at {}'.format(instance_worker_1.public_v6))
else:
    print('No fractals app worker deployed')

print( 'Done! Congrats!')