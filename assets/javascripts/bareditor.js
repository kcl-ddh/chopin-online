DeleteFeature = OpenLayers.Class(OpenLayers.Control, {
    initialize:function (layer, options) {
        OpenLayers.Control.prototype.initialize.apply(this, [options]);
        this.layer = layer;
        this.handler =
            new OpenLayers.Handler.Feature(this,
                layer, {click:this.clickFeature});
    },
    clickFeature:function (feature) {
        // if feature doesn't have a fid, destroy it
        this.layer.destroyFeatures([feature]);
        var format = new OpenLayers.Format.GeoJSON();
        updateRegions(2, null, format.write(feature), 1);
    },
    setMap:function (map) {
        this.handler.setMap(map);
        OpenLayers.Control.prototype.setMap.apply(this, arguments);
    },
    CLASS_NAME:"OpenLayers.Control.DeleteFeature"
});

saveAll = function () {
    var format = new OpenLayers.Format.GeoJSON();
    var geoJson = format.write(vlayer.features);
    updateRegions(0, null, geoJson, 0)
}

updateRegionCoords = function (f, pixel) {
    var id = f.attributes.id;
    var bounds = (f.geometry.getBounds());
    var x = bounds.left;
    var y = bounds.top;
    var width = bounds.getWidth();
    var height = bounds.getHeight();
    //updateBarRegion('U', {regionid:id,x:x,y:y,width:width,height:height});

}

writeEndCoords = function (f, pixel) {
    var bounds = (f.geometry.getBounds());
    endX = bounds.left;
    endY = bounds.top;
};

populateBarForm= function(barNumber,regionID,anomaly){
    $('#barNumber').val(barNumber)
    $('#regionID').val(regionID)
    if (anomaly == 1) {
        $('#anomaly').attr('checked', true);
    } else {
        $('#anomaly').attr('checked', false);
    }
};

featurePopulateBarForm = function (f, pixel) {
    populateBarForm(f.attributes.label,f.attributes.id,f.attributes.anomaly)
};

/*
 Insert,update and delete bar regions.  Called by openLayers toolbar
 op = operation insert, etc.
 f = feature for updating inserted feature with barregion id, null in other operations
 geojson = geometry data to be passed
 */
updateRegions = function (op, f, geoJson, showmsg) {
    postData = '';
    var newid = 0
    if (op == 1) {
        //insert new region
        postData = {"insert":1, "pageID":pageID, "regions":geoJson}
    } else if (op == 2) {
        //Delete
        postData = {"delete":1, "pageID":pageID, "regions":geoJson}
    } else {
        //Update
        postData = {"pageID":pageID, "regions":geoJson}
    }

    $.ajax({
        type:'POST',
        url:'/ocve/updateBarRegions/',
        dataType:"json",
        data:postData,
        error:function (xhr, textStatus, errorThrown) {
            //alert('Saved');
        },
        success:function (result) {
            if (showmsg == 1) {
               // alert(result.message)
            }
            if (result.id) {
                f.attributes.id = result.id;
            }
        }
    });

}

/*
 This tool will draw an entire system, then prompt the user how many bars it should be split into.
 NOTE: function has no idea where bar lines are.
 */
createSystemBounds = function (feature) {
    var vertices = feature.geometry.getVertices();
    createSystemControl.deactivate();
    drawSystemPoint.systemfeature=feature
    drawSystemPoint.activate();
};

