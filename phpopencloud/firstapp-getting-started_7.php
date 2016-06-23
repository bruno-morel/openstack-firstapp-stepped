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
$flavor_id = 'A1.1';

$image_id = "3c76334f-9644-4666-ac3c-fa090f175655";

#step5
echo( "Listing networks...\n" );
$neutron = $openstack->networkingV2();
foreach ($neutron->listNetworks() as $network) {
    if( strpos( $network->name, "WAN" ) > -1 )
      $idPublicWan = $network->id;
}

$nova = $openstack->computeV2();
$instance = $nova->createServer([
    'name'     => 'second test for phpOpenCloud',
    'imageId'  => $image_id,
    'flavorId' => $flavor_id,
    'networks'  => [ 0 => [ 'uuid' => $idPublicWan ] ]
]);
print_r( $instance );

echo( "Listing servers \n" );
foreach ($nova->listServers() as $server) {
  echo $server->id . "\t" . $server->name . "\n";
}
echo( "Done! Congrats\n" );
