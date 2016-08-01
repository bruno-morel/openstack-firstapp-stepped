from shade import *


simple_logging(debug=True)
conn = openstack_cloud(cloud='internapNYJ')

#step-10
print('Checking for existing security groups...')
sec_group_name = 'all-in-one'
if conn.search_security_groups(sec_group_name):
    print('Security group already exists. Skipping creation.')
else:
    print('Creating security group.')
    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

secgroup = conn.search_security_groups(sec_group_name)
print( secgroup )

print( 'Done! Congrats!')
