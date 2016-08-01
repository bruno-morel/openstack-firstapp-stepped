from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


instance_name                   = 'testing for libcloud #2 - step 2'
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

print( 'Destroying all active instances')
instances = conn.list_nodes()
for instance in instances:
    if "testing for libcloud" in instance.name:
        print(' -destroying Instance: %s' % instance.name)
        conn.destroy_node(instance)

print('Removing existing ' + security_group_name + ' security group...')
for security_group in conn.ex_list_security_groups():
    if security_group.name == security_group_name:
        conn.ex_delete_security_group(security_group)

print( 'Done! Congrats!')
