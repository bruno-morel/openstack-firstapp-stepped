#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';//'php-opencloud/openstack/src/OpenStack.php';

use Symfony\Component\Yaml\Yaml;

try {
  $configs = Yaml::parse(file_get_contents('clouds.yaml'));
} catch (ParseException $e) {
    printf("Unable to parse the YAML string: %s", $e->getMessage());
}

$paramConnection= [
    'authUrl' => $configs[ 'clouds' ][ 'internap' ][ 'authUrlV3'],
    'region'  => $configs[ 'clouds' ][ 'internap' ][ 'region_name' ],
    'user'    => [
        'id'       => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'username' ],
        'password' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'password' ]
    ],
    'scope'   => ['project' => ['id' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'project_name' ]]]
];

$client = new OpenStack\OpenStack($paramConnection);

$compute = $client->computeV2();
$options = [
    // Required
    'name'     => 'phpOpenCloud Test',
    'imageId'  => '',
    'flavorId' => '',

    // Optional
    'metadata' => ['foo' => 'bar'],
    'userData' => base64_encode('echo "Hello World. The time is now $(date -R)!" | tee /root/output.txt')
];

// Create the server
$server = $compute->createServer($options);
/*
# step-2
$images = $conn->imageList();
foreach ($images as $image) {
    echo $image->id . "\t" . $image->name . "\n";
}

# step-3
$flavors = $conn->flavorList();
foreach ($flavors as $flavor) {
    print_r(['id' => $flavor->id,
             'name' => $flavor->name,
             'ram' => $flavor->ram,
             'disk' => $flavor->disk,
             'vcpus' => $flavor->vcpus,
           ]);
}

# step-4
$image_id = '2cccbea0-cea9-4f86-a3ed-065c652adda5';
$image = $conn->image($image_id);

# step-5
$flavor_id = '2';
$flavor = $conn->flavor($flavor_id);

# step-6
$instance_name = 'testing';
$testing_instance = $conn->server();

$testing_instance->create(array(
 'name'   => $instance_name,
 'image'  => $image,
 'flavor' => $flavor
));

echo $testing_instance;

# step-7
$instances = $conn->serverList();
foreach ($instances as $instance) {
    echo $instance->name;
}

# step-8
$testing_instance->delete();

# step-9
echo 'Checking for existing SSH key pair...';
$keypair_name = 'demokey';
$pub_key_file = '/home/fifieldt/.ssh/id_rsa.pub';
$keypair_exists = False;
foreach ($conn->listKeypairs() as $keypair) {
    if ($keypair->getName() == $keypair_name) {
        $keypair_exists = True;
    }
}

if ($keypair_exists) {
    echo 'Keypair ' . $keypair_name . ' already exists. Skipping import.';
} else {
    echo 'adding keypair...';
    $conn->keypair()->create(array(
       'name' => $keypair_name,
       'publicKey' => file_get_contents($pub_key_file)
   ));
}

foreach ($conn->listKeypairs() as $keypair) {
    echo $keypair->getName() . "\n";
}

# step-10
echo 'Checking for existing security group...';
$security_group_name = 'all-in-one';
$security_group_exists = False;
/*
foreach ($conn->listSecurityGroups() as $security_group) {
    if (security_group->name == $security_group_name) {
        $all_in_one_security_group = security_group;
        $security_group_exists = True;
    }
}

if (security_group_exists) {
    echo 'Security Group ' . all_in_one_security_group.name . ' already exists. Skipping creation.'
} else {
    $all_in_one_security_group = $conn->createSecurityGroup(array(
        'name'        => security_group_name,
        'description' => 'network access for all-in-one application.'));
    $conn->createSecurityGroupRule(array(
       'securityGroupId' => $all_in_one_security_group->id,
       'protocol'        => 'tcp'
       'direction'       => 'ingress'
       'portRangeMin'    => 80,
       'porRangeMax'     => 80));
    $conn->createSecurityGroupRule(array(
       'securityGroupId' => $all_in_one_security_group->id,
       'protocol'        => 'tcp'
       'direction'       => 'ingress'
       'portRangeMin'    => 22,
       'porRangeMax'     => 22));
}

foreach ($conn->listSecurityGroups as $security_group) {
    echo $security_group;
}

# step-11
$userdata = "#!/usr/bin/env bash
curl -L -s https://git.openstack.org/cgit/stackforge/faafo/plain/contrib/install.sh | bash -s -- \
    -i faafo -i messaging -r api -r worker -r demo
"

# step-12
echo 'Checking for existing instance...'
$instance_name = 'all-in-one';
$instance_exists = False;
foreach ($conn->listServers() as $instance) {:
    if ($instance->name == instance_name) {
        $testing_instance = instance;
        $instance_exists = True;
    }
}

if (instance_exists) {
    echo 'Instance ' . $testing_instance->name . ' already exists. Skipping creation.';
} else {
$testing_instance = $conn->server();

$testing_instance->create(array(
 'name'    => $instance_name,
 'image'   => $image,
 'flavor'  => $flavor,
 'keyname' =>$ keypair_name,
userdata=userdata,
security_groups=[all_in_one_security_group])

));

$testing_instance->waitFor(ServerState::ACTIVE, 600);


foreach ($conn->ListServers() as instance) {
    echo instance;
}

# step-13
echo 'Checking for unused Floating IP...';
$ unused_floating_ip = False;
foreach ($conn->listFloatingIPs as $floating_ip) {
    if (not $floating_ip->id):
        $unused_floating_ip = floating_ip;
        break;
}

if (not $unused_floating_ip) {
    $pool = $conn->ex_list_floating_ip_pools()[0]
    echo 'Allocating new Floating IP from pool:' . pool
    $unused_floating_ip = $pool->createFloatingIp()
}

# step-14
if (strlen(testing_instance.public_ips) > 0) {
    echo 'Instance ' . $testing_instance->name . ' already has a public ip. Skipping attachment.';
} else {
    $conn->attachFloatingIp($testing_instance, $unused_floating_ip);
}

# step-15
echo 'The Fractals app will be deployed to http://' . $unused_floating_ip->ip_address;

*/
