from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

print( 'Listing flavors' )
flavors =  conn.list_flavors()
for flavor in flavors:
	print( '--> flavor details :{}'.format(flavor))

print( 'Done! Congrats' )