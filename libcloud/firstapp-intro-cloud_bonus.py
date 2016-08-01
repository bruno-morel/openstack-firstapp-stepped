from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internapNYJ', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

print('Checking for existing SSH key pair...')
keypair_exists = False
for keypair in conn.list_key_pairs():
    if keypair.name == keypair_name:
        keypair_exists = True

if keypair_exists:
    print(' keypair ' + keypair_name + ' already exists. Skipping import.')
else:
    print(' adding keypair...')
    conn.import_key_pair_from_file(keypair_name, pub_key_file)

print('Checking for networks...')
nets = conn.ex_list_networks()
for net in nets:
    if "WAN" in net.name:
        publicnet = net
        print(' -found public network : {}'.format(publicnet))
    if "LAN" in net.name:
        privatenet = net
        print(' -found private network : {}'.format(privatenet))

image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

flavor_id = 'A1.1'
flavor = conn.ex_get_size(flavor_id)

# step-11
print('Creating security group for ' + worker_security_group_name)
worker_group = conn.ex_create_security_group(worker_security_group_name, 'for services that run on a worker node')
conn.ex_create_security_group_rule(worker_group, 'TCP', 22, 22)

print('Creating security group for ' + controller_security_group_name)
controller_group = conn.ex_create_security_group(controller_security_group_name, 'for services that run on a control node')
conn.ex_create_security_group_rule(controller_group, 'TCP', 22, 22)
conn.ex_create_security_group_rule(controller_group, 'TCP', 80, 80)
conn.ex_create_security_group_rule(controller_group, 'TCP', 5672, 5672, source_security_group=worker_group)


userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i messaging -i faafo -r api'''

print( 'Creating the instance ' + appcontroller_name + ' with userdata ' + userdata )
instance_controller_1 = conn.create_node(name=appcontroller_name,
                                         image=image,
                                         size=flavor,
                                         networks=[publicnet,privatenet],
                                         ex_keyname=keypair_name,
                                         ex_userdata=userdata,
                                         ex_security_groups=[controller_group])
instance_controller_1 = conn.wait_until_running([instance_controller_1])[0][0]
print( instance_controller_1 )
controller_private_ip = instance_controller_1.private_ips[0]
controller_public_ip = instance_controller_1.public_ips[0]

userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
    ''' % {'ip_controller': controller_private_ip}

print( 'Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = conn.create_node(name=appworker_name,
                                     image=image,
                                     size=flavor,
                                     networks=[privatenet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[worker_group])
instance_worker_1 = conn.wait_until_running([instance_worker_1])[0][0]
print( instance_worker_1 )
worker_ip = instance_worker_1.private_ips[0]

print('The worker will be available privately from the controller through SSH at {}'.format(worker_ip))
print('And the Fractals app will be deployed to http://{}'.format(controller_public_ip))
