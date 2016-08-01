from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')
print( 'Connection details :{} '.format(conn) )

print( 'Done! Congrats' )
