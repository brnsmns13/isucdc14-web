function caseList($scope,$http) {
	$http.get("/clients.php?query=SELECT * FROM candc").success(function(response) {$scope.cases = response;});
}
