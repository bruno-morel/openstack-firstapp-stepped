from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config

cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internap', region_name='nyj01')

provider = get_driver(Provider.OPENSTACK)
conn = provider(cloud_config.config['auth']['username'],
                cloud_config.config['auth']['password'],
                ex_force_auth_url=cloud_config.config['auth']['auth_url'],
                ex_force_auth_version='2.0_password',
                ex_tenant_name=cloud_config.config['auth']['project_name'],
                ex_force_service_region=cloud_config.region)

print('Checking for unused Floating IP...')
unused_floating_ip = None
for floating_ip in conn.ex_list_floating_ips():
    if not floating_ip.node_id:
        unused_floating_ip = floating_ip
        break

# step-16
print('Attaching reserved Floating IP...')
if public_ip:
    print('Instance ' + testing_instance.name + ' already has a public ip. Skipping attachment.')
elif unused_floating_ip:
    conn.ex_attach_floating_ip_to_node(testing_instance, unused_floating_ip)

print( 'Done! Congrats!')
