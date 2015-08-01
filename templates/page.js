function initialize() {
  var mapOptions = {
    center: { lat: 51.507351,
    lng: -0.127758},
    zoom: 5
  };

  var map = new google.maps.Map(
    document.getElementById('map-canvas'),
    mapOptions
  );

  map.data.setStyle({
    icon: '//example.com/path/to/image.png',
    fillColor: 'green'
  });

  map.data.loadGeoJson(
    '../resource/exampleData.json'
  );

  map.data.addListener('click', function(event) {
      map.data.overrideStyle(event.feature, {fillColor: 'red'});
  });

  map.data.addListener('mouseover', function(event) {
    map.data.overrideStyle(event.feature, {fillColor: 'blue'});
  });

  map.data.addListener('mouseout', function(event) {
    map.data.overrideStyle(event.feature, {fillColor: 'red'});
  });

}

google.maps.event.addDomListener(window, 'load', initialize);