addBarPoint=function (feature) {
    if (!drawSystemPoint.systemPoints){
        drawSystemPoint.systemPoints=new Array();
    }
    //var x=feature.geometry.getVertices()[0].x;
    drawSystemPoint.systemPoints.push(feature)

};
finishSystem = function(){
    drawSystemPoint.systemPoints.sort(function(a,b){return a.geometry.getVertices()[0].x-b.geometry.getVertices()[0].x});
    var newRegions=new Array();
    var vertices = drawSystemPoint.systemfeature.geometry.getVertices();
    vlayer.removeFeatures(drawSystemPoint.systemfeature);
    var bottomY = vertices[0].y;
    var topY = vertices[1].y;
    var leftX = vertices[0].x;
    var rightX = vertices[2].x;
    var x1=0;
    var x2=0;
    var red = '#A52A2A';
    var blue = "#00BFFF";
    var colour = blue;
    if (drawSystemPoint.systemPoints.length>0){
        //First point
        x1=leftX;
        x2=drawSystemPoint.systemPoints[0].geometry.getVertices()[0].x;
        //Default attributes, alternating colours
        var attributes = {"id":0, "fillColor":red, "label":"0"}
        //Create new vertices
        var points = new Array();
        points[0] = new OpenLayers.Geometry.Point(x1, bottomY);
        points[1] = new OpenLayers.Geometry.Point(x1, topY);
        points[2] = new OpenLayers.Geometry.Point(x2, topY);
        points[3] = new OpenLayers.Geometry.Point(x2, bottomY);
        var ring = new OpenLayers.Geometry.LinearRing(points);
        var polygon = new OpenLayers.Geometry.Polygon([ring]);
        //New object
        var newF = new OpenLayers.Feature.Vector(polygon, attributes);
        newRegions.push(newF);
    }
    for (var i=0;i<drawSystemPoint.systemPoints.length;i++){
        var next=i+1;
        if (next==drawSystemPoint.systemPoints.length){
            //Last system point use box as x2
            x1=drawSystemPoint.systemPoints[i].geometry.getVertices()[0].x;
            x2=rightX
        }else{
            x1=drawSystemPoint.systemPoints[i].geometry.getVertices()[0].x;

            x2=drawSystemPoint.systemPoints[next].geometry.getVertices()[0].x;
        }

        //Default attributes, alternating colours
        var attributes = {"id":0, "fillColor":colour, "label":"0"}
        //Create new vertices
        var points = new Array();
        points[0] = new OpenLayers.Geometry.Point(x1, bottomY);
        points[1] = new OpenLayers.Geometry.Point(x1, topY);
        points[2] = new OpenLayers.Geometry.Point(x2, topY);
        points[3] = new OpenLayers.Geometry.Point(x2, bottomY);
        var ring = new OpenLayers.Geometry.LinearRing(points);
        var polygon = new OpenLayers.Geometry.Polygon([ring]);
        //New object
        var newF = new OpenLayers.Feature.Vector(polygon, attributes);
        if (colour.indexOf(blue) > -1) {
            colour = red;
        } else {
            colour = blue;
        }
        newRegions.push(newF);
        vlayer.removeFeatures(drawSystemPoint.systemPoints[i]);
    }
    //Add to layer
    vlayer.addFeatures(newRegions);
    drawSystemPoint.systemPoints=null;
    drawSystemPoint.systemfeature=null;
}


initControls = function (vlayer) {
    var format = new OpenLayers.Format.GeoJSON();
    deleteFeature = new DeleteFeature(vlayer,
        {displayClass:"olControlDeleteFeature", title:'Delete'});

    rectangleFeature = new OpenLayers.Control.DrawFeature(vlayer,
        OpenLayers.Handler.RegularPolygon,

        {   featureAdded:function (e) {
            updateRegions(1, e, format.write(e), 1);

        },
            handlerOptions:{sides:4, irregular:true},
            title:"Draw Rectangle",
            displayClass:"olControlDrawFeaturePolygon"});
    var polygonFeature = new OpenLayers.Control.DrawFeature(vlayer,
        OpenLayers.Handler.Polygon,
        {displayClass:"olControlDrawFeaturePolygon",
            title:"Draw Polygon"});

    selectFeature = new OpenLayers.Control.SelectFeature(vlayer,
        {title:'Select', clickout:true, toggle:false,
            displayClass:"olControlSelectFeature",
            multiple:true, hover:false,
            toggleKey:"ctrlKey", // ctrl key removes from selection
            multipleKey:"shiftKey", // shift key adds to selection
            box:true, onSelect:featurePopulateBarForm
        });

    createSystemControl = new OpenLayers.Control.DrawFeature(vlayer,
        OpenLayers.Handler.RegularPolygon,

        {
            featureAdded:createSystemBounds,
            handlerOptions:{sides:4,
                irregular:true},
            title:"Draw System",
            displayClass:"olControlCreateSystem"});

    drawSystemPoint = new OpenLayers.Control.DrawFeature(vlayer,
        OpenLayers.Handler.Point,{featureAdded:addBarPoint})
    drawSystemPoint.events.register("deactivate", null, finishSystem);

    var dragFeature = new OpenLayers.Control.DragFeature(vlayer,
        {displayClass:"olControlDragFeature", title:'Drag'});

    var modifyFeature = new OpenLayers.Control.ModifyFeature(vlayer,
        {sides:4, mode:OpenLayers.Control.ModifyFeature.RESHAPE,
            displayClass:"olControlModifyFeature",
            title:'Modify'});

    transformFeature = new TransformFeature(vlayer, {
        renderIntent:'transform',
        rotate:false,
        irregular:true,
        displayClass:'olControlTransformFeature',
        title:'Transform'
    });

    saveButton = new OpenLayers.Control.Button({
        title:'Save',
        trigger:function () {
            if (modifyFeature.feature) {
                modifyFeature.selectControl.unselectAll();
            }
            var form = $('#frmAnnotation');
            saveAll();
        },
        displayClass:'olControlSaveFeatures'
    });
    var panelControls = [saveButton,
        deleteFeature,
        rectangleFeature,
        selectFeature,
        dragFeature,
        transformFeature,
        createSystemControl
        ,drawSystemPoint
    ]

    var toolbarPanel = new OpenLayers.Control.Panel(
        {displayClass:"olControlEditingToolbar"});
    toolbarPanel.addControls(panelControls);
    return toolbarPanel;
};


