myApp.controller('QuestionsCtrl', ['$scope', '$http', '$location', '$routeParams', 'toaster', function($scope, $http, $location, $routeParams, toaster) {
        $scope.successMessage;
        $scope.errorMessage;
        $scope.searchQuestions = function(){
            
            // $http({method: 'GET', url: 'iec/api/v1/retrieve/' {params:{"code": $scope.ieCode}} }).            
            // $http.get('mini-quora/api/v1/questions/', {params: {"title": $scope.title}}, {headers: {'api-key': $scope.apiKey}}).

            $http(
                {
                  method: 'GET', 
                  url: 'mini-quora/api/v1/questions/', 
                  headers: {'api-key': $scope.apiKey},
                  params: {"title": $scope.title}

                }).
                success(function(data, status, headers, config) {
                       if(status == 200){
                        $scope.responseQuestions = data
                           // toaster.pop('success', "", "");
                       }

                     }).
                error(function(data, status, headers, config) {
                    if(status == 401){
                        toaster.pop('error', "", data.message);
                    }
                    if(status == 400){
                        toaster.pop('error', "", data.message);
                    }
                    if(status == 500){
                        toaster.pop('error', "", data.message);
                    }
                    if(status == 502){
                        toaster.pop('error', "", "Server down");
                    }
                    if(status == 503){
                        toaster.pop('error', "", data.message);
                    }
                    if(status == 404){
                        toaster.pop('error', "", data.message);
//                      $location.path("/page-not-found");
                    }
                    if(status == 429){
                        toaster.pop('error', "", data.detail + ". Please wait for " + data.availableIn);
                    }
//                   $scope.errorMessage = data.message;
                 }); 
        }
        
}]);