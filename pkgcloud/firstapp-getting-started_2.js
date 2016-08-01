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
    if( err ) { console.log(err); return; }

    console.log( "Listing images..." );
    var image = null;
    for( var currentImageIndex = 0, len = images.length; currentImageIndex  < len; currentImageIndex++ ) {
      image = images[ currentImageIndex  ];
      if( image.id != null &&
          image.id == '3c76334f-9644-4666-ac3c-fa090f175655' )
        console.log( image.id + " \t" + image.name + ' <------- this is our image' );
      else
        console.log( image.id + " \t" + image.name );

    }
    console.log( "Done! Congrats" );
});
