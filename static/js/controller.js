
var app = angular.module('client', [])

app.controller('controller', function ($scope, $http) {
	$scope.getCalendars = function() {
		$http({
			method: 'GET',
			url: '/api/calendar'
		}).success(function(data) {
			$scope.selectedCalendar = data.data.selected
			$scope.calendars = data.data.calendars;
		})
	}
	
	$scope.getCongratulations = function() {
		$http({
			method: 'GET',
			url: '/api/congrats'
		}).success(function(data, status) {
			$scope.congrats = data.congrats;
		})
	}

	$scope.createCongratulation = function() {
		$http({
			method: 'POST',
			data: { text: $scope.congrat_text },
			url: '/api/congrats'
		}).success(function(data, status) {
			$scope.congrats.push(data)
		})
	}

	$scope.dropCongratulation = function(id) {
		$http({
			method: 'DELETE', 
			url: '/api/congrats',
			params: {id: id}
		}).success(function(data){
			console.log(data);
			var ids = $scope.congrats.map(function(d){return d._id})
			$scope.congrats.splice(ids.indexOf(id), 1)
		})
	}
	$scope.getChannels = function() {
		$http({
			method: 'GET',
			url: '/api/channel'
		}).success(function(data) {
			$scope.selectedChannel = data.data.selected;
			$scope.channels = data.data.channels;
		})
	}
	$scope.update = function() {
		$http({
			method:'POST',
			url: '/api/update',
			data: {calendar_id: $scope.selectedCalendar, channel_id: $scope.selectedChannel}
		}).success(function(data) {
			console.log('Config successfully saved')
		})
	}
	$scope.setSelected = function(calendar) {
		$scope.selectedCalendar = calendar
	}
	$scope.setSelectedChannel = function(channel) {
		$scope.selectedChannel = channel
	}

	$scope.getCongratulations();
	$scope.getCalendars();
	$scope.getChannels();
})
