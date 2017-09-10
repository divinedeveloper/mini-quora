'use strict';
// Declare app level module which depends on filters, and services
var myApp = angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives','ngRoute', 'ng-environments', 'ngAnimate', 'toaster']).
 	config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider, $rootScope) {
        // $routeProvider.when('/', {
        //     templateUrl: '/static/pages/dashboard.html', 
        //     controller: 'DashboardCtrl',
        // });

        $routeProvider.when('/dashboard', {
            templateUrl: '/static/pages/dashboard.html', 
            controller: 'DashboardCtrl',
        });
        
        $routeProvider.when('/questions', {
            templateUrl: '/static/pages/searchQuestions.html', 
            controller: 'QuestionsCtrl',
        });
        
        $routeProvider.when('/page-not-found', {
            templateUrl: '/static/pages/page-not-found.html'
                       
        });
	    $routeProvider.otherwise({redirectTo: '/'});
	    $locationProvider.html5Mode(true);
  }]);