saveSuccess = function (event) {
    alert('Changes saved');
}

//Programatically move a feature's centre dx and/or dy
moveFeatureFixed = function (f, dx, dy) {
    //Feature centre, have to do it this way the OpenLayers methods don't seem right
    var newPoint = map.getPixelFromLonLat(f.geometry.getBounds().getCenterLonLat());
    newPoint.x = newPoint.x + dx;
    if (dy != 0) {
        newPoint.y = newPoint.y + dy;
    }
    //Apply change
    f.move(newPoint);
}


/*Transform a rectangular feature (as in bar region)
 Points in diagram:
 1 2
 0 3
 Currently, this function is forced to clone the feature, apply the deltas and destroy the old one
 */
transformFeatureFixed = function (f, dx0, dy0, dx1, dy1, dx2, dy2, dx3, dy3) {
    var vertices = f.geometry.getVertices();
    var attributes = f.attributes;
    vlayer.removeFeatures(f);
    vertices[0].x = vertices[0].x + dx0;
    vertices[0].y = vertices[0].y + dy0;
    vertices[1].x = vertices[1].x + dx1;
    vertices[1].y = vertices[1].y + dy1;
    vertices[2].x = vertices[2].x + dx2;
    vertices[2].y = vertices[2].y + dy2;
    vertices[3].x = vertices[3].x + dx3;
    vertices[3].y = vertices[3].y + dy3;

    var ring = new OpenLayers.Geometry.LinearRing(vertices);
    var polygon = new OpenLayers.Geometry.Polygon([ring]);
    var newF = new OpenLayers.Feature.Vector(polygon, attributes);
    vlayer.addFeatures(newF);
    selectFeature.select(newF);
    return newF;
};

/*
 Takes a selection of features and makes their vertical edges uniform
 Intended to even out the bar boxes of a system so they are uniform
 NOTE:  Currently 'greedy,' as in maximizes size of boxes
 returns a set of new features with same attributes and new geometries
 */
smoothFeatureEdges = function (features) {
    var newFeatures = new Array();
    var minY = 9999;
    var maxY = 0;
    //Determine maximum vertical extent
    for (var i = 0; i < features.length; i++) {
        var f = features[i];
        var vertices = f.geometry.getVertices();
        //Bottom edge, y is reversed in OpenLayers
        if (vertices[0].y < minY) {
            minY = vertices[0].y;
        }
        if (vertices[1].y > maxY) {
            maxY = vertices[1].y;
        }
    }

    //Apply new y coordinates to all selected features
    for (i = 0; i < features.length; i++) {
        f = features[i];
        vertices = f.geometry.getVertices();
        //The transformation offsets
        var matrix = [0, 0, 0, 0, 0, 0, 0, 0];
        if (vertices[0].y != minY) {
            matrix[1] = minY - vertices[0].y;
            matrix[7] = minY - vertices[3].y;
        }

        if (vertices[1].y != maxY) {
            matrix[3] = maxY - vertices[1].y;
            matrix[5] = maxY - vertices[2].y;
        }
        //alert(matrix);
        transformFeatureFixed(f, matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5], matrix[6], matrix[7]);
    }
    return newFeatures;
};


