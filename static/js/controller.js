
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

	$scope.getCalendars()
	$scope.getChannels()

})
