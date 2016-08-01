from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

print( 'Listing flavors' )
flavors =  conn.list_flavors()
for flavor in flavors:
	print( '--> flavor details : '+ flavor["name"] + ' - ID : ' + flavor["id"] )

print( 'Done! Congrats' )
