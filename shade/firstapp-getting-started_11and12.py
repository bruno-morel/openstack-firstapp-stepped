from shade import *


simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')


flavor_id = 'A1.1'
image_id = '3c76334f-9644-4666-ac3c-fa090f175655'

networks = conn.list_networks()
for network in networks:
    if "WAN" in network["name"]:
        netWAN_id = network["id"]

keypair_name = 'demokey'
sec_group_name = 'all-in-one'

#step-11
ex_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

#step-12
instance_name = 'all-in-one'
testing_instance = conn.create_server(wait=True, auto_ip=False,
    name=instance_name,
    image=image_id,
    network=netWAN_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[sec_group_name],
    userdata=ex_userdata)

print( testing_instance )

print( 'Done! Congrats!')