from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

print( 'Listing images' )
images = conn.list_images()
for image in images:
	print( '--> image details :{}'.format(image))
    
print( 'Done! Congrats' )