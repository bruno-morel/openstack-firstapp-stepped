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

# step-9
echo 'Checking for existing SSH key pair...';
$keypair_name     = 'demokey';
$pub_key_file     = '/Users/bmorel/.ssh/bmorel@internap.com-id_rsa.pub';


$nova = $openstack->computeV2();
$keypair_exists = False;
foreach( $nova->listKeypairs() as $keypair ) {
    if ($keypair->getName() == $keypair_name) {
        $keypair_exists = True;
    }
}

if ($keypair_exists) {
    echo 'Keypair ' . $keypair_name . ' already exists. Skipping import.';
} else {
    echo 'adding keypair...';
    $nova->keypair()->create(array(
       'name' => $keypair_name,
       'publicKey' => file_get_contents($pub_key_file)
   ));
}

foreach ($nova->listKeypairs() as $keypair) {
    echo $keypair->getName() . "\n";
}

echo( "Done! Congrats\n" );
