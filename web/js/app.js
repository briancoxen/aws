var awsApp = angular.module('awsApp', []);

awsApp.service('awsService', ['$http', function ($http){
  this.getThumbnails = function(cb){
    $http.get("https://zoitjqaeuh.execute-api.us-west-1.amazonaws.com/prod/getS3Thumbnails")
      .success(function(data){
        cb(data);
      })
     .error(function(){
    });
  }

  this.postImage = function(cb, image) {
    $http.post("https://zzw1lwv0kb.execute-api.us-west-1.amazonaws.com/prod/postImage", { url: image })
      .success(function(data){
        cb(data);
      })
      .error(function(){
    })
  }
}]);

awsApp.controller('awsCtrl', ['$scope', 'awsService', function($scope, awsService){
  $scope.imageForm = true;
  $scope.photos = [];

  awsService.getThumbnails(function(cb) {
    angular.forEach(cb, function(values) {
      if(values.Key.split("/")[2]) {
        $scope.photos.push(values.Key);
      }
    });
  });

  $scope.uploadImage = function() {
    $scope.imageForm = false;
    $scope.loader = true;
    awsService.postImage(function(cb) {
      $scope.loader = false;
      $scope.imageForm = true;
      $scope.imageURL = "";
      $scope.photos = [];
      awsService.getThumbnails(function(cb) {
        angular.forEach(cb, function(values) {
          if(values.Key.split("/")[2]) {
            $scope.photos.push(values.Key);
          }
        });
      });
    }, $scope.imageURL); 
  };
}]);
