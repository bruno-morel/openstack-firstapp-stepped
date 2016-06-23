#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';//'php-opencloud/openstack/src/OpenStack.php';

use Symfony\Component\Yaml\Yaml;

try { $configs = Yaml::parse(file_get_contents('clouds.yaml')); }
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
echo 'Selected flavor : ';
$nova = $openstack->computeV2();
$flavor_id = 'A1.1';
$flavor = $nova->getFlavor( [ 'id' => $flavor_id ] );
print_r( $flavor );
echo "\n";

echo 'Selected image : ';
$glance = $openstack->imagesV2();
$image_id = '3c76334f-9644-4666-ac3c-fa090f175655';
$image = $glance->getImage( $image_id );
print_r( $image );
echo "\n";
