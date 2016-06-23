from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


keypair_name                    = 'demokey'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
appcontroller_name              = 'app-controller'
appworker_name                  = 'app-worker'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internap', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

print('Checking for WAN network...')
nets = conn.ex_list_networks()
for net in nets:
    if "WAN" in net.name:
        finalnet = net

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
                                    networks=[finalnet],
                                    ex_keyname=keypair_name,
                                    ex_userdata=userdata,
                                    ex_security_groups=[controller_group])
conn.wait_until_running([instance_controller_1])
print( instance_controller_1 )

instance_exists = False
for instance in conn.list_nodes():
    if instance.name == appcontroller_name:
        instance_controller_1 = instance
        instance_exists = True

private_ip = None
if len(instance_controller_1.public_ips):
    public_ip = instance_controller_1.public_ips[0]
    print('The Fractals app controller will be deployed to http://{}'.format(public_ip))
else:
    print('No fractals app controller deployed')

print( 'Done! Congrats!')
