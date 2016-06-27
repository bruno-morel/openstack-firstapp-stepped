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

openstack.getImages(function (err, images)
{
    if( err ) { console.log(err); return; }

    // Pick an image based on Ubuntu 14.04
    var image = null;
    for( var currentImageIndex = 0, len = images.length; currentImageIndex  < len; currentImageIndex++ ) {
        if( images[ currentImageIndex  ].id != null &&
            images[ currentImageIndex  ].id == '3c76334f-9644-4666-ac3c-fa090f175655' )
            image = images[ currentImageIndex  ];
    }

    openstack.getFlavors(function (err, flavors) {
        if( err ) { console.log(err); return; }

        // Pick the smallest instance flavor
        var flavor = null;
        for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ ) {
            if( flavors[ currentFlavorIndex ].id != null &&
                flavors[ currentFlavorIndex ].id == 'A1.1' )
                flavor = flavors[ currentFlavorIndex ];
        }

        openstack.getNetworks(function (err, networks) {
            if( err ) { console.log(err); return; }

            var netWAN = null;
            for( var currentNetworkIndex = 0, len = networks.length; currentNetworkIndex < len; currentNetworkIndex++ ) {
                if( networks[ currentNetworkIndex   ].label != null &&
                    networks[ currentNetworkIndex   ].label.indexOf( 'WAN' ) > 0 )
                    netWAN = networks[ currentNetworkIndex   ];
            }

            console.log( "\nCreating Server with parameters : " );
            console.log( "\t flavor - " + flavor.name );
            console.log( "\t image - " + image.name );
            console.log( "\t network - " + netWAN.label + ' with UUID ' + netWAN.id );

            // Create our first server
            openstack.createServer({  name: 'test server for pkgcloud',
                                      image: image,
                                      flavor: flavor,
                                      networks: [{uuid:netWAN.id.toString()}] },
                                    handleServerCreation );
        });
    });
});

function handleServerCreation( err, server) {
    if( err ) { console.log( err ); return; }

    console.log( JSON.stringify( server ) );
    server.setWait({ status: server.STATUS.running }, 5000, function (err) {
        if( err ) { console.log(err); return; }

        console.log('SERVER ' + server.name + ' IS ACTIVE!' );
        openstack.getServer( server.id, function (err, server ){
            console.log( 'Server details : ' + JSON.stringify( server ));
            console.log( "Done! Congrats" );
        });
    });
}
