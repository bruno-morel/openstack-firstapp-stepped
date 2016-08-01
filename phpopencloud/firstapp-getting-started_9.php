#! /usr/bin/env php
<?php

require_once __DIR__ . '/vendor/autoload.php';//'php-opencloud/openstack/src/OpenStack.php';

use Symfony\Component\Yaml\Yaml;

try {  $configs = Yaml::parse(file_get_contents('clouds.yaml'));}
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

# step-9
echo 'Checking for existing SSH key pair...';
$keypair_name     = 'demokey';
$pub_key_file     = '/Users/bmorel/.ssh/bmorel@internap.com-key.pub';


$nova = $openstack->computeV2();
$keypair_exists = False;
foreach( $nova->listKeypairs() as $keypair ) {
    if ($keypair->name == $keypair_name) {
        $keypair_exists = True;
    }
}

if ($keypair_exists) {
    echo " \tkeypair " . $keypair_name . " already exists. Skipping import.\n";
} else {
    echo " \tadding keypair...";
    $nova->createKeypair([
      'name'      => $keypair_name,
      'publicKey' => file_get_contents($pub_key_file)
    ]);
}

echo( "Listing keypairs...\n" );
foreach ($nova->listKeypairs() as $keypair) {
    echo $keypair->name . "\n";
}

echo( "Done! Congrats\n" );
