#! /usr/bin/env bash

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


instance_name = 'test instance for libcloud'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internap', region_name='nyj01')

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

# step-6
print( 'Creating testing instance')
testing_instance = conn.create_node(name=instance_name, image=image, size=flavor, networks=[finalnet])
print(testing_instance)

print( 'Done! Congrats!')
