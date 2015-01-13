// -*- mode: js; coding: utf-8 -*-

miguiApp.controller("ScanCtrl", function($rootScope, $scope, $interval) {
    $scope.devices = [];
    $scope.scan_counter = 0;
    $scope.state = "init";

    // debug
    $scope.state = "found";
    $scope.devices = [
	{name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
  	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
	// {name: "MI", address: "88:0F:10:10:73:DA"},
    ];


    $rootScope.$watch("wise_ready", function(newv, oldv) {
    	if (! newv)
    	    return;

    	// $scope.state = "first-run";
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

    $scope.pair = function(device) {
	$scope.selected = device;
	$scope.state = "pairing";
    	$scope.progress = {
	    max: 3,
	    current: 0,
	    iterations: 59,
	    color: "#c00",
	    bgcolor: "#eaeaea",
	};

	var cw = 1;
    	var ticks = $interval(function() {
	    var p = $scope.progress;
	    if (p.current == p.max) {
		cw = -1;
		var c = $scope.progress.color;
		$scope.progress.color = $scope.progress.bgcolor;
		$scope.progress.bgcolor = c;
	    }

	    if (p.current == 0 && cw == -1) {
		cw = 1;
		var c = $scope.progress.color;
		$scope.progress.color = $scope.progress.bgcolor;
		$scope.progress.bgcolor = c;
	    }

	    p.current += cw;
    	}, 1000, 60);

    	$rootScope.manager.connect(device.address)
	    .then(on_success, on_error);

	function on_success() {
	    $interval.cancel(ticks);
	};

	function on_error(error) {
	    $interval.cancel(ticks);
	    $scope.state = "error";
	    $scope.error = error;
	};
    };
});
