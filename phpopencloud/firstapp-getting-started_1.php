#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';

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
        'password' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'password' ],
        'domain'   => ['id' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'domain_id' ]]
    ],
    'scope'   => ['project' => ['id' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'project_name' ]]]
];

$client = new OpenStack\OpenStack($paramConnection);
print_r( $client );
$identity = $client->identityV3();


$token = $identity->generateToken([
    'user' => [
        'name'     => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'username' ],
        'password' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'password' ],
        'domain'   => [
            'id' => $configs[ 'clouds' ][ 'internap' ][ 'auth' ][ 'domain_id' ]
        ]
    ]
]);
print_r( $token );