sortFeatures = function (a) {
    var swapped;
    do {
        swapped = false;
        for (var i = 0; i < a.length - 1; i++) {
            var v1 = a[i].geometry.getVertices();
            var v2 = a[i + 1].geometry.getVertices();
            if (v1[1].y < v2[1].y) {
                var temp = a[i];
                a[i] = a[i + 1];
                a[i + 1] = temp;
                swapped = true;
            } else if (v1[1].y == v2[1].y && v1[1].x > v2[1].x) {
                var temp = a[i];
                a[i] = a[i + 1];
                a[i + 1] = temp;
                swapped = true;
            }
        }
    } while (swapped);
    return a;
};

/*
 Selects the next bar in a page to allow tab navigation
 */
nextBar = function (features, selected) {
    var current;
    var next;
    features = sortFeatures(features);
    if (selected && selected.length > 0) {
        for (var i = 0; i < selected.length; i++) {
            current = selected[i];
        }

        for (i = 0; i < features.length; i++) {
            if (current == features[i]) {
                if ((i + 1) < features.length) {

                    next = features[(i + 1)];
                } else {
                    //Last bar reached, wrap back around to first
                    //next = features[0];
                }
            }
        }
    } else {
        next = features[0];
    }
    //Unselect all
    selectFeature.unselectAll();
    //Select next bar
    selectFeature.select(next);

};

//Handles all keyboard shortcuts for the edit window
//Current shortcuts are based off arrow keys with ctrl & alt modifiers:
//Just arrow key: move selected bars
//ctrl: expand bar(s) edge in that direction
//ctrl&alt: reduce bar(s) edge in that direction
//Note: ctrl+alt used because of alt-based shortcuts native to FireFox,Chrome
keyboardShortcuts = function (event) {
    //Key code
    var code = event.keyCode;
    //Is control depressed?
    var ctrl = event.ctrlKey;
    //Is alt depressed?
    var alt = event.altKey;
    //Number of pixels to move selected object
    var dragOffset = 5;
    //Number of pixels to increase vertex when resizing
    var tOffset = 10;
    var selected = vlayer.selectedFeatures.slice(0);
    var newFeatures = new Array();
    var total = selected.length;
    var newF = null;
    //Special case for 'next' key, so it activates if nothing selected

    if (code == 78) {
        //N, next bar
        //Sort?
        var features = vlayer.features.slice(0);
        var current = vlayer.selectedFeatures.slice(0);
        nextBar(features, current);
    } else if (code == 27 && total==0) {
        //Escape
        if (drawSystemPoint.active) {
            //Finalise system
            drawSystemPoint.deactivate();
            //Restart
                createSystemControl.activate();

        }else if (createSystemControl.active){
            createSystemControl.deactivate();
        }
    } else {
        //Keyboard shortcuts used to move/manipulate bars that have been selected
        for (var i = 0; i < total; i++) {
            var f = selected[i];
            switch (code) {
                case 37:
                    //left arrow
                    if (ctrl && alt) {
                        newF = transformFeatureFixed(f, 0, 0, 0, 0, tOffset * -1, 0, tOffset * -1, 0);
                    } else if (ctrl) {
                        newF = transformFeatureFixed(f, tOffset * -1, 0, tOffset * -1, 0, 0, 0, 0, 0);
                    } else {
                        moveFeatureFixed(f, -5, 0);
                    }
                    break;
                case 38:
                    //up arrow
                    if (ctrl && alt) {
                        newF = transformFeatureFixed(f, 0, tOffset, 0, 0, 0, 0, 0, tOffset);
                    } else if (ctrl) {
                        newF = transformFeatureFixed(f, 0, 0, 0, tOffset, 0, tOffset, 0, 0);
                    } else {
                        moveFeatureFixed(f, 0, dragOffset * -1);
                    }
                    break;
                case 39:
                    //right arrow
                    if (ctrl && alt) {
                        newF = transformFeatureFixed(f, tOffset, 0, tOffset, 0, 0, 0, 0, 0);
                    } else if (ctrl) {
                        newF = transformFeatureFixed(f, 0, 0, 0, 0, tOffset, 0, tOffset, 0);
                    } else {
                        moveFeatureFixed(f, dragOffset, 0);
                    }
                    break;
                case 40:
                    //down arrow
                    if (ctrl && alt) {
                        newF = transformFeatureFixed(f, 0, 0, 0, tOffset * -1, 0, tOffset * -1, 0, 0);
                    } else if (ctrl) {
                        newF = transformFeatureFixed(f, 0, tOffset * -1, 0, 0, 0, 0, 0, tOffset * -1);
                    } else {
                        moveFeatureFixed(f, 0, dragOffset);
                    }
                    break;
                case 27:
                    //Escape
                    //Unselect all
                    selectFeature.unselectAll();
                    break;
                case 46:
                    //Delete
                    var feature=vlayer.selectedFeatures[0];
                    var format = new OpenLayers.Format.GeoJSON();
                    updateRegions(2, null, format.write(feature), 1);
                    vlayer.destroyFeatures(vlayer.selectedFeatures.slice(0));
                    break;
                case 70:
                    //f
                    if (ctrl && alt) {
                        //make system uniform
                        var selected = vlayer.selectedFeatures.slice(0);
                        if (selected && selected.length > 1) {
                            smoothFeatureEdges(selected);
                        }
                    }
                    break;

            }
        }
    }
};

