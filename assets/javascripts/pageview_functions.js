$(document).ready(function () {
    //Annotation functions
    //Show/hide for openlayers annotation controls
    aselector = '#annotations';
    allNotesVisible = false;

    // Opens a new annotation window for drawn feature
    newDrawnAnnotation = function (feature) {
        var noteid = 0;

        if ($('#annotation_id').val() > 0) {
            noteid = $('#annotation_id').val();
        }

        feature.attributes = {'noteid': noteid};
        feature.renderIntent = 'visibleNote';

        $('#id_noteregions').val(feature.geometry.toString());
        $('#featureid').val(feature.id);

        showNewAnnotationWindow();
        alayer.redraw();
    }

    showNewAnnotationWindow = function () {
        $('#newNote').fadeIn();
        $('#notes').hide();
        $('#commentary').hide()
    };

    initSquareAnnotation = function () {
        squareFeature.activate();
        hideExistingNotes();
        showNewAnnotationWindow();
    }

    initCircleAnnotation = function () {
        circleFeature.activate();
        hideExistingNotes();
        showNewAnnotationWindow();
    }

    initBarSelect = function () {
        toggleBarBoxes();
        hideExistingNotes();
        showNewAnnotationWindow();
    }

    hideNewAnnotationWindow = function () {
        $('#newNote').fadeOut();
        $('#notes').show();
        $('#commentary').show();
    };

    //Write a note
    writeNote = function (noteForm) {
        var newNotes = "<div id=\"comment-" + noteid + "\" class=\"annotation-box\">"
        newNotes += "<p class=\"annotation-details\">";
    }

    //Remove any notes drawn but not saved
    deleteOrphanAnnotations = function () {
        for (var f in alayer.features) {
            if (alayer.features[f].attributes.noteid == 0) {
                alayer.removeFeatures(alayer.features[f])
            }
        }
        alayer.redraw();
    }

    //Deactivate all annotation functions
    resetPage = function () {
        selectControl.unselectAll()
        noteSelectFeature.unselectAll();
        circleFeature.deactivate();
        squareFeature.deactivate();
        barSelectFeature.deactivate();
        noteSelectFeature.deactivate();
        deleteOrphanAnnotations();
        hideAnnotationTools();
        hideNewAnnotationWindow();
    }

    updateUserNote = function (note, notetext) {
        $(note).child('div.annotation p').html(notetext);
    }

    saveNote = function () {
        //Are bars in the bar layer selected?
        var barString = "";

        if (vlayer.selectedFeatures.length > 0) {
            for (var v in vlayer.selectedFeatures) {
                //Serialize
                if (barString.length > 0) {
                    barString += ",";
                }
                barString += vlayer.selectedFeatures[v].attributes.barid;
            }
        }

        if (alayer.selectedFeatures.length > 0) {
            for (var a in alayer.selectedFeatures) {
                //Serialize
                if (barString.length > 0) {
                    barString += ",";
                }
                barString += alayer.selectedFeatures[a].attributes.barid;
            }
        }

        //Add to form
        $('#noteBars').val(barString);

        //Validate
        if ($('#noteBars').val().length == 0
            && $('#id_noteregions').val().length == 0) {
            //No regions or bars select
            alert('Please attach a bar or draw a shape for your note');
            return false;
        }

        if ($('#id_notetext').val().length == 0) {
            //No Annotation text
            alert('No text written for annotation');
            return false;
        }

        //Submit the lot
        var noteData = $("#newNoteForm").serialize();

        $.post('/ocve/saveNote/', noteData, function(data) {
            //Add/update with new note
            var noteid = data.noteid;
            // update alayer
            var newFeatures = [];

            for (var v in vlayer.selectedFeatures) {
                //Clone bar regions with note attributes
                //Note Attributes
                var noteAttributes = {"noteid": noteid};
                var newF = OpenLayers.Feature.Vector(
                    noteAttributes, vlayer.selectedFeatures[v].geometry);
                newFeatures.push(newF);
            }

            if ($('#comment-' + noteid).length > 0) {
                $('#comment-' + noteid).replaceWith(data.notehtml);
            } else {
                // update user notes
                $('#notes div.collapseme').append(data.notehtml);
            }

            // Clear and hide new note form
            hideNewAnnotationWindow();

            $('#id_notetext').val('');
            $('#id_noteBars').val('');
            $('#id_noteregions').val('');

            $('#messages').html(data.messages);
        }, "json");
    }

    initAnnotationPanel = function (alayer) {
        squareFeature = new OpenLayers.Control.DrawFeature(
            alayer, OpenLayers.Handler.RegularPolygon,
            {displayClass: "olControlDrawFeaturePolygon",
                title: "Draw Custom Annotation",
                featureAdded: newDrawnAnnotation
            });

        circleFeature = new OpenLayers.Control.DrawFeature(
            alayer,
            OpenLayers.Handler.RegularPolygon,
            {displayClass: "olControlDrawFeaturePolygon",
                title: "Draw Custom Annotation",
                featureAdded: newDrawnAnnotation
            });
            circleFeature.handler.sides = 40;

        barSelectFeature = new OpenLayers.Control.SelectFeature(
            vlayer,
            {
                title: 'Select',
                clickout: true,
                toggle: false,
                displayClass: "olControlModifyFeature",
                multiple: true,
                hover: false,
                toggleKey: "ctrlKey", // ctrl key removes from selection
                multipleKey: "shiftKey", // shift key adds to selection
                onSelect: showNewAnnotationWindow,
                box: true
            });

        noteSelectFeature = new OpenLayers.Control.SelectFeature(
            alayer,
            {title: 'Select', clickout: true, toggle: false,
                displayClass: "olControlDrawFeaturePolygon",
                multiple: true, hover: false,
                toggleKey: "ctrlKey", // ctrl key removes from selection
                multipleKey: "shiftKey", // shift key adds to selection
                renderIntent: "selectedNote",
                box: true
            });

        var panelControls = [barSelectFeature, squareFeature, circleFeature, noteSelectFeature];
        toolbarPanel = new OpenLayers.Control.Panel(
            {displayClass: "olControlEditingToolbar"});
            toolbarPanel.addControls(panelControls);

        //Connect bar labels to features with hover highlight
        $('.noteBarHighlight').hover(function () {
            noteSelectFeature.unselectAll();
            var select = alayer.getFeaturesByAttribute(
                'barid', $(this).find('span').data('barid'));
            if (select.length > 0) {
                noteSelectFeature.select(select[0]);
            }
        }, function () {
            //visibleNote
            noteSelectFeature.unselectAll();
            var select = alayer.getFeaturesByAttribute(
                'barid', $(this).find('span').data('barid'))[0];
            select.renderIntent = "visibleNote";
            alayer.redraw();
        });

        $('.noteRegionHighlight').hover(function () {
            noteSelectFeature.unselectAll();
            var select = alayer.getFeaturesByAttribute(
                'noteid', $(this).data('noteid'));
            if (select.length > 0) {
                noteSelectFeature.select(select[0]);
            }
        }, function () {
            noteSelectFeature.unselectAll();
            var select = alayer.getFeaturesByAttribute(
                'noteid', $(this).data('noteid'));
            if (select.length > 0) {
                select[0].renderIntent = "visibleNote";
                alayer.redraw();
            }
        });

        //Update/Delete controls for any notes on page created by current user
        $('a.updateNote').click(function () {
            var noteid = $(this).data('noteid');
            nTest=noteid;
            var oldText = $('#comment-' + noteid + ' div.annotation p').html();
            $('#id_notetext').val(oldText);
            $('#annotation_id').val(noteid);
            //Select current notes/regions
            curFeatures = alayer.getFeaturesByAttribute('noteid', noteid);
            for (var c=0; c< curFeatures.length;c++) {
                console.log(curFeatures[c].layer);
                curFeatures[c].renderIntent = 'visibleNote' ;
                noteSelectFeature.select(curFeatures[c]);
            }
            alayer.redraw();
            showNewAnnotationWindow();

        });

        $('a.deleteNote').click(function() {
            var sure = confirm('Delete This Note?');

            if (sure == true) {
                var noteid = $(this).data('noteid');

                $.post('/ocve/deleteNote/' + noteid, function(data) {
                    $('#comment-' + noteid).fadeOut();
                    $('#messages').html(data.messages);
                }, 'json');
            }

            return false;
        });
    }

    hideExistingNotes = function () {
        for (var f in alayer.features) {
            if (alayer.features[f].attributes.noteid > 0) {
                alayer.features[f].renderIntent = "default";
            }
        }
        alayer.redraw();
    }

    toggleExistingNotes = function (noteType) {
        for (var f in alayer.features) {
            if (alayer.features[f].attributes.noteid > 0) {
                if (noteType=='all'
                    || (noteType == 'notes'
                        && alayer.features[f].data.noteType != 2)
                    || (noteType == 'commentary'
                        && alayer.features[f].data.noteType == 2))
                    if (alayer.features[f].renderIntent == "default") {
                        allNotesVisible = true;
                        alayer.features[f].renderIntent = "visibleNote";
                } else {
                    allNotesVisible = false;
                    alayer.features[f].renderIntent = "default";
                }
            }
        }
        alayer.redraw();
    }

    showAnnotationTools = function () {
        //Replace bar styles
        vlayer.styleMap.styles["default"] = vlayer.styleMap.styles["annotation"]
        vlayer.setVisibility(false);
        map.addControl(toolbarPanel);
    }

    hideAnnotationTools = function () {
        //Restore bar styles
        vlayer.styleMap.styles["default"] = vlayer.styleMap.styles["barSelector"]
        vlayer.redraw();
        vlayer.setVisibility(true);
        map.removeControl(toolbarPanel);
    }

    hideAnnotations = function () {
        $(aselector).fadeOut();
    }

    //Bar boxes on/off
    toggleBarBoxes = function () {
        if (vlayer.visibility) {
            vlayer.setVisibility(false)
        } else {
            vlayer.setVisibility(true)
        }
        vlayer.redraw();
    }

    toggleBarNumbers = function () {
        if (vlayer.styleMap.styles.default.defaultStyle.label.length > 0) {
            vlayer.styleMap.styles.default.defaultStyle.label = '';
        } else {
            vlayer.styleMap.styles.default.defaultStyle.label = "${label}"
        }
        vlayer.redraw();
    }

    //To run in doc ready to init all annotation events

    annotationEvents = function () {
        //Init state
        $('#newNote').hide();

        $('#barAttachToggle').click(function () {
            toggleBarBoxes();
            hideExistingNotes();
            barSelectFeature.activate();

            return false;
        });

        $('#newCircleNoteToggle').click(function () {
            initCircleAnnotation();
            return false;
        });

        $('#newSquareNoteToggle').click(function () {
            initSquareAnnotation();
            return false;
        });

        initAnnotationPanel(alayer);

        $('#newNoteForm').submit(function (event) {
            event.preventDefault();
        });

        $('#createNote').click(function () {
            saveNote();
        });

        $('#cancelNote').click(function () {
            resetPage();
            toggleBarBoxes();
            return false;
        });
    }
});
