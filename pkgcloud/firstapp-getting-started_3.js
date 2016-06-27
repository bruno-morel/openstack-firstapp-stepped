var pkgcloud = require('pkgcloud');
var yaml = require('yamljs');

var config = yaml.load( 'clouds.yaml' );
var openstack = pkgcloud.compute.createClient({
    provider:     "openstack",
    username:     config[ "clouds" ][ "internap" ][ "auth" ].username,
    password:     config[ "clouds" ][ "internap" ][ "auth" ].password,
    authUrl:      config[ "clouds" ][ "internap" ][ "authUrl" ],
    region:       config[ "clouds" ][ "internap" ][ "region_name" ]
});

openstack.getFlavors(function (err, flavors)
{
    if( err ) { console.log(err); return; }

    console.log( "Listing flavors..." );
    var flavor = null;
    for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ )
    {
        flavor = flavors[ currentFlavorIndex ];
        if( flavor.id != null &&
            flavor.id == 'A1.1' )
          console.log( flavor.id + '     ' + flavor.name + ' <------- this is our flavor' );
        else
          console.log( flavor.id + '     ' + flavor.name );
    }
    console.log( "Done! Congrats" );
});
