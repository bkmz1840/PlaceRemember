ymaps.ready(init);
function init() {
    var locationInput = document.getElementById('remember_location');
    locationInput.disabled = true;
    let myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 6,
        controls: ['typeSelector', 'fullscreenControl', 'zoomControl']
    });
    ymaps.geocode(locationInput.value).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates(),
            bounds = firstGeoObject.properties.get('boundedBy');

        firstGeoObject.options.set('preset', 'islands#darkBlueDotIconWithCaption');
        firstGeoObject.properties.set('iconCaption', firstGeoObject.getAddressLine());

        myMap.geoObjects.add(firstGeoObject);
        myMap.setBounds(bounds, {
            checkZoomRange: true
        });
    });

    myMap.events.add('click', function (e) {
        var currentPoint = e.get('coords');
        myMap.geoObjects.removeAll();
        myMap.geoObjects.add(new ymaps.Placemark(currentPoint));
        let myGeocoder = ymaps.geocode(currentPoint).then(function (res) {
            let geoObject = res.geoObjects.get(0);
            let address = geoObject.getAddressLine()
            locationInput.value = address;
        });
    });
    document.getElementById('submit_remember_update_form').addEventListener("click", function() {
        document.getElementById('remember_location').disabled = false;
    });
}