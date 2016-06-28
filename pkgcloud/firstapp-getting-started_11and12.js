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

var security_group_name           = 'all-in-one';
var security_group_description    = 'group for all in none security';
var instance_name                 = 'test instance for pkgcloud';
var keypair_name                  = 'demokey';

console.log( 'Checking for existing security group named ' + security_group_name + '...' );
openstack.listGroups( function (err, security_groups) {
  if (err) { console.log(err); return; }

  var security_group = null;
  for( var currentSGroupIndex = 0, len = security_groups.length; currentSGroupIndex < len; currentSGroupIndex++ ) {
    security_group = security_groups[ currentSGroupIndex ];
    if( security_group.name != null &&
        security_group.name == security_group_name )
        break;
  }

  if( security_group.name == security_group_name )
  {
    console.log( ' ' + security_group_name + " already exists, skipping creation..." );
    continuewithCreatingInstance();
  }
  else {
    console.log( ' creating security group ' + security_group_name );
    openstack.addGroup( { 'name' : security_group_name, 'description' : security_group_description }, function (err, newSgroup) {
      if (err) { console.log(err); return; }

      openstack.addRule({ 'groupId': newSgroup.id, 'ipProtocol' : 'TCP', 'fromPort' : 80, 'toPort' : 80 }, function (err, newRule) {
        if (err) { console.log(err); return; }

        openstack.addRule({ 'groupId': newSgroup.id, 'ipProtocol' : 'TCP', 'fromPort' : 22, 'toPort' : 22 }, function (err, newRule) {
          if (err) { console.log(err); return; }

          continuewithCreatingInstance();
        });
      });
    });
  }
});

function continuewithCreatingInstance( ) {
  console.log( "Checking if instance with name " + instance_name + "doesn't exist already" );
  openstack.getServers( function (err, servers){
    if (err) { console.log(err); return; }

    var server = null;
    for( var currentServerIndex = 0, len = servers.length; currentServerIndex  < len; currentServerIndex++ ) {
        server = servers[ currentServerIndex ];
        if( server.name != null &&
            server.name.indexOf( instance_name ) > 0 ){
              break;
        }
    }

    if( server != null &&
        server.name != null &&
        server.name.indexOf( instance_name ) > 0 ){
          console.log( "\tfound server, skipping creation");
          console.log( "Done! Congrats");
    }
    else {
      console.log( "\tinstance not active");
      createInstance();
    }
  });
}

function createInstance() {
  console.log( "Creating the instance");
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

              console.log( "\nCreating instance " + instance_name + "..." );
              openstack.createServer({  name: instance_name,
                                        image: image,
                                        flavor: flavor,
                                        keyname: keypair_name,
                                        securityGroups : [{'name':security_group_name}],
                                        networks: [{uuid:netWAN.id.toString()}] },
                                      handleServerCreation );
          });
      });
  });
}
