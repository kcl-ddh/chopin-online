DeleteFeature = OpenLayers.Class(OpenLayers.Control, {
    initialize: function(layer, options) {
        OpenLayers.Control.prototype.initialize.apply(this, [options]);
        this.layer = layer;
        this.handler =
                new OpenLayers.Handler.Feature(this,
                        layer, {click: this.clickFeature});
    },
    clickFeature: function(feature) {
        // if feature doesn't have a fid, destroy it
        if (feature.fid == undefined) {
            this.layer.destroyFeatures([feature]);
        } else {
            feature.state = OpenLayers.State.DELETE;
            this.layer.events.triggerEvent("afterfeaturemodified",
            {feature: feature});
            feature.renderIntent = "select";
            this.layer.drawFeature(feature);
        }
    },
    setMap: function(map) {
        this.handler.setMap(map);
        OpenLayers.Control.prototype.setMap.apply(this, arguments);
    },
    CLASS_NAME: "OpenLayers.Control.DeleteFeature"
});

updateRegionCoords = function(f, pixel) {
    var id = f.attributes.id;
    var bounds = (f.geometry.getBounds());
    var x = bounds.left;
    var y = bounds.top;
    var width = bounds.getWidth();
    var height = bounds.getHeight();
    //updateBarRegion('U', {regionid:id,x:x,y:y,width:width,height:height});

}

writeEndCoords = function(f, pixel) {
    var bounds = (f.geometry.getBounds());
    endX= bounds.left;
    endY = bounds.top;
    console.log ('end:'+endX+':'+endY);
};

writeStartCoords = function(f, pixel) {
    var bounds = (f.geometry.getBounds());
    startX= bounds.left;
    startY = bounds.top;
    console.log ('start:'+bounds.left+':'+bounds.top);
};

initControls=function(vlayer){
    var deleteFeature = new DeleteFeature(vlayer,
    {displayClass: "olControlDeleteFeature", title: 'Delete'});
    var rectangleFeature = new OpenLayers.Control.DrawFeature(vlayer,
            OpenLayers.Handler.RegularPolygon,

    {   featureAdded: function(e) {
        x = x + 1;
        var newNote = $('#blankNoteForm').clone();
        $(newNote).show();
        $(newNote).attr('id', 'noteForm_' + x);
        $(e).attr('id', 'newNote_' + x);

        $(newNote).appendTo('#annotations');
    },
        handlerOptions: {sides: 4,
            irregular: true},
        title: "Draw Rectangle",
        displayClass: "olControlDrawFeaturePolygon"});


    var rectangleFeature = new OpenLayers.Control.DrawFeature(vlayer,
            OpenLayers.Handler.RegularPolygon,

    {   featureAdded: function(e) {
        x = x + 1;
        var newNote = $('#blankNoteForm').clone();
        $(newNote).show();
        $(newNote).attr('id', 'noteForm_' + x);
        $(e).attr('id', 'newNote_' + x);

        $(newNote).appendTo('#annotations');
    },
        handlerOptions: {sides: 4,
            irregular: true},
        title: "Draw Rectangle",
        displayClass: "olControlDrawFeaturePolygon"});
    var polygonFeature = new OpenLayers.Control.DrawFeature(vlayer,
            OpenLayers.Handler.Polygon,
    {displayClass: "olControlDrawFeaturePolygon",
        title: "Draw Polygon"});

    var selectFeature = new OpenLayers.Control.SelectFeature(vlayer,
    {title: 'Select', clickout: true, toggle: false,
        displayClass: "olControlSelectFeature",
        multiple: false, hover: false,
        toggleKey: "ctrlKey", // ctrl key removes from selection
        multipleKey: "shiftKey", // shift key adds to selection
        box: true,onSelect:writeStartCoords});

    var dragFeature = new OpenLayers.Control.DragFeature(vlayer,
    {displayClass: "olControlDragFeature", title: 'Drag',onComplete:writeEndCoords});

    var modifyFeature = new OpenLayers.Control.ModifyFeature(vlayer,
    {mode: OpenLayers.Control.ModifyFeature.RESIZE |
            OpenLayers.Control.ModifyFeature.ROTATE,
        displayClass: "olControlNavigation",
        title: 'Modify'});

    var saveButton = new OpenLayers.Control.Button({
        title: 'Save',
        trigger: function() {
            if (modifyFeature.feature) {
                modifyFeature.selectControl.unselectAll();
            }
            var offsetX=endX-startX;
            var offsetY=startY-endY;
            $.post('/ocve/correctCropping/',{pageID:pageID,offsetX:offsetX,offsetY:offsetY},function(){
            alert('Correction saved');
            });
        },
        displayClass: 'olControlSaveFeatures'
    });
    var panelControls=[saveButton,
        dragFeature,
            selectFeature
    ];
    var toolbarPanel = new OpenLayers.Control.Panel(
    {displayClass: "olControlEditingToolbar",defaultControl: panelControls[2]});
    toolbarPanel.addControls(panelControls);
    return toolbarPanel;
};

window.onload = function() {
    /* First we initialize the zoomify pyramid (to get number of tiers) */
    var zoomify = new OpenLayers.Layer.Zoomify("Zoomify", zoomify_url,
            new OpenLayers.Size(zoomify_width, zoomify_height));

    /* Map with raster coordinates (pixels) from Zoomify image */
    var options = {
        controls: [],
        maxExtent: new OpenLayers.Bounds(0, 0, zoomify_width, zoomify_height),
        maxResolution: Math.pow(2, zoomify.numberOfTiers - 1),
        numZoomLevels: zoomify.numberOfTiers,
        units: 'pixels'
    };

    var docWidth = parseInt($('body').width());
    var docHeight = parseInt($(window).height());
    var fullWidth = docWidth - Math.round(docWidth * .40);
    var fullHeight = docHeight - Math.round(docHeight * .30);

    $("#map").css('width',fullWidth+"px").css("height",fullHeight+"px")

    map = new OpenLayers.Map("map", options);
    //vlayer = new OpenLayers.Layer.Vector("Editable")
    vlayer = new OpenLayers.Layer.Vector("Editable",{
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url: regionURL,
            format: new OpenLayers.Format.GeoJSON()
         })
    });

    map.addLayers([zoomify, vlayer]);
    var mouse=new OpenLayers.Control.Navigation({'zoomWheelEnabled': false});
    //mouse.disableZoomWheel();
    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(mouse);
    map.addControl(new OpenLayers.Control.KeyboardDefaults());



    /*Initialise toolbar*/

    var toolbarPanel=initControls(vlayer);

    map.addControl(toolbarPanel);
    map.zoomToMaxExtent();

};
