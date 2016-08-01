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


print('Checking for WAN network...')
nets = conn.ex_list_networks()
for net in nets:
    if "WAN" in net.name:
        finalnet = net

image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

flavor_id = 'A1.1'
flavor = conn.ex_get_size(flavor_id)

print('Checking for controller instance...')
controllerinstance_exists = False
for instance in conn.list_nodes():
    if instance.name == appcontroller_name:
        controller_instance = instance
        instance_exists = True

print('Retrieving controller instance IP...')
instance_exists = False
for instance in conn.list_nodes():
    if instance.name == appcontroller_name:
        instance_controller_1 = instance
        instance_exists = True

controller_ip = None
if len(instance_controller_1.public_ips):
    controller_ip = instance_controller_1.public_ips[0]
else:
    print('!!!!No controller IP found!!!!')

security_group_exists = False
for security_group in conn.ex_list_security_groups():
    if security_group.name == worker_security_group_name:
        worker_group = security_group
        security_group_exists = True

userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
    ''' % {'ip_controller': controller_ip}

print( 'Creating the instance ' + appworker_name + ' with userdata ' + userdata )
instance_worker_1 = conn.create_node(name=appworker_name,
                                     image=image,
                                     size=flavor,
                                     networks=[finalnet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[worker_group])
conn.wait_until_running([instance_worker_1])
print( instance_worker_1 )

instance_exists = False
for instance in conn.list_nodes():
    if instance.name == appworker_name:
        instance_worker_1 = instance
        instance_exists = True

if len(instance_worker_1.public_ips):
    public_ip = instance_worker_1.public_ips[0]
    print('The fractal worker will be available through SSH at {}'.format(public_ip))
else:
    print('No fractals app worker deployed')

print( 'Done! Congrats!')
