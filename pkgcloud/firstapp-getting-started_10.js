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

var security_group_name           = 'all-in-one';
var security_group_description    = 'group for all in none security';

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
    listingSecurityGroups();
  }
  else {
    console.log( ' creating security group ' + security_group_name );
    openstack.addGroup( { 'name' : security_group_name, 'description' : security_group_description }, function (err, newSgroup) {
      if (err) { console.log(err); return; }

      openstack.addRule({ 'groupId': newSgroup.id, 'ipProtocol' : 'TCP', 'fromPort' : 80, 'toPort' : 80 }, function (err, newRule) {
        if (err) { console.log(err); return; }

        openstack.addRule({ 'groupId': newSgroup.id, 'ipProtocol' : 'TCP', 'fromPort' : 22, 'toPort' : 22 }, function (err, newRule) {
          if (err) { console.log(err); return; }

          listingSecurityGroups();
        });
      });
    });
  }
});

function listingSecurityGroups( ) {
  console.log( 'Listing security groups...' );
  openstack.listGroups( function (err, security_groups){
    if (err) { console.log(err); return; }

    var security_group = null;
    for( var currentSGroupIndex = 0, len = security_groups.length; currentSGroupIndex < len; currentSGroupIndex++ ) {
      security_group = security_groups[ currentSGroupIndex ];
      console.log( '\t- found security group with id ' + security_group.id + ' and name ' + security_group.name );
    }
    console.log( "Done! Congrats" );
  })
}
