from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os_client_config


keypair_name                    = 'demokey'
services_security_group_name    = 'services'
controller_security_group_name  = 'controller'
worker_security_group_name      = 'worker'
api_security_group_name         = 'api'
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

# step-2
print( 'Creating new security groups')
print( '    - creating : ' + api_security_group_name)
api_group = conn.ex_create_security_group(api_security_group_name, 'for API services only')
conn.ex_create_security_group_rule(api_group, 'TCP', 80, 80)
conn.ex_create_security_group_rule(api_group, 'TCP', 22, 22)

print( '    - creating : ' + worker_security_group_name)
worker_group = conn.ex_create_security_group(worker_security_group_name, 'for services that run on a worker node')
conn.ex_create_security_group_rule(worker_group, 'TCP', 22, 22)

print( '    - creating : ' + controller_security_group_name)
controller_group = conn.ex_create_security_group(controller_security_group_name, 'for services that run on a control node')
conn.ex_create_security_group_rule(controller_group, 'TCP', 22, 22)
conn.ex_create_security_group_rule(controller_group, 'TCP', 80, 80)
conn.ex_create_security_group_rule(controller_group, 'TCP', 5672, 5672, source_security_group=worker_group)

print( '    - creating : ' + services_security_group_name)
services_group = conn.ex_create_security_group(services_security_group_name, 'for DB and AMQP services only')
conn.ex_create_security_group_rule(services_group, 'TCP', 22, 22)
conn.ex_create_security_group_rule(services_group, 'TCP', 3306, 3306, source_security_group=api_group)
conn.ex_create_security_group_rule(services_group, 'TCP', 5672, 5672, source_security_group=worker_group)
conn.ex_create_security_group_rule(services_group, 'TCP', 5672, 5672, source_security_group=api_group)

print( 'Done! Congrats!')
