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

openstack.getNetworks(function (err, networks) {
    if (err) { console.log(err); return; }

    console.log( "Listing networks..." );
    var network = null;
    for( var currentNetworkIndex = 0, len = networks.length; currentNetworkIndex < len; currentNetworkIndex++ ) {
      network = networks[ currentNetworkIndex ];
      if( network.label != null &&
          network.label.indexOf( 'WAN' ) > 0 )
          console.log( network.id + '     ' + network.label + ' <------- this is our WAN network' );
      else
          console.log( network.id + '     ' + network.label );
    }
    console.log( "Done! Congrats" );
});
