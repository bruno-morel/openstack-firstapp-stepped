from shade import *


simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')


servers = conn.list_servers()
for server in servers:
    print( '--> Deleting server with ID :' + server[ "id"] )
    secgroups = conn.get_openstack_vars(server)['security_groups']
    for secgroup in secgroups:
        conn.delete_security_group(sec_group_name)
    conn.delete_server( server[ "id" ], wait=True )

print( 'Done! Congrats!')