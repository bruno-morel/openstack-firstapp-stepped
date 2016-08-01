#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';

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
print_r( $openstack );
$keystone = $openstack->identityV3();
$token = $keystone->generateToken([
    'user' => [
        'name'     => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'username' ],
        'password' => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'password' ],
        'domain'   => [
            'name' => $configs[ 'clouds' ][ 'internapNYJ' ][ 'auth' ][ 'domain_name' ]
        ]
    ]
]);
print_r( $token );

echo( "Done! Congrats\n" );
