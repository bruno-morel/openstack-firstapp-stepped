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
appservices_name                = 'app-services'
appapis_name                    = 'app-api'


cloud_config = os_client_config.OpenStackConfig().get_one_cloud(
    'internap', region_name='nyj01')

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
        finalnet = net

image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

flavor_id = 'A1.1'
flavor = conn.ex_get_size(flavor_id)

# step-3
def get_security_group(connexion, security_group_name):
    '''A helper function to find security groups'''
    security_group_exists = False
    for security_group in connexion.ex_list_security_groups():
        if security_group.name == security_group_name:
            found_security_group = security_group
            security_group_exists = True
    if security_group_exists:
        return found_security_group
    else:
        print('ERROR : didn t find security group named :' + security_group_name)
        return Null


# step-4
print( 'Looking for security group ' + services_security_group_name)
instance_security_group = get_security_group(conn,services_security_group_name)
userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i database -i messaging
    '''

print( 'Creating the instance ' + appservices_name + ' with userdata ' + userdata )
instance_services = conn.create_node(name=appservices_name,
                                     image=image,
                                     size=flavor,
                                     networks=[finalnet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[instance_security_group])
instance_services = conn.wait_until_running([instance_services])[0][0]
services_ip = instance_services.public_ips[0]
print( services_ip )


# step-5
print( 'Looking for security group ' + api_security_group_name)
instance_security_group = get_security_group(conn,api_security_group_name)
userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i faafo -r api -m 'amqp://guest:guest@%(services_ip)s:5672/' \
    -d 'mysql+pymysql://faafo:password@%(services_ip)s:3306/faafo'
    ''' % { 'services_ip': services_ip }

instancename = appapis_name + '-1'
print( 'Creating the instance ' + instancename + ' with userdata ' + userdata )
instance_api_1 = conn.create_node(name=instancename,
                                  image=image,
                                  size=flavor,
                                  networks=[finalnet],
                                  ex_keyname=keypair_name,
                                  ex_userdata=userdata,
                                  ex_security_groups=[instance_security_group])

instancename = appapis_name + '-2'
print( 'Creating the instance ' + instancename + ' with userdata ' + userdata )
instance_api_2 = conn.create_node(name=instancename,
                                  image=image,
                                  size=flavor,
                                  networks=[finalnet],
                                  ex_keyname=keypair_name,
                                  ex_userdata=userdata,
                                  ex_security_groups=[instance_security_group])

instance_api_1 = conn.wait_until_running([instance_api_1])[0][0]
api_1_ip = instance_api_1.public_ips[0]
instance_api_2 = conn.wait_until_running([instance_api_2])[0][0]
api_2_ip = instance_api_2.public_ips[0]


# step-6
print( 'Looking for security group ' + worker_security_group_name)
instance_security_group = get_security_group(conn,worker_security_group_name)
userdata = '''#!/usr/bin/env bash
    curl -L -s http://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
    -i faafo -r worker -e 'http://%(api_1_ip)s' -m 'amqp://guest:guest@%(services_ip)s:5672/'
    ''' % {'api_1_ip': api_1_ip, 'services_ip': services_ip}

instancename = appworker_name + '-1'
print( 'Creating the instance ' + instancename + ' with userdata ' + userdata )
instance_worker_1 = conn.create_node(name=instancename,
                                     image=image,
                                     size=flavor,
                                     networks=[finalnet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[instance_security_group])

instancename = appworker_name + '-2'
print( 'Creating the instance ' + instancename + ' with userdata ' + userdata )
instance_worker_2 = conn.create_node(name=instancename,
                                     image=image,
                                     size=flavor,
                                     networks=[finalnet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[instance_security_group])

instancename = appworker_name + '-3'
print( 'Creating the instance ' + instancename + ' with userdata ' + userdata )
instance_worker_3 = conn.create_node(name=instancename,
                                     image=image,
                                     size=flavor,
                                     networks=[finalnet],
                                     ex_keyname=keypair_name,
                                     ex_userdata=userdata,
                                     ex_security_groups=[instance_security_group])


print( 'Done! Congrats!')
