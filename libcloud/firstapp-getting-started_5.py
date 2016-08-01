#! /usr/bin/env bash

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config

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
        print(net + '\t <-----this is our WAN LAN')
    else:
        print(net)

print( 'Done! Congrats!')
