from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config

instance_name                   = 'testing for libcloud'
keypair_name                    = 'demokey'
security_group_name             = 'all-in-one'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internapNYJ', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

# step-4
image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

# step-5
flavor_id = 'A1.1'
flavor = conn.ex_get_size(flavor_id)

print('Checking for WAN network...')
nets = conn.ex_list_networks()
for net in nets:
    if "WAN" in net.name:
        finalnet = net


print('Checking for existing security group...')
security_group_exists = False
for security_group in conn.ex_list_security_groups():
    if security_group.name == security_group_name:
        all_in_one_security_group = security_group
        security_group_exists = True

# step-11
userdata = '''#!/bin/bash
    curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -i messaging -r api -r worker -r demo'''

# step-12
print('Checking for existing instance...')
instance_exists = False
for instance in conn.list_nodes():
    if instance.name == instance_name:
        testing_instance = instance
        instance_exists = True


if instance_exists:
    print(' instance ' + testing_instance.name + ' already exists. Skipping creation.')
else:
    print(' creating instance ' + instance_name)
    testing_instance = conn.create_node(name=instance_name,
                                        image=image,
                                        size=flavor,
                                        networks=[finalnet],
                                        ex_keyname=keypair_name,
                                        ex_userdata=userdata,
                                        ex_security_groups=[all_in_one_security_group])
    conn.wait_until_running([testing_instance])


print( 'List all active instance')
for instance in conn.list_nodes():
    print(instance)

print( 'Done! Congrats!')
