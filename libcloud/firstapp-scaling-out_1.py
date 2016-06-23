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

# step-1
print( 'Destroying all test nodes')
for instance in conn.list_nodes():
    if instance.name in [appcontroller_name, appworker_name] :
        print(' -destroying Instance: %s' % instance.name)
        conn.destroy_node(instance)

print( 'Done! Congrats!')
