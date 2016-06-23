from shade import *


simple_logging(debug=True)
conn = openstack_cloud(cloud='internap')

#step-9
print('Checking for existing SSH keypair...')
keypair_name = 'demokey'
pub_key_file = '/Users/bmorel/.ssh/bmorel@internap.com-id_rsa.pub'

if conn.search_keypairs(keypair_name):
    print('Keypair already exists. Skipping import.')
else:
    print('Adding keypair...')
    conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

for keypair in conn.list_keypairs():
    print(keypair)

print( 'Done! Congrats!')
