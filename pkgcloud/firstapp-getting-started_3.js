var pkgcloud = require('pkgcloud');

var client = pkgcloud.compute.createClient({
    provider:     'YOURPROVIERNAME',
    username:     'APILOGIN',
    password:     'APIPASS',
    authUrl:      'https://identity.api.cloud.iweb.com/',
    region:       'nyj01'
});

client.getFlavors(function (err, flavors)
{
    if( err ) { console.dir(err); return; }
    console.dir( flavors );

    var flavor = null;
    for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ )
    {
        if( flavors[ currentFlavorIndex ].id != null &&
            flavors[ currentFlavorIndex ].id == 'A1.1' )
            flavor = flavors[ currentFlavorIndex ];
    }
});
