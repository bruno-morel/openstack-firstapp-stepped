var pkgcloud = require('pkgcloud');

var client = pkgcloud.compute.createClient({
    provider:     'YOURPROVIERNAME',
    username:     'APILOGIN',
    password:     'APIPASS',
    authUrl:      'https://identity.api.cloud.iweb.com/',
    region:       'nyj01'
});

client.getNetworks(function (err, networks) {
    if (err) { console.dir(err); return; }
    console.dir( networks );

    var netWAN = null;
    for( var currentNetworkIndex = 0, len = networks.length; currentNetworkIndex < len; currentNetworkIndex++ ) {
        if( networks[ currentNetworkIndex   ].label != null &&
            networks[ currentNetworkIndex   ].label.indexOf( 'WAN' ) )
            netWAN = networks[ currentNetworkIndex   ];
    }
});
