from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


instance_name                   = 'testing for libcloud'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internapNYJ', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

print('Checking for existing instance...')
instance_exists = False
for instance in conn.list_nodes():
    if instance.name == instance_name:
        testing_instance = instance
        instance_exists = True

# step-13
if testing_instance:
    print('Checking for Private IPs...')
    private_ip = None
    pprint( vars(testing_instance) )
    if len(testing_instance.private_ips):
        private_ip = testing_instance.private_ips[0]
        print(' private IP found: {}'.format(private_ip))
    else:
        print(' no Private IP found')

    print( 'Done! Congrats!')

else:
    print( 'No testing instance found')
