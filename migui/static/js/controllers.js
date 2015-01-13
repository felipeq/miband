// -*- mode: js; coding: utf-8 -*-

miguiApp.controller("ScanCtrl", function($rootScope, $scope, $interval) {
    $scope.devices = [];
    $scope.scan_counter = 0;
    $scope.state = "init";

    $rootScope.$watch("wise_ready", function(newv, oldv) {
    	if (! newv)
    	    return;

    	$scope.state = "first-run";
    });

    $scope.discover = function() {
    	$scope.first_run = false;
    	$scope.state = "discovering";

	$scope.scan_counter++;
	var timeout = Math.pow(2, $scope.scan_counter)
    	$scope.progress = { max: timeout - 1, current: 0, iterations: 59 };

    	var ticks = $interval(function() {
    	    if ($scope.progress.current > $scope.progress.max) {
    		$interval.cancel(ticks);
    		return;
    	    }
    	    $scope.progress.current += 1;
    	}, 1000, timeout);

    	$rootScope.manager.discover(timeout)
	    .then(on_success, on_error);

    	function on_success(devices) {
    	    $interval.cancel(ticks);
    	    $scope.devices = devices;
    	    $scope.progress.current = $scope.progress.max;
    	    $scope.state = devices.length == 0 ? "not-found": "found";
    	    $scope.$apply();
    	};

	function on_error(error) {
	    $interval.cancel(ticks);
	    $scope.state = "error";
	    $scope.error = error;
	};
    };
});
