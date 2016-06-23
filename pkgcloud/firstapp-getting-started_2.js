var pkgcloud = require('pkgcloud');

var client = pkgcloud.compute.createClient({
    provider:     'YOURPROVIERNAME',
    username:     'APILOGIN',
    password:     'APIPASS',
    authUrl:      'https://identity.api.cloud.iweb.com/',
    region:       'nyj01'
});

client.getImages(function (err, images)
{
    if( err ) { console.dir(err); return; }
    console.dir( images );

    var image = null;
    for( var currentImageIndex = 0, len = images.length; currentImageIndex  < len; currentImageIndex++ )
    {
        if( images[ currentImageIndex  ].id != null &&
            images[ currentImageIndex  ].id == '3c76334f-9644-4666-ac3c-fa090f175655' )
            image = images[ currentImageIndex  ];
    }
});
