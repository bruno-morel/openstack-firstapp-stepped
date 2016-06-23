from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

networks = conn.list_networks()
for network in networks:
    if "WAN" in network["name"]:
        finalnet = network

print( 'last WAN network >> details :{}'.format(finalnet))

print( 'Done! Congrats' )