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

# step-15
print('Checking for unused Floating IP...')
unused_floating_ip = None
for floating_ip in conn.ex_list_floating_ips():
    if not floating_ip.node_id:
        unused_floating_ip = floating_ip
        break

if not unused_floating_ip and len(conn.ex_list_floating_ip_pools()):
    pool = conn.ex_list_floating_ip_pools()[0]
    print(' allocating new Floating IP from pool: {}'.format(pool))
    unused_floating_ip = pool.create_floating_ip()

print( 'Done! Congrats!')
