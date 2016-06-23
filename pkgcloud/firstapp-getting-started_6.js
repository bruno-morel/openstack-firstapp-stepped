var pkgcloud = require('pkgcloud');

var client = pkgcloud.compute.createClient({
    provider:     'YOURPROVIERNAME',
    username:     'APILOGIN',
    password:     'APIPASS',
    authUrl:      'https://identity.api.cloud.iweb.com/',
    region:       'nyj01'
});

var winston = require('winston');

// setup a simple console winston logger
var logger = new winston.Logger({
    levels: {
        debug: 0,
        verbose: 1,
        info: 3,
        warn: 4,
        error: 5
    },
    colors: {
        debug: 'grey',
        verbose: 'cyan',
        info: 'green',
        warn: 'yellow',
        error: 'red'
    },
    transports: [
        new winston.transports.Console({
            level: 'debug',
            prettyPrint: true,
            colorize: true
        })
    ]
});

client.on('log::*', function (message, object) {
    if (object) {
        logger.log(this.event.split('::')[1], message, object);
    }
    else {
        logger.log(this.event.split('::')[1], message);
    }
    console.dir( message );
    console.dir( object );
});

client.getImages(function (err, images)
{
    if (err) {
        console.dir(err);
        return;
    }

    // Pick an image based on Ubuntu 14.04
    var image = null;
    for( var currentImageIndex = 0, len = images.length; currentImageIndex  < len; currentImageIndex++ )
    {
        if( images[ currentImageIndex  ].id != null &&
            images[ currentImageIndex  ].id == '3c76334f-9644-4666-ac3c-fa090f175655' )
            image = images[ currentImageIndex  ];
    }

    client.getFlavors(function (err, flavors)
    {
        if (err) {
            console.dir(err);
            return;
        }

        // Pick the smallest instance flavor
        var flavor = null;
        for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ )
        {
            if( flavors[ currentFlavorIndex ].id != null &&
                flavors[ currentFlavorIndex ].id == 'A1.1' )
                flavor = flavors[ currentFlavorIndex ];
        }

        client.getNetworks(function (err, networks)
        {
            if( err ) {
                console.dir(err);
                return;
            }

            var netWAN = null;
            for( var currentNetworkIndex = 0, len = networks.length; currentNetworkIndex < len; currentNetworkIndex++ )
            {
                if( networks[ currentNetworkIndex   ].label != null &&
                    networks[ currentNetworkIndex   ].label.indexOf( 'WAN' ) )
                    netWAN = networks[ currentNetworkIndex   ];
            }

            console.log( "\nCreating Server with parameters : " );
            console.log( "\t flavor - " + flavor.name );
            console.log( "\t image - " + image.name );
            console.log( "\t network - " + netWAN.label + ' with UUID ' + netWAN.id );

            // Create our first server
            client.createServer({ name: 'MyFirstVM', image: image, flavor: flavor, networks: [{uuid:netWAN.id.toString()}] },
                function( err, server) {
                    if( err ) { console.dir( err ); return; }
                    console.dir( server );
                    server.setWait({ status: server.STATUS.running }, 5000, function (err) {
                        if( err ) { console.dir(err); return; }
                        console.log('SERVER ' + server.name + ' IS ACTIVE!' );
                    });
                });
        });
    });
});

// This function will handle our server creation,
// as well as waiting for the server to come online after we've
// created it.
function handleServerResponse(err, server) {
    if (err) {
        console.dir(err);
        return;
    }

    provider, err := openstack.AuthenticatedClient(gophercloud.AuthOptions{
                                                   IdentityEndpoint: 	"https://identity.api.cloud.iweb.com/",
                                                   Username: 			"api-5707f1d445043",
                                                   Password: 			"72cd86201eec2de59678c19cc59ae833",
                                                   TenantName: 		"inap-18009",
                                                   })
    if err != nil {
        fmt.Println(err)
        return
    }

    console.log('SERVER CREATED: ' + server.name + ', waiting for active status');

    // Wait for status: RUNNING on our server, and then callback
    server.setWait({ status: server.STATUS.running }, 5000, function (err) {
        if (err) {
            console.dir(err);
            return;
        }

        console.log('SERVER INFO');
        console.log(server.name);
        console.log(server.status);
        console.log(server.id);

        console.log('Make sure you DELETE server: ' + server.id + ' in order to not accrue billing charges');
    });
}
