
var app = angular.module('client', [])

app.controller('controller', function ($scope, $http) {
	$scope.getCalendars = function() {
		$http({
			method: 'GET',
			url: '/api/calendar'
		}).success(function(data) {
			$scope.selected = data.data[0]
			$scope.calendars = data.data
		})
	}
	$scope.getChannels = function() {
		$http({
			method: 'GET',
			url: '/api/channel'
		}).success(function(data) {
			$scope.selected = data.data[0]
			$scope.channels = data.data
		})
	}

	$scope.update = function() {
		$http({
			method:'POST',
			url: '/api/update',
			data: {calendar_id: $scope.selected.id, channel_id: $scope.selectedChannel.id}
		}).success(function(data) {
			console.log('Config successfully saved')
		})
	}
	$scope.setSelected = function(calendar) {
		$scope.selected = calendar
	}
	$scope.setSelectedChannel = function(channel) {
		$scope.selectedChannel = channel
	}

	$scope.getCalendars()
	$scope.getChannels()

})
