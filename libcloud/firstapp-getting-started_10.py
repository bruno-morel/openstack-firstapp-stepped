#! /usr/bin/env bash

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


security_group_name             = 'all-in-one'
security_group_description      = 'network access for all-in-one application.'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internapNYJ', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

# step-10
print('Checking for existing security group...')
security_group_exists = False
for security_group in conn.ex_list_security_groups():
    if security_group.name == security_group_name:
        all_in_one_security_group = security_group
        security_group_exists = True

if security_group_exists:
    print(' security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
else:
    print(' creating security group ' + security_group_name)
    all_in_one_security_group = conn.ex_create_security_group(security_group_name, security_group_description)
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)

print( 'Listing all security groups')
for security_group in conn.ex_list_security_groups():
    print(security_group)

print( 'Done! Congrats!')
