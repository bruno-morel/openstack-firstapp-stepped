from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


instance_name                   = 'testing for libcloud #2 - step 1'
keypair_name                    = 'demokey'
security_group_name             = 'all-in-one'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internap', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

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

if security_group_exists:
    print(' security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
else:
    print(' creating security group for all-in-one...')
    all_in_one_security_group = conn.ex_create_security_group(security_group_name, 'network access for all-in-one application.')
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)


# step-1
userdata = '''#!/usr/bin/env bash
    curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i faafo -i messaging -r api -r worker -r demo
    '''

print('Starting ' + instance_name + ' instance and waiting until it s ready...')
testing_instance = conn.create_node(name=instance_name,
                                    image=image,
                                    size=flavor,
                                    networks=[finalnet],
                                    ex_keyname=keypair_name,
                                    ex_userdata=userdata,
                                    ex_security_groups=[all_in_one_security_group])
conn.wait_until_running([testing_instance])

print( 'Done! Congrats!')
