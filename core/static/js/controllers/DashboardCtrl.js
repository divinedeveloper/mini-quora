myApp.controller('DashboardCtrl', ['$scope', '$http', '$location', '$rootScope', 'toaster', function($scope, $http, $location, $rootScope, toaster) {
        $scope.errorMessage;
    $scope.fileuploaded = "";

        $scope.dashboardCount = function(){

                $http({method: 'GET', url: 'mini-quora/api/v1/dashboard/'}).
                   success(function(data, status, headers, config) {
                    if(status == 200){
                        $scope.responseCountData = data
                           // toaster.pop('success', "", "Welcome to dashboard");
                   }
                       
                       
                     }).
                 error(function(data, status, headers, config) {
                   if(status == 500){
                        toaster.pop('error', "", data.message);
                    }
                     if(status == 502){
                        toaster.pop('error', "", "Server down");
                    }
                    if(status == 503){
                        toaster.pop('error', "", data.message);
                    }
                       if(status == 401){
                           toaster.pop('error', "", data.message);
                       }
                       if(status == 403){
                           toaster.pop('error', "", data.message);
                       }
                     if(status == 400){
                           toaster.pop('error', "", data.message);
                       }
                    if(status == 404){
                        toaster.pop('error', "", data.message);
//                      $location.path("/page-not-found");
                    }
                 }); 

            // $scope.tenantDetails = function(){

                $http({method: 'GET', url: 'mini-quora/api/v1/tenants-dashboard/'}).
                   success(function(data, status, headers, config) {
                    if(status == 200){
                        $scope.responeTenantData = data
                           // toaster.pop('success', "", "Welcome to dashboard");
                   }
                       
                       
                     }).
                 error(function(data, status, headers, config) {
                   if(status == 500){
                        toaster.pop('error', "", data.message);
                    }
                     if(status == 502){
                        toaster.pop('error', "", "Server down");
                    }
                    if(status == 503){
                        toaster.pop('error', "", data.message);
                    }
                       if(status == 401){
                           toaster.pop('error', "", data.message);
                       }
                       if(status == 403){
                           toaster.pop('error', "", data.message);
                       }
                     if(status == 400){
                           toaster.pop('error', "", data.message);
                       }
                    if(status == 404){
                        toaster.pop('error', "", data.message);
//                      $location.path("/page-not-found");
                    }
                 }); 
           
        // }
           
        }

        
        
}]);