$(document).ready(function () {


    $('#smoothTest').click(function () {
        var selected = vlayer.selectedFeatures.slice(0);
        if (selected && selected.length > 1) {
            smoothFeatureEdges(selected);
        }
        return false;
    });
    //Bind keyboard shortcuts
    $(document).keyup(keyboardShortcuts);

    $('#reorderForm').submit(function () {
        var yes = confirm('This will reassign all bars based on the page image.  Continue?');
        if (!yes) {
            return false;
        } else {

        }

    });

    /*Openlayers Window*/
    //Set div width/height as proprortion of available screen
    var docWidth = parseInt($('body').width());
    var docHeight = parseInt($(window).height());
    var fullWidth = docWidth - Math.round(docWidth * .40);
    var fullHeight = docHeight - Math.round(docHeight * .30);

    $("#map").css('width', fullWidth + "px").css("height", fullHeight + "px")

    /* First we initialize the zoomify pyramid (to get number of tiers) */
    zoomify = new OpenLayers.Layer.Zoomify("Zoomify", zoomify_url,
        new OpenLayers.Size(zoomify_width, zoomify_height));
    /* Map with raster coordinates (pixels) from Zoomify image */
    var options = {
        controls:[],
        maxExtent:new OpenLayers.Bounds(0, 0, zoomify_width, zoomify_height),
        maxResolution:Math.pow(2, zoomify.numberOfTiers - 1),
        numZoomLevels:zoomify.numberOfTiers,
        units:'pixels'
    };

    map = new OpenLayers.Map("map", options);
    //vlayer = new OpenLayers.Layer.Vector("Editable")


    vlayer = new OpenLayers.Layer.Vector("Editable", {
        strategies:[new OpenLayers.Strategy.Fixed()],
        styleMap:new OpenLayers.StyleMap({'default':{
            strokeOpacity:1,
            strokeWidth:1,
            fillColor:"${fillColor}",
            fillOpacity:0.5,
            pointRadius:6,
            pointerEvents:"visiblePainted",
            // label with \n linebreaks
            label:"${label}",
            fontColor:"black",
            fontSize:"10px",
            fontFamily:"Courier New, monospace",
            fontWeight:"bold",
            labelAlign:"cm",
            labelOutlineColor:"white",
            labelOutlineWidth:3
        }}),
        protocol:new OpenLayers.Protocol.HTTP({
            url:regionURL,
            format:new OpenLayers.Format.GeoJSON()
        })
    });

    map.addLayers([zoomify, vlayer]);

    var mouse = new OpenLayers.Control.Navigation({'zoomWheelEnabled':false});

    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(mouse);
    //map.addControl(new OpenLayers.Control.KeyboardDefaults());
    //map.addControl(new OpenLayers.Control.EditingToolbar(vlayer));
    // map.addControl(new OpenLayers.Control.OverviewMap());

    /*Initialise toolbar*/

    var toolbarPanel = initControls(vlayer);

    map.addControl(toolbarPanel);
    map.zoomToMaxExtent();


});
