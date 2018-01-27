var rootDomain = '192.168.20.13';

var getPic = function () {
    $.get('http://'+rootDomain+':10000/', function(data) {
        console.log('got it!');
    });
}

var setUp = function() {

    // Clear the map.
    $.ajax({
        url:'http://'+rootDomain+':10001/map',
        type: 'DELETE',
        crossDomain: true
    })

    // Grab an image from the camera.
    getPic();

}

$(document).ready(function () {

    setUp();

});
