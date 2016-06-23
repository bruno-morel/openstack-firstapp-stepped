from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

servers = conn.list_servers()
for server in servers:
	print( '--> Deleting server with ID :' + server[ "id"] )
	conn.delete_server( server[ "id" ] )

print( 'Done! Congrats.' )