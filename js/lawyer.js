function lawyerList($scope,$http) {
	$http.get("/lawyers.php?query=SELECT * FROM lawyers").success(function(response) {$scope.lawyers = response;});
}
