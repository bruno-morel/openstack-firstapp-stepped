var winston = require('winston');
var pkgcloud = require('pkgcloud');
var yaml = require('yamljs');

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

var config = yaml.load( 'clouds.yaml' );
var openstack = pkgcloud.compute.createClient({
    provider:     "openstack",
    username:     config[ "clouds" ][ "internapNYJ" ][ "auth" ].username,
    password:     config[ "clouds" ][ "internapNYJ" ][ "auth" ].password,
    authUrl:      config[ "clouds" ][ "internapNYJ" ][ "authUrl" ],
    region:       config[ "clouds" ][ "internapNYJ" ][ "region_name" ]
});

openstack.on('log::*', function (message, object) {
    if (object) logger.log(this.event.split('::')[1], message, object);
    else        logger.log(this.event.split('::')[1], message);

    console.log( message );
    console.log( object );
});

console.log( JSON.stringify( openstack ) );
console.log( openstack );
console.log( "Done! Congrats" );
