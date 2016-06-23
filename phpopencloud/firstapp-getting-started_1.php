#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';

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
print_r( $openstack );
$keystone = $openstack->identityV3();
$token = $keystone->generateToken([
    'user' => [
        'name'     => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'username' ],
        'password' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'password' ],
        'domain'   => [
            'name' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'domain_name' ]
        ]
    ]
]);
print_r( $token );

echo( "Done! Congrats\n" );
