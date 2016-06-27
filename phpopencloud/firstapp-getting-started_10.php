#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';//'php-opencloud/openstack/src/OpenStack.php';

use Symfony\Component\Yaml\Yaml;

try {  $configs = Yaml::parse(file_get_contents('clouds.yaml'));}
catch (ParseException $e) { printf("Unable to parse the YAML string: %s", $e->getMessage()); }

$openstack = new OpenStack\OpenStack([
    'authUrl' => $configs[ 'clouds' ][ 'internap' ][ 'authUrlV3'],
    'region'  => $configs[ 'clouds' ][ 'internap' ][ 'region_name' ],
    'user'    => [
        'name'      => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'username' ],
        'password'  => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'password' ],
        'domain'    => [
            'name'    => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'domain_name' ]
        ]
    ]
]);

$security_group_name        = 'all-in-one';
$security_group_description = 'network access for all-in-one application.';

# step-9

$neutron = $openstack->networkingV2ExtSecGroups();

$security_group_exists = False;
echo 'Checking for existing security group named ' . $security_group_name . "...\n";
foreach ($neutron->listSecurityGroups() as $secGroup) {
  if ($secGroup->name == $security_group_name)
      $security_group_exists = True;
}

if ($security_group_exists) {
    echo " \tsecurity group " . $security_group_name . " already exists, skipping creation.\n";
} else {
    echo " \tadding security group...";
    $secGroup = $neutron->createSecurityGroup([
        'name'        => $security_group_name,
        'description' => $security_group_description,
    ]);
}

echo( "Listing security groups...\n" );
foreach ($neutron->listSecurityGroups() as $secGroup) {
    echo ' - found security group with ID ' . $secGroup->id . ' and name ' .  $secGroup->name . "\n";
}

echo( "Done! Congrats\n" );
