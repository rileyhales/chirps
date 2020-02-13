// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

////////////////////////////////////////////////////////////////////////  LOAD THE MAP
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function

////////////////////////////////////////////////////////////////////////  LAYER CONTROLS, MAP EVENTS, LEGEND
mapObj.on("mousemove", function (event) {
    $("#mouse-position").html('Lat: ' + event.latlng.lat.toFixed(4) + ', Lon: ' + event.latlng.lng.toFixed(4));
});

let chirpsLayerObj = newChirpsGEFS();              // adds the wms raster layer
let controlsObj = makeControls();       // the layer toggle controls top-right corner
chirpsLegend.addTo(mapObj);           // add the legend for the WMS forecast layer

////////////////////////////////////////////////////////////////////////  LISTENERS FOR CONTROLS ON THE MENU
function changemap() {
    clearMap();
    chirpsLayerObj = newChirpsGEFS();
    controlsObj = makeControls();
    chirpsLegend.addTo(mapObj);
}

$("#chirpsproducts").change(function () {
    clearMap();
    chirpsLayerObj = newChirpsGEFS();
    controlsObj = makeControls();
    chirpsLegend.addTo(mapObj);
});

$('#colorscheme').change(function () {
    changemap()
});

$("#opacity_raster").change(function () {
    chirpsLayerObj.setOpacity($("#opacity_raster").val())
});
