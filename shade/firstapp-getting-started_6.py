from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')


flavor_id = 'A1.1'
flavor = conn.get_flavor(flavor_id)

image_id = '3c76334f-9644-4666-ac3c-fa090f175655'
image = conn.get_image(image_id)

networks = conn.list_networks()
for network in networks:
    if "WAN" in network["name"]:
        netWAN_id = network["id"]

instance_name = 'test instance for shade'
testing_instance = conn.create_server(wait=True, auto_ip=True,
                                      name=instance_name,
                                      image=image_id,
                                      network=netWAN_id,
                                      flavor=flavor_id)
print(testing_instance)

print( 'Done! Congrats' )
