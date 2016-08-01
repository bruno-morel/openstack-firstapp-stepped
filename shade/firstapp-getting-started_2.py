from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

print( 'Listing images' )
images = conn.list_images()
for image in images:
	print( '--> image details :'+ image["name"] + ' - ID : ' + image["id"] )

print( 'Done! Congrats' )
