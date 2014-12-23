// -*- mode: js; coding: utf-8 -*-

miguiApp.controller("ScanCtrl", function($rootScope, $scope, $interval) {
    $scope.devices = [];
    $scope.state = "init";

    $rootScope.$watch("wise_ready", function(newv, oldv) {
	if (! newv)
	    return;

	$scope.state = "first-run";
    });

    $scope.discover = function() {
	$scope.first_run = false;
	$scope.state = "discovering";
	$scope.progress = { max: 100, current: 10, iterations: 59 };

	var ticks = $interval(function() {
	    if ($scope.progress.current > $scope.progress.max) {
		$interval.cancel(ticks);
		return;
	    }
	    $scope.progress.current += 20;
	}, 1000, 5);

	$rootScope.manager.discover().then(on_success, logger.on_failure);

	function on_success(devices) {
	    $interval.cancel(ticks);
	    $scope.devices = devices;
	    $scope.progress.current = $scope.progress.max;
	    $scope.state = devices.length == 0 ? "not-found": "found";
	    $scope.$apply();
	};
    };
});
