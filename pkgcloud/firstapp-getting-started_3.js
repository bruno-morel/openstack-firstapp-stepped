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

openstack.getFlavors(function (err, flavors)
{
    if( err ) { console.log(err); return; }

    console.log( "Listing flavors..." );
    var flavor = null;
    for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ ) {
        flavor = flavors[ currentFlavorIndex ];
        if( flavor.id != null &&
            flavor.id == 'A1.1' )
          console.log( flavor.id + " \t" + flavor.name + ' <------- this is our flavor' );
        else
          console.log( flavor.id + " \t" + flavor.name );
    }
    console.log( "Done! Congrats" );
});
