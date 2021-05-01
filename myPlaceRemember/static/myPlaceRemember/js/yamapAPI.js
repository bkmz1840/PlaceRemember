ymaps.ready(init);
function init() {
    let myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 7
    });
    let currentPoint = undefined;
    myMap.events.add('click', function (e) {
        var currentPoint = e.get('coords');
        myMap.geoObjects.removeAll();
        myMap.geoObjects.add(new ymaps.Placemark(currentPoint));
        let myGeocoder = ymaps.geocode(currentPoint).then(function (res) {
            let geoObject = res.geoObjects.get(0);
            let address = geoObject.getAddressLine()
            document.getElementById('location').value = address;
        });
    });
}