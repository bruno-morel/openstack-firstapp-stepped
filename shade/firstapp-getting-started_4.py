from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')


image_id = 'f4bcad12-5668-44f7-9ceb-dfd9c00beee0'
image = conn.get_image(image_id)
print( 'Ubuntu image >> details :{}'.format(image))

flavor_id = 'A1.1'
flavor = conn.get_flavor(flavor_id)
print( 'Smallest flavor >> details :{}'.format(flavor))

print( 'Done! Congrats' )