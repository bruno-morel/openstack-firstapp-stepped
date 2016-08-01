#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';//'php-opencloud/openstack/src/OpenStack.php';

use Symfony\Component\Yaml\Yaml;

try { $configs = Yaml::parse(file_get_contents('clouds.yaml')); }
catch (ParseException $e) { printf("Unable to parse the YAML string: %s", $e->getMessage()); }

$openstack = new OpenStack\OpenStack([
    'authUrl' => $configs[ 'clouds' ][ 'internapNYJ' ][ 'authUrlV3'],
    'region'  => $configs[ 'clouds' ][ 'internapNYJ' ][ 'region_name' ],
    'user'    => [
        'name'      => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'username' ],
        'password'  => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'password' ],
        'domain'    => [
            'name'    => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'domain_name' ]
        ]
    ]
]);

# step-2
echo( "Listing images...\n" );
$glance = $openstack->imagesV2();
foreach ($glance->listImages() as $image) {
    echo $image->id . "\t" . $image->name . "\n";
}

echo( "Done! Congrats\n" );
