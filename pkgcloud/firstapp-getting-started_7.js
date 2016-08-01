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

openstack.getImage( '3c76334f-9644-4666-ac3c-fa090f175655', function (err, image) {
    if( err ) { console.log(err); return; }

    openstack.getFlavor( 'A1.1', function (err, flavor) {
        if( err ) { console.log(err); return; }

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
            openstack.createServer({  name: 'second test server for pkgcloud',
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
