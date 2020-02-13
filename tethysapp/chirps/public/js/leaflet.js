////////////////////////////////////////////////////////////////////////  MAP FUNCTIONS
function map() {
    // create the map
    return L.map('map', {
        zoom: 3,
        minZoom: 2,
        maxZoom: 3,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100, -225), L.latLng(100, 225)),
        center: [0, 0],
    });
}

function basemaps() {
    return {
        "ESRI Topographic": L.esri.basemapLayer('Topographic').addTo(mapObj),
        "ESRI Terrain": L.layerGroup([L.esri.basemapLayer('Terrain'), L.esri.basemapLayer('TerrainLabels')]),
        "ESRI Grey": L.esri.basemapLayer('Gray'),
    }
}

////////////////////////////////////////////////////////////////////////  WMS LAYERS FOR PRECIPITATION FORECASTS
function newChirpsGEFS() {
    let productvariable = $("#chirpsproducts").val().split('_');
    let wmsurl = thredds_url + '/chirpsgefs_20200213.nc4';
    return L.tileLayer.wms(wmsurl, {
        layers: productvariable[1],
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity_raster").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/' + $('#colorscheme').val(),
        colorscalerange: '0,100',
    }).addTo(mapObj);
}
////////////////////////////////////////////////////////////////////////  FORECAST LAYER LEGEND
// the forecast layer raster legend
let chirpsLegend = L.control({position: 'bottomleft'});
chirpsLegend.onAdd = function () {
    let productvariable = $("#chirpsproducts").val().split('_');
    let max = '100';
    let div = L.DomUtil.create('div', 'legend');
    let url = thredds_url + '/chirpsgefs_20200213.nc4' + "?REQUEST=GetLegendGraphic&LAYER=" + productvariable[1] + "&PALETTE=" + $('#colorscheme').val() + "&COLORSCALERANGE=0," + max;
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};

////////////////////////////////////////////////////////////////////////  MAP CONTROLS AND CLEARING
// the layers box on the top right of the map
function makeControls() {
    return L.control.layers(basemapObj, {
        'Forecast Layer': chirpsLayerObj,
    }).addTo(mapObj);
}

// you need to remove layers when you make changes so duplicates dont persist and accumulate
function clearMap() {
    // remove the controls for the wms layer then remove it from the map
    controlsObj.removeLayer(chirpsLayerObj);
    mapObj.removeLayer(chirpsLayerObj);
    // now delete the controls object
    mapObj.removeControl(controlsObj);
}