var pkgcloud = require('pkgcloud');
var yaml = require('yamljs');
var fs = require('fs');

var config = yaml.load( 'clouds.yaml' );
var openstack = pkgcloud.compute.createClient({
    provider:     "openstack",
    username:     config[ "clouds" ][ "internap" ][ "auth" ].username,
    password:     config[ "clouds" ][ "internap" ][ "auth" ].password,
    authUrl:      config[ "clouds" ][ "internap" ][ "authUrl" ],
    region:       config[ "clouds" ][ "internap" ][ "region_name" ]
});

var keypair_name      = 'demokey';
var pub_key_file      = '/Users/bmorel/.ssh/bmorel@internap.com-key.pub';
var pub_key           = fs.readFileSync( pub_key_file, 'utf8' );

console.log( 'Checking for existing keypairs...' );
openstack.getKey( keypair_name, function (err, keypair) {
    if (err) {
      console.log( ' ' + keypair_name + " keypair doesn't exists, creating it..." );
      openstack.addKey( { 'name' : keypair_name,
                          'public_key' : pub_key },
                        function (err, newKey){ if (err) { console.log(err); return; } });
      listingKeyPairs();
      return;
    }

    console.log( ' ' + keypair_name + " exists, skipping import..." );
    listingKeyPairs();
});


function listingKeyPairs( ) {
  console.log( 'Listing keypairs...' );
  openstack.listKeys( function (err, keypairs){
    if (err) { console.log(err); return; }

    var keypair = null;
    for( var currentKeyPairIndex = 0, len = keypairs.length; currentKeyPairIndex < len; currentKeyPairIndex++ ) {
      keypair = keypairs[ currentKeyPairIndex ][ 'keypair' ];
      console.log( " \t- key found with name : " + keypair.name + "\t and fingerprint : " + keypair.fingerprint );
    }
  });
}
