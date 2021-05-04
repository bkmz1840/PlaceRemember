ymaps.ready(init);
function init() {
    let location = document.getElementById("remember_location");
    let myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 6,
        controls: ['typeSelector', 'fullscreenControl', 'zoomControl']
    });
    ymaps.geocode(location.innerHTML).then(function (res) {
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
}