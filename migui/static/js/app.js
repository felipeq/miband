// -*- mode: js; coding: utf-8 -*-

var miguiApp = angular.module(
    "MiguiApp", ['ngRoute', 'ngAnimate', 'angular-svg-round-progress']);

miguiApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider
	.when('/', {
	    templateUrl: '/static/partials/scan_devices.html',
	});
}]);


Logger = Class.extend({
    on_failure: function(error) {
	log.error(title, message);
    },
});

logger = new Logger();
logger.on_failure = bind(logger, logger.on_failure);

function get_scope_for_element(id) {
    return angular.element(document.getElementById(id)).scope();
};

function wise_application(broker) {
    log.set_level(2);

    var $rootScope = get_scope_for_element("MiguiApp");

    broker.stringToProxy("DeviceManager -w ws").then(
     	function(proxy) {
     	    $rootScope.manager = proxy;
	    $rootScope.wise_ready = true;
	    $rootScope.$apply();

     	}, logger.on_failure);
};
