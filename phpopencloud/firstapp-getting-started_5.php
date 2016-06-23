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

#step4
echo( "Listing networks...\n" );
$neutron = $openstack->networkingV2();
foreach ($neutron->listNetworks() as $network) {
    echo $network->id . "\t" . $network->name;
    if( strpos( $network->name, "WAN" ) > -1 )
      echo ' ---> this is our WAN lan';

    echo "\n";
}

echo( "Done! Congrats\n" );
