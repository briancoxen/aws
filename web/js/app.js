var awsApp = angular.module('awsApp', []);

awsApp.service('awsService', ['$http', function ($http){
  this.getThumbnails = function(cb){
    $http.get("https://b7i8yau8a4.execute-api.us-west-1.amazonaws.com/prod/getS3Thumbnails")
      .success(function(data){
        cb(data);
      })
     .error(function(){
    });
  }

  this.postImage = function(cb) {
    $http.post("https://b7i8yau8a4.execute-api.us-west-1.amazonaws.com/prod/postImage")
      .success(function(data){
        cb(data);
      })
      .error(function(){
    })
  }
}]);

awsApp.controller('awsCtrl', ['$scope', 'awsService', function($scope, awsService){
  $scope.photos = [];

  awsService.getThumbnails(function(cb) {
    angular.forEach(cb, function(values) {
      if(values.Key.split("/")[2]) {
        $scope.photos.push(values.Key);
      }
    });
  });
}]);
