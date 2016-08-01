var pkgcloud = require('pkgcloud');
var yaml = require('yamljs');

var config = yaml.load( 'clouds.yaml' );
var openstack = pkgcloud.compute.createClient({
    provider:     "openstack",
    username:     config[ "clouds" ][ "internapNYJ" ][ "auth" ].username,
    password:     config[ "clouds" ][ "internapNYJ" ][ "auth" ].password,
    authUrl:      config[ "clouds" ][ "internapNYJ" ][ "authUrl" ],
    region:       config[ "clouds" ][ "internapNYJ" ][ "region_name" ]
});

console.log( JSON.stringify( openstack ) );
console.log( "Done! Congrats" );
