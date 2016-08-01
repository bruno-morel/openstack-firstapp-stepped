from shade import *

flavor_id 						= 'A1.1'
nyjimage_id 					= '3c76334f-9644-4666-ac3c-fa090f175655'
amsimage_id                     = 'b9ba51bb-1852-4759-b80e-e588f40784db'
keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


simple_logging(debug=True)
connNYJ = openstack_cloud(cloud='internapNYJ')
connAMS = openstack_cloud(cloud='internapAMS')


print( 'NYJ - Listing networks' )
networksNYJ = connNYJ.list_networks()
for network in networksNYJ:
    if "WAN" in network["name"]:
        netNYJWAN = network
        netNYJWAN_id = netNYJWAN["id"]
        print( '  --> found WAN network : ' + netNYJWAN["name"] + ' - with ID : ' + netNYJWAN_id)
        subnet = connNYJ.get_subnet(netNYJWAN["subnets"][0])
        cidrNYJWAN = subnet["cidr"]
        print( '       -> found subnet : ' + cidrNYJWAN )
    if "LAN" in network["name"]:
        netNYJLAN = network
        netNYJLAN_id = netNYJLAN["id"]
        print( '  --> found LAN network : ' + netNYJLAN["name"] + ' - with ID : ' + netNYJLAN_id)
        subnet = connNYJ.get_subnet(netNYJLAN["subnets"][0])
        cidrNYJLAN = subnet["cidr"]
        print( '       -> found subnet : ' + cidrNYJLAN )

print( 'AMS - Listing networks' )
networksAMS = connAMS.list_networks()
for network in networksAMS:
    if "WAN" in network["name"]:
        netAMSWAN = network
        netAMSWAN_id = netAMSWAN["id"]
        print( '  --> found WAN network : ' + netAMSWAN["name"] + ' - with ID : ' + netAMSWAN_id)
        subnet = connAMS.get_subnet(netAMSWAN["subnets"][0])
        cidrAMSWAN = subnet["cidr"]
        print( '       -> found subnet : ' + cidrAMSWAN )
    if "LAN" in network["name"]:
        netAMSLAN = network
        netAMSLAN_id = netAMSLAN["id"]
        print( '  --> found LAN network : ' + netAMSLAN["name"] + ' - with ID : ' + netAMSLAN_id)
        subnet = connAMS.get_subnet(netAMSLAN["subnets"][0])
        cidrNYJLAN = subnet["cidr"]
        print( '       -> found subnet : ' + cidrNYJLAN )

print('AMS - Creating security group for ' + worker_security_group_name)
ams_worker_sgroup = connAMS.create_security_group(worker_security_group_name, 'for services that run on a worker node')
connAMS.create_security_group_rule(ams_worker_sgroup['name'], 22, 22, 'TCP')

print('AMS - Creating security group for ' + controller_security_group_name)
controller_sgroup = connAMS.create_security_group(controller_security_group_name, 'for services that run on a control node')
connAMS.create_security_group_rule(controller_sgroup['name'], 22, 22, 'TCP')
connAMS.create_security_group_rule(controller_sgroup['name'], 80, 80, 'TCP')
connAMS.create_security_group_rule(controller_sgroup['name'], 5672, 5672, 'TCP', remote_group_id=ams_worker_sgroup['id'])
connAMS.create_security_group_rule(controller_sgroup['name'], 5672, 5672, 'TCP', remote_ip_prefix=cidrNYJWAN)

print('NYJ - Creating security group for ' + worker_security_group_name)
nyj_worker_sgroup = connNYJ.create_security_group(worker_security_group_name, 'for services that run on a worker node')
connNYJ.create_security_group_rule(nyj_worker_sgroup['name'], 22, 22, 'TCP')


userdata = '''#!/usr/bin/env bash
curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i messaging -i faafo -r api
'''

print( 'AMS - Creating the instance ' + appcontroller_name + ' with userdata ' + userdata )
instance_controller_1 = connAMS.create_server(wait=True, auto_ip=False,
    name=appcontroller_name,
    image=amsimage_id,
    flavor=flavor_id,
    network=netAMSWAN_id,
    key_name=keypair_name,
    userdata=userdata,
    security_groups=[controller_security_group_name])
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

print( 'AMS - Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = connAMS.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=amsimage_id,
    flavor=flavor_id,
    nics=[{"net-id":netAMSWAN_id},{"net-id":netAMSLAN_id}],
    key_name=keypair_name,
    userdata=userdata,
    security_groups=[worker_security_group_name])
print( instance_worker_1 )

if len(instance_worker_1.public_v4):
    ip_instance_worker_1 = instance_worker_1.public_v4
elif len(instance_worker_2.public_v6):
    ip_instance_worker_1 = instance_worker_1.public_v6

if len(ip_instance_worker_1 ):
    print('The worker will be available through SSH at ' + ip_instance_worker_1)
else:
    print('No fractals app worker deployed')


print( 'NYJ - Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_2 = connNYJ.create_server(wait=True, auto_ip=False,
    name=appworker_name,
    image=nyjimage_id,
    flavor=flavor_id,
    nics=[{"net-id":netNYJWAN_id},{"net-id":netNYJLAN_id}],
    key_name=keypair_name,
    userdata=userdata,
    security_groups=[worker_security_group_name])
print( instance_worker_2 )

if len(instance_worker_2.public_v4):
    ip_instance_worker_2 = instance_worker_2.public_v4
elif len(instance_worker_2.public_v6):
    ip_instance_worker_2 = instance_worker_2.public_v6

if len(ip_instance_worker_2 ):
    print('The worker will be available through SSH at ' + ip_instance_worker_2)
else:
    print('No fractals app worker deployed')


print( 'Done! Congrats!')
