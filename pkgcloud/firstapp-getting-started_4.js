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

openstack.getImages(function (err, images)
{
    if (err) { console.log(err); return; }

    // Pick an image based on Ubuntu 14.04
    var image = null;
    for( var currentImageIndex = 0, len = images.length; currentImageIndex  < len; currentImageIndex++ )
    {
        if( images[ currentImageIndex  ].id != null &&
            images[ currentImageIndex  ].id == '3c76334f-9644-4666-ac3c-fa090f175655' )
            image = images[ currentImageIndex  ];
    }
    console.log( 'Selected image : ' +  JSON.stringify( image ) );

    openstack.getFlavors(function (err, flavors)
    {
        if (err) { console.log(err); return; }

        // Pick the smallest instance flavor
        var flavor = null;
        for( var currentFlavorIndex = 0, len = flavors.length; currentFlavorIndex < len; currentFlavorIndex++ ) {
            if( flavors[ currentFlavorIndex ].id != null &&
                flavors[ currentFlavorIndex ].id == 'A1.1' )
                flavor = flavors[ currentFlavorIndex ];
        }
        console.log( 'Selected flavor : ' + JSON.stringify( flavor ) );
        console.log( "Done! Congrats" );
    });
});
