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

console.log( 'Cleaning up test instances...' );
openstack.getServers(function (err, servers) {
    if (err) { console.log(err); return; }

    var server = null;
    for( var currentServerIndex = 0, len = servers.length; currentServerIndex  < len; currentServerIndex++ ) {
        server = servers[ currentServerIndex ];
        if( server.name != null &&
            server.name.indexOf( 'pkgcloud' ) > 0 ){
              console.log( ' -> deleting server with ID : ' + server.id );
              openstack.destroyServer( server.id, function (err, servers){
                    if (err) { console.log(err); return; }
              } );
        }
    }
});
