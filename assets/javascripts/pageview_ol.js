$(document).ready(function () {
    //Display work information / source information
    addOverview = function (url, selector) {
        $.get(url, function (data) {
            $(selector).html(data);
            $(selector).foundation('reveal', 'open')
        });
        //Stop jumping when modal clicked on
        return false;
    }

    /*Openlayers Window*/
    //Set div width/height as proprortion of available screen
    var sf = zoomify_height / zoomify_width;
    var docWidth = parseInt($('body').width());
    var docHeight = parseInt($(window).height());
    var fullWidth = parseInt($('#pageimage').width());
    var fullHeight = fullWidth * sf;

    $("#map").css('width', fullWidth + "px").css("height", fullHeight + "px")

    /* First we initialize the zoomify pyramid (to get number of tiers) */
    var zoomify = new OpenLayers.Layer.Zoomify(
        "Zoomify", zoomify_url,
        new OpenLayers.Size(zoomify_width, zoomify_height));

    /* Map with raster coordinates (pixels) from Zoomify image */
    var options = {
        controls: [],
        maxExtent: new OpenLayers.Bounds(0, 0, zoomify_width, zoomify_height),
        maxResolution: Math.pow(2, zoomify.numberOfTiers - 1),
        numZoomLevels: zoomify.numberOfTiers,
        units: 'pixels'
    };

    map = new OpenLayers.Map("map", options);

    function onPopupClose(evt) {
        //selectControl.unselect(selectedFeature);
    }

    function onFeatureSelect(feature) {
        window.location = '/ocve/browse/barview?workid=' + workid + '&pageimageid=' + pageID + '&barid=' + feature.attributes["barid"];
    }

    function onFeatureUnselect(feature) {
    }

    function showBar(feature) {
        $('span[data-barid=' + feature.feature.attributes['barid'] + ']').parents('div.annotation-box').addClass('highlight');
    }

    function hideBar(feature) {
        $('span[data-barid=' + feature.feature.attributes['barid'] + ']').parents('div.annotation-box').removeClass('highlight');
    }

    var fontSize = '12px';
    var labelAlign = 'cb';

    var barStyles = new OpenLayers.StyleMap({
        "default": new OpenLayers.Style({
            strokeOpacity: 0,
            fillOpacity: 0.0,
            labelAlign: labelAlign
        }),
        "barSelector": new OpenLayers.Style({
            strokeOpacity: 0,
            fillOpacity: 0.0
        }),
        "Initial": new OpenLayers.Style({
            strokeOpacity: 0,
            fillOpacity: 0.0,
            labelAlign: labelAlign
        }),
        "annotation": new OpenLayers.Style({
            strokeOpacity: 1,
            fillOpacity: 0.0,
            strokeColor: 'green',
            label: "${label}",
            labelAlign: labelAlign,
            labelOutlineColor: "white",
            labelOutlineWidth: 3,
            fontColor: "black",
            fontSize: fontSize,
            fontFamily: "Courier New, monospace",
            fontWeight: "bold"
        }),
        "select": new OpenLayers.Style({
            strokeOpacity: 1,
            strokeWidth: 1,
            fillColor: "${fillColor}",
            fillOpacity: 0.3,
            pointRadius: 6,
            pointerEvents: "visiblePainted",
            // label with \n linebreaks
            label: "${label}",
            fontColor: "black",
            fontSize: fontSize,
            fontFamily: "Courier New, monospace",
            fontWeight: "bold",
            labelAlign: labelAlign,
            labelOutlineColor: "white",
            labelOutlineWidth: 3
        }),
        "temporary": new OpenLayers.Style({
            strokeOpacity: 1,
            strokeWidth: 1,
            strokeColor: 'red',
            pointRadius: 6,
            pointerEvents: "visiblePainted",
            // label with \n linebreaks
            label: "${label}",
            labelAlign: labelAlign,
            labelOutlineColor: "white",
            labelOutlineWidth: 3,
            fontColor: "red",
            fontSize: "12px",
            fontFamily: "Courier New, monospace",
            fontWeight: "bold"
        })
    });

    //Bar layers
    vlayer = new OpenLayers.Layer.Vector("Editable", {
        strategies: [new OpenLayers.Strategy.Fixed()],
        styleMap: barStyles,
        protocol: new OpenLayers.Protocol.HTTP({
            url: regionURL,
            format: new OpenLayers.Format.GeoJSON()
        })
    });


    noteStyles = new OpenLayers.StyleMap({
        "default": new OpenLayers.Style({
            strokeOpacity: 1,
            fillOpacity: 0.0,
            display: 'none'
        }),
        "visibleNote": new OpenLayers.Style({
            strokeOpacity: 1,
            fillOpacity: 0.0,
            strokeColor: 'orange',
            display: 'block'
        }),
        "invisibleNote": new OpenLayers.Style({
            strokeOpacity: 1,
            fillOpacity: 0.0,
            display: 'none'
        }),
        "Commentary": new OpenLayers.Style({
            strokeOpacity: 0,
            fillOpacity: 0.0
        }),
        "selectedNote": new OpenLayers.Style({
            strokeOpacity: 1,
            fillOpacity: 0.0,
            strokeColor: '#00BFFF',
            display: 'block'
        })
    });

    //Annotation layer
    alayer = new OpenLayers.Layer.Vector("Editable", {
        strategies: [new OpenLayers.Strategy.Fixed()],
        styleMap: noteStyles,
        protocol: new OpenLayers.Protocol.HTTP({
            url: noteURL,
            format: new OpenLayers.Format.GeoJSON()
        })
    });

    highlightCtrl = new OpenLayers.Control.SelectFeature(vlayer, {
        hover: true,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            featurehighlighted: showBar,
            featureunhighlighted: hideBar
        }

    });

    selectControl = new OpenLayers.Control.SelectFeature(
        vlayer,
        {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});

    map.addLayers([zoomify, vlayer, alayer]);

    var mouse = new OpenLayers.Control.Navigation({'zoomWheelEnabled': false});

    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(selectControl);
    map.addControl(highlightCtrl);
    map.addControl(mouse);
    map.zoomToMaxExtent();


    vlayer.events.register("loadend",vlayer,loadselectedregion);
    highlightCtrl.activate();
    selectControl.activate();
    annotationEvents();

});
