'use strict';

/* Controllers */

myApp.controller('AppCtrl', ['$scope', '$http', '$rootScope', '$location', 'toaster', function($scope, $http, $rootScope, $location, toaster) {
	$scope.init = function () {
        $location.path("/");
    }
    
    $scope.dashboard = function(){

        $location.path("/dashboard");
    }

    $scope.searchQuestions = function(){

        $location.path("/questions");
    }
    
    $scope.goToHomePage= function(){

        $location.path("/");
    }
    
    
}]);
    