#! /usr/bin/env bash

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config

keypair_name                    = 'demokey'
pub_key_file                    = '/Users/bmorel/.ssh/bmorel@internap.com-key.pub'

cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internapNYJ', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

# step-9
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

print( 'Listing all keypairs...')
for keypair in conn.list_key_pairs():
    print(keypair)

print( 'Done! Congrats!')
