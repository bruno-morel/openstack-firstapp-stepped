from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

servers = conn.list_servers()
for server in servers:
	if "shade" in server[ "name" ]:
    	print( '--> Deleting server with ID :' + server[ "id"] )
		conn.delete_server( server[ "id" ] )

print( 'Done! Congrats.' )
