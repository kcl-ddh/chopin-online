/* 
 * Bar View Javascript Support
 */

//Add bar region to collection
/*

 */

 /**
 * Gets a cookie. Mmmmmmmmm cookies!
 */
function cookie_get(name)
{
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++)
    {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == name)
        {
            return unescape(y);
        }
    }
}

/**
 * Sets a cookie! Put that cookie down!
 */
function cookie_set(name, value, valid_days)
{
    var expiry = new Date();
    if (valid_days == null)
    {
        expiry.setDate(expiry.getDate() + valid_days);
    } else
    {
        expiry.setDate(expiry.getDate() + 365);
    }
    var value = escape(value) + "; expires=" + expiry.toUTCString();
    document.cookie = name + "=" + value + "; path=/";
}


addCollection = function(button){
    B=button;
    var id=$(button).data('region-id');
    var thumbnailURL=$(button).data('thumbnail');
    $("<li data-region-id=\""+id+"\" class='collection-thumbnail'><input type=\"hidden\" name=\"regionID\" value=\""+id+"\"/><a class=\"th radius added\" href=\"annotate.html\"><img src=\""+thumbnailURL+"\" alt=\"\" class=\"thumbnail\"></a></li>").insertBefore("#clearCollection")
}

//Remove bar region from collection
removeCollection = function(id){
    $("li[data-region-id="+id+"]").remove();
}

//Commit Collection
saveCollection = function(){

}

//Load previous collections
loadCollection = function(){

}

function initBarView()
{// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
    $(document).foundation();
	if($(".bar-images").length)
	{
	
		// This restores draggable regions in the bar view:
		if(typeof(Storage) !== "undefined") {
			$(".barList>li").each(function()
			{
				var r_id = $(this).attr("id");
				
				if(localStorage.getItem(r_id + "top") !== null)
				{
					$(this).css("top", localStorage.getItem(r_id + "top"));
					$(this).css("left", localStorage.getItem(r_id + "left"));
					$(this).css("z-index", localStorage.getItem(r_id + "z-index"));
					if(localStorage.getItem(r_id + "display") == "none")
					{
						$("input.sourceFilter[value='" + $(this).find(".closeSource").attr("data-source-id") + "']").prop("checked", false);
						$(".toggle-all input[type='checkbox']").prop("checked", false);
						$(this).hide();
					}
				}
												
			});
		}
		
		// Source List 
	    $('.sourceFilter').click(function(){
	        $('.source'+$(this).val()).toggle("normal", function()
	       	{
	       	// Persistence!
	       	
		       	if(typeof(Storage) !== "undefined") {
		       		$(".barList>li").each(function()
		       		{
		       			var r_id = $(this).attr("id");
		       			localStorage.setItem(r_id + "top", $(this).css("top"));
		       			localStorage.setItem(r_id + "left", $(this).css("left"));
		       			localStorage.setItem(r_id + "z-index", $(this).css("z-index"));  
		       			localStorage.setItem(r_id + "display", $(this).css("display"));
		       		});
		       	}
		      });
		      $("#available-sources .toggle-all input").prop("checked", $("input.sourceFilter:checkbox:checked").length == $("input.sourceFilter:checkbox").length);
	
	    });
	    
	    
    //  Makes images NAIVELY draggable
    $('.barList>li').draggable({
    	stack: "li",
    	stop: function()
    	{
    		// Persistence - using local storage rather than cookies
    		// there's no point sending this stuff to the server ;).
    		
    		if(typeof(Storage) !== "undefined") {
    			$(".barList>li").each(function()
    			{
    				var r_id = $(this).attr("id");
    				localStorage.setItem(r_id + "top", $(this).css("top"));
    				localStorage.setItem(r_id + "left", $(this).css("left"));
    				localStorage.setItem(r_id + "z-index", $(this).css("z-index"));  
    				localStorage.setItem(r_id + "display", $(this).css("display"));
    			});
    		}
    	},
   	});
	
	
		// Add button - we want to do more than the default foundation controls
		// allow because of ajax ;).
		
		$("body").on("click", ".barList .add-btn", function(event)
		{
			event.preventDefault();
			event.stopPropagation();
			
			if($(".collections-inline").is(":visible"))
			{
				$(".collections-inline").hide("slide", { direction: "down" }, 500);
				$(".bar-images").css({"margin-bottom" : "0px"});
			}
			
			$("#add-image-to-collection-modal").attr("data-region-id", $(this).attr("data-region-id"));
		
			$.get("/ocve/ajax/add-image-to-collection-modal/", function( data ) {
				$("#add-image-to-collection-modal").html(data);
				$("#add-image-to-collection-modal").foundation('reveal', 'open');
			});
		});
		
	
		
		// Searching within bar chooser:
		// TODO - autofocus on show - BM
		// TODO - up/down arrow/enter to navigate/select list - BM
		$("body").on("keyup", ".list-search", function (event) {
	        var objects = $("ul#"+ $(this).attr("data-list-id")).children("li");
	        if (event.keyCode == 27) {
	            $(this).val("");
	        }
	
	        if ($.trim($(this).val()) == "") {
	            $(objects).show();
	        } else {
	            for (var i = 0; i < objects.length; i++) {
	
	                if ($(objects[i]).text().toLowerCase().indexOf($(this).val().toLowerCase()) !== -1) {
	                    $(objects[i]).show();
	                } else {
	                    $(objects[i]).hide();
	                }
	            }
	        }
	    });
	    
	   
	   // Allows the user to reset current the bar view
	   $("body").on("click",".bar-view-reset-btn", function(event)
	   {
	   	event.preventDefault();
	   	if(typeof(Storage) !== "undefined") {
	   		$(".barList>li").each(function()
	   		{
	   			var r_id = $(this).attr("id");
	   			localStorage.removeItem(r_id + "top");
	   			localStorage.removeItem(r_id + "left");
	   			localStorage.removeItem(r_id + "z-index"); 	
	   			localStorage.removeItem(r_id + "display"); 	
	   			
	   			
	   			$(this).css("top", "auto");
	   			$(this).css("left", "auto");
	   			$(this).css("z-index", "auto");			
	   		});
	   		
				if(!$(".toggle-all input[type='checkbox']").prop("checked"))	   	
				{
					$(".toggle-all input[type='checkbox']").click();
				}	
	   		
	   	}
	   });
	    
	    // UI tweak - changes live search placeholder on focus
		$("body").on("focus", ".list-search", function (event) {
			$(this).attr("placeholder", "Type to search...");
		}).on("blur", ".list-search", function (event) {
			$(this).attr("placeholder", "Click to search...");
		});
	    
	    
	    // Enables "Select All" toggle
	    $("#available-sources .toggle-all input").on("click", function(event)
	    {
				if(!$(this).prop('checked'))
				{
					$("input.sourceFilter").each(function(event_inner)
					{
						if($(this).prop('checked'))
						{
							$(this).click(); // doing this calls the click event!
						}
					});
				} else
				{
					$("input.sourceFilter").each(function(event_inner)
					{
						if(!$(this).prop('checked'))
						{
							$(this).click(); // doing this calls the click event!
						}
					});
				}
	    });
	    
	    
	    // Enables image zooming
	    $("body").on("click", ".large-image-button", function(event)
	    {
            var img=$("#large-image-img");
	    	$(img).attr("src", $(this).attr("data-img"));
            $(this).attr("data-img")
            var regionid=$(this).attr("data-region_id");
            var regionlabel=$(this).attr("data-region-label");
            $("#large-image div.row div span").html(regionlabel);
            $.post('/ocve/browse/getAnnotations/'+regionid+'/',function(data){
               if (data.length > 0){
                   $("#large-image div.row div.large-12.columns").attr('class','large-8 columns');
                   $("#large-image div.row div.large-4.columns").show();
               }else{
                   $("#large-image div.row div.large-8.columns").attr('class','large-12 columns');
                   $("#large-image div.row div.large-4.columns").hide();
               }
               $('#modal-annotations').empty().html(data);

            })
	    });


	    // Enables the close source button
	    $("body").on("click", ".closeSource", function(event)
	    {
	    	$(".sourceFilter[value='" + $(this).attr("data-source-id") + "']").click();
		});
		
		
		
		
	}
}

/**
 * CFEO add to collection 
 */
 function initCFEOComparison()
 {
 	$("body").on("click", ".cfeo-add-to-compare", function(event)
 	{
 		event.preventDefault();
 		event.stopPropagation();

 		// hide notification and show the L/R bar
 		$(".add-to-compare-notification").hide();
 		$(".add-to-compare-bar").fadeIn();
 	});

 	$("body").on("click", ".add-to-compare-bar a", function(event)
 	{
 		event.preventDefault();
 		event.stopPropagation();

 		// Set the page ID into the respective cookie. Cookie_set name, val, days
 		cookie_set("cfeo_compare_" + $(this).attr("data-cookie"), $(this).attr("data-page-id"), 365);
 		$(".add-to-compare-bar").hide();
 		$(".add-to-compare-notification").fadeIn();

 	});
 }


/**
 *
 * OCVE page view
 *
 */
function initOCVEPageView()
{
$(document).foundation();


}
/**
 *
 * CFEO page view
 *
 */
function initCFEOPageView()
{

}

/**
 * Inline collections support 
 */
function initInlineCollections()
{

	// Fetches collections via ajax and opens the window
	$("body").on("click", ".open-collections-inline", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		if(!$(".collections-inline").is(":visible"))
		{
			$.get("/ocve/ajax/inline-collections/", function( data ) {
				$(".collections-inline .inner").html(data);
				$(".collections-inline").show("slide", { direction: "down" }, 500);
			});
			
			$(".bar-images").css({"margin-bottom" : 220 - $(".footer").height() + "px"});
		} else {
			$(".collections-inline").hide("slide", { direction: "down" }, 500);
			$(".bar-images").css({"margin-bottom" : "0px"});
		}
		
	});
	

	// Fetches collections via ajax and opens the window on a specific collection
	$("body").on("click", ".auto-switch-collection", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		var collectionID = $(this).attr("data-collection-id");
		if(!$(".collections-inline").is(":visible"))
		{
			$.get("/ocve/ajax/inline-collections/", function( data ) {
				$(".collections-inline .inner").html(data);
				$('.collection-inline-switcher').val(collectionID).trigger('change');
				$(".collections-inline").show("slide", { direction: "down" }, 500);
			});
			
			$(".bar-images").css({"margin-bottom" : 220 - $(".footer").height() + "px"});
		} else {
			$('.collection-inline-switcher').val(collectionID).trigger('change');

		}
		
	});
	
	
	// Closes the collections window.
	$("body").on("click", ".close-collections-inline", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		if($(".collections-inline").is(":visible"))
		{
			$(".collections-inline").hide("slide", { direction: "down" }, 500);
			$(".bar-images").css({"margin-bottom" : "0px"});
		}
	});
	
	// Enables the edit collection button
	$("body").on("click", ".collection-meta .edit", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var collection_id=$(".collection-inline-switcher").find(":selected").attr('data-collection-id');
		var collection_name=$(".collection-inline-switcher").find(":selected").text();
		
		$("<div class='edit-collection-form'><input class='edit-collection-name' type='text' data-collection-id='" + collection_id + "' value='" + collection_name + "'><a href='#' class='save'><i class='fa fa-check-circle'></i></a><a href='#' class='cancel'><i class='fa fa-times-circle'></i></a></div>").insertAfter(	$(".collection-inline-switcher"));
		
		$(".collection-inline-switcher").hide();
		$(".collection-control").hide();
		$(".edit-collection-name").focus();
	});
	
	// Enables the cancel edit collection button
	$("body").on("click", ".edit-collection-form .cancel", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		$(".edit-collection-form").remove();
		$(".collection-inline-switcher").show();
		$(".collection-control").show();
		
	});
	
	// Enables the cancel add collection cancel button
	$("body").on("click", ".add-collection-inline-form .cancel", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		$(".add-collection-inline-form").remove();
		$(".collection-inline-switcher").show();
		$(".collection-control").show();
	});
	
	// Enables the edit collection button
	$("body").on("click", ".edit-collection-form .save", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var name = $(".edit-collection-form .edit-collection-name").val();
		var collection_id = $(".edit-collection-form .edit-collection-name").attr("data-collection-id");
		if(name.trim() !== "")
		{
			$.post( "/ocve/ajax/change-collection-name/", 
				{
					collection_id: collection_id,
					new_collection_name: name
				},
				function( data ) {
			  	if(data == "1")
			  	{
			  		// success
			  		$(".collection-inline-switcher option[data-collection-id='" + collection_id + "']").text($(".edit-collection-form .edit-collection-name").val());
			  		
			  		$(".collection-viewer[data-collection-id='" + collection_id + "'] .title").text($(".edit-collection-form .edit-collection-name").val());
			  		$(".edit-collection-form").remove();
			  		$(".collection-inline-switcher").show();
			  		$(".collection-control").show();
			  		
			  		
			  		
			  	} else {
			  		//fail - this should be a nice notification
			  		alert("Unable to change name.");
			  	}
			});
		} else {
			//fail - this should be a nice notification
			alert("New name is needed.");
		}
	});
	
	// Enables the add collection save button
	$("body").on("click", ".add-collection-inline-form .save", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var name = $(".add-collection-inline-form .collection-name").val();
		
		if(name.trim() !== "")
		{
			/**
			 * Note: Ajax status = new collection id. 0 if not added.
			 */
			$.post( "/ocve/ajax/add-collection/", 
				{
					new_collection_name: name
				},
				function( data ) {
			  	if(data !== "0")
			  	{
			  		// success
			  		
			  		var newoption = $('<option data-collection-id="' + data + '">' + $(".add-collection-inline-form .collection-name").val() + '</option>');
			  		$(".collection-inline-switcher").append(newoption);
			  		
			  		$(".collection-inline-switcher option[data-collection-id='" + data + "']").prop("selected", true); 
			  		$(".collection-inline-switcher option[data-collection-id='null']").remove();
			  		
			  		
			  		$(".add-collection-inline-form").remove();
			  		$(".collection-inline-switcher").show();
			  		$(".collection-control").show();
			  		
			  	} else {
			  		//fail - this should be a nice notification
			  		alert("Unable to add collection.");
			  	}
			});
		} else {
			//fail - this should be a nice notification
			alert("Collection name needed.");
		}
	});
	
	// Enables the delete collection button
	$("body").on("click", ".collection-meta .delete", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var collection_id=$(".collection-inline-switcher").find(":selected").attr('data-collection-id');
		var collection_name=$(".collection-inline-switcher").find(":selected").text();
		
		$(".collections-inline .collection-delete-alert .delete-collection-name").text(collection_name);
		$(".collections-inline .collection-delete-alert .confirm").attr("data-collection-id", collection_id);
		$(".collections-inline .collection-delete-alert").fadeIn();		
		
		$(".collection-inline-switcher").hide();
		$(".collection-control").hide();
	});
	
	// Enables the delete collection cancel button
	$("body").on("click", ".collections-inline .collection-delete-alert .cancel", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
			
		$(".collections-inline .collection-delete-alert").hide();		
		
		$(".collection-inline-switcher").show();
		$(".collection-control").show();
	});
		
	// enables the delete collection confirm button
	$("body").on("click", ".collections-inline .collection-delete-alert .confirm", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
			
		var collection_id = $(this).attr("data-collection-id");
		
		$.post( "/ocve/ajax/delete-collection/", 
			{
				collection_id: collection_id,
			},
			function( data ) {
		  	if(data == "1")
		  	{
					// Collection deleted, reload the panel:
					$.get("/ocve/ajax/inline-collections/", function( data ) {
						$(".collections-inline .inner").html(data);
					});
							  		
		  		
		  	} else {
		  		//fail - this should be a nice notification
		  		alert("Unable to delete collection - an error occured.");
		  	}
		});
			
	});
	
	
	// Enables the add collection  button in modal
	$("body").on("click", ".add-new-collection-form .submit", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var name = $(".add-new-collection-form .collection-name").val();
		
		if(name.trim() !== "")
		{
			/**
			 * Note: Ajax status = new collection id. 0 if not added.
			 */
			$.post( "/ocve/ajax/add-collection/", 
				{
					new_collection_name: name
				},
				function( data ) {
			  	if(data !== "0")
			  	{
			  		// success
			  		
			  		var newoption = $('<option data-collection-id="' + data + '">' + $(".add-new-collection-form .collection-name").val() + '</option>');
			  		
			  		var newoption2 =  $('<option data-collection-id="' + data + '">' + $(".add-new-collection-form .collection-name").val() + '</option>');
			  	
			  		$(".collection-inline-switcher").append(newoption);
			  		$(".collection-inline-switcher option[data-collection-id='" + data + "']").prop("selected", true); 
			  		$(".collection-inline-switcher option[data-collection-id='null']").remove();
			  		
			  		$(".add-to-collection-select").append(newoption2);
			  		$(".add-to-collection-select option[data-collection-id='" + data + "']").prop("selected", true); 
			  		$(".add-to-collection-select option[data-collection-id='null']").remove();
			  		
			  		$(".add-new-collection-form .collection-name").val("")
			  		
			  		$(".success, .error").hide();
			  		$(".success").text("Collection added, you may now add to it.").fadeIn();
			  	} else {
			  		//fail - this should be a nice notification
			  		$(".success, .error").hide();
			  		$(".error").text("Error: Unable to add new collection.").fadeIn();
			  	}
			});
		} else {
			//fail - this should be a nice notification
			$(".success, .error").hide();
			$(".error").text("Enter a collection name.").fadeIn();
		}
	});
	
	
	// Enables the inline add-collection form:
	$("body").on("click", ".add-collection-inline", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		$("<div class='add-collection-inline-form'><input class='collection-name' type='text' placeholder='Collection Name'><a href='#' class='save'><i class='fa fa-plus-circle'></i></a><a href='#' class='cancel'><i class='fa fa-times-circle'></i></a></div>").insertAfter(	$(".collection-inline-switcher"));
		
		$(".collection-inline-switcher").hide();
		$(".collection-control").hide();
	});
	
	
	// Enables the collection switcher
	$("body").on("change", ".collection-inline-switcher", function(event)
	{
		var collection_id = $(this).find(":selected").attr('data-collection-id');
		
		$(".collection-viewer").hide();
		$(".collection-viewer[data-collection-id='" + collection_id + "']").show();
		
	});
	
	
	// lets us add an image to a collection:
	$("body").on("click", ".add-to-collection-btn", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var region_id = $("#add-image-to-collection-modal").attr("data-region-id");
		var collection_id = $(".add-to-collection-select").find(":selected").attr('data-collection-id');
		$.post( "/ocve/ajax/add-image-to-collection/", 
			{
				collection_id: collection_id,
				region_id: region_id
			},
			function( data ) {
				/**
				 * 0 = error
				 * 1 = success
				 * 2 = not added because it already exists
				 */
				 
				 
				if(data == "0")
				{
					// error - should be presented nicely
		  		$(".success, .error").hide();
					$(".error").text("Error: Unable to add to collection.").fadeIn();
				} else if(data == "1")
		  	{
		  		// success - should be presented nicely
		  		$(".success, .error").hide();
		  		$(".success").text("Added to collection.").fadeIn();			  		
		  		
		  	} else if(data == "2")
		  	{
		  		$(".success, .error").hide();
		  		$(".error").text("Error: Already in collection.").fadeIn();
		  	}
		});
				
	});
	
	
	
	// lets us remove an image from a collection:
	// Todo - does this need a prompt?
	$("body").on("click", ".removeFromCollection a", function(event)
	{
		event.preventDefault();
		event.stopPropagation();
		
		var region_id = $(this).attr("data-region-id");
		var collection_id = $(this).attr('data-collection-id');
		
		$.post( "/ocve/ajax/delete-image-from-collection/", 
			{
				collection_id: collection_id,
				region_id: region_id
			},
			function( data ) {
				/**
				 * 0 = error
				 * 1 = success
				 */
				
			
				if(data == "1")
		  	{
		  		$(".collection-viewer[data-collection-id='" + collection_id + "']").find("li[data-region-id='" + region_id + "']").remove();
		  		
		  		if($(".collection-viewer[data-collection-id='" + collection_id + "'] .collection-thumbs").find("li").length == 0)
		  		{
		  			$(".collection-viewer[data-collection-id='" + collection_id + "'] .collection-thumbs").html("<p>There are no images in this collection (yet).</p>");
		  		}
		  		
		  	}
		  	
		 });
		  	
	});
}

/* function resizeModal(winHeight) {
	$('.reveal-modal').css('max-height', winHeight - 110 + 'px'); // 100 +10px to keep modal effect visible
	$('.reveal-modal > img').css("display","block").css('max-height', winHeight  - 200 + 'px');
} */

/* Expandable lists */
function expandableList() {
	// expandable lists
	var collapsedClass = "fa fa-caret-right";
	var expandedClass = "fa fa-caret-down";
    $("section[data-section='expandable'] .list-header a.ctrl").click(function () {
		if ( $(this).attr("data-collapsed-text") ) {
			collapsedText = $(this).attr("data-collapsed-text");
		} else {
			collapsedText = '';
		}
		if ( $(this).attr("data-expanded-text") ) {
			expandedText = $(this).attr("data-expanded-text");
		} else {
			expandedText = '';
		}
        if ($(this).hasClass("expand")) {
            $(this).parent().parent().parent().find(".list-content").slideDown(400, function () {
                // finished
            });
            $(this).removeClass("expand").addClass("collapse");
            $(this).find("i").removeClass(collapsedClass).addClass(expandedClass);
			if ( expandedText !='') {
				$(this).find(".ctrl-link-title").text(expandedText);
			}
        } else if ($(this).hasClass("collapse")) {
            $(this).parent().parent().parent().find(".list-content").slideUp();
            $(this).removeClass("collapse").addClass("expand");
            $(this).find("i").removeClass(expandedClass).addClass(collapsedClass);
			if ( collapsedText !='') {
				$(this).find(".ctrl-link-title").text(collapsedText);
			}
        }

        return false;
    });
	// end expandable lists
}



/* End added */


/* Faceted browsing functions */
/* Update browse results */
function updateBrowseResults() {
	$("#loading").addClass("spinner-active");
	$("#results-section").addClass("overlay-active");
	setTimeout(function() { 
		$("#results-section").removeClass("overlay-active"); 
		$("#loading").removeClass("spinner-active");
	 }, 500);
	 $("#no-filters").css("display","none");
	
}

// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
/* $(document).foundation();

$(window).resize(function() {
	winHeight = $(window).height();
	resizeModal( winHeight );
}); */

$(document).ready( function() {
	
	// Note: initBarView handles the check to see if the hooks
	// within it should be called (BM)
	initBarView();

	initOCVEPageView();

	// Inits the "add to comparison" functionality in CFEO (BM)
	initCFEOComparison();
	
	// This enables inline collection.
	initInlineCollections();
	
	expandableList();
	// faceted navigation
	$("section[data-expandable-group-member='facets'] .ctrl.select").click( function() {
		updateBrowseResults();
	});
	// remove facet
	$(".selected-filter .ctrl.remove").click( function() {
		$(this).parent().parent().remove();
		updateBrowseResults();
	});
	// remove all facets
	$(".filters-header").click( function() {
		$(".selected-filter").remove();
		updateBrowseResults();
		$("#no-filters").css("display","block");
	});
	
	/* Modal fix: https://github.com/zurb/foundation/issues/2971 */
	/* winHeight = $(window).height();
	resizeModal(winHeight); */
	
	
	/* Tree navigation */
	$("a[data-expand='']").click( function() {
		if ( $(this).attr("data-expand-type")) {
			iconOpen = 'icon-plus-sign';
			iconClose = 'icon-minus-sign';
		} else {
			iconOpen = 'icon-caret-right';
			iconClose = 'icon-caret-down';
		}
		if ($(this).hasClass('expand')) {
			$(this).parent().parent().find('.expandable-details').first().slideDown(400, function () {
		     	// finished
			});
			$(this).css("font-weight","700");
			$(this).removeClass('expand').addClass('contract');
			$(this).find('span').removeClass(iconOpen).addClass(iconClose);
		} else if ( $(this).hasClass("contract")) {
			$(this).parent().parent().find('.expandable-details').first().slideUp();
			$(this).css("font-weight","400");
			$(this).removeClass('contract').addClass('expand');
			$(this).find('span').removeClass(iconClose).addClass(iconOpen);
		}
        
	});

	/* works navigation */
	$("#toggle-secondary-navigation").click( function() {
		navCol = $("#secondary-nav-column");
		mainCol = $("#main-content-column");
		if ( navCol.hasClass("hidden") ) {
			navCol.removeClass("hidden").addClass("large-3").addClass("columns");
			mainCol.removeClass("large-12").addClass("large-9");
		} else {
			navCol.addClass("hidden").removeClass("large-3").removeClass("columns");
			mainCol.removeClass("large-9").addClass("large-12");
		}
	});
	
	/* opus navigation */
	/* Show / hide navaigator */
	$("#toggle-opus-navigator").click( function() {
		if ( $("#opus-navigator").hasClass("hidden")) {
			$("#opus-navigator").removeClass("hidden");
			$(this).text("On");
		} else {
			$(this).text("Off");
			$("#opus-navigator").addClass("hidden");
		}
		return false;
	});
	
	/* Annotations panel */
	$("a.ctrl.show-annotations").click( function() {
		$cpanel = $("#context-panel");
		if ( !$cpanel.hasClass("slide-out")) {
			$cpanel.addClass("slide-out");
		} else {
			$cpanel.removeClass("slide-out").addClass("slide-in");
		}
	});
	$("#close-context-panel").click( function() {
		$("#context-panel").removeClass("slide-out");
	});
	
	$("a.ctrl.reply").click( function() {
		$(".reply-box").slideDown(400);
		$(this).css("display","none");
	});
	
	/* save a comment */
	$(".ctrl.save-reply").click( function() {
		replyTo = $(this).attr("data-reply-to");
		replyArea = $('div[data-reply-area="' + replyTo + '"]');
		replyArea.find('.saving').css("display","block");
		setTimeout( function() {
			replyArea.find('.saving').css("display","none");
			if (! replyArea.attr("data-saved-reply") ) {
				replyArea.slideUp(200);
				$('div[data-saved-reply="' + replyTo + '"]').css("display","block");
			}
		}, 500);
	});
	
	/* edit a comment */
	$("a.ctrl.edit").click( function() {
		commentToEdit = $(this).attr("data-edit");
		textarea = $('textarea[data-reply-text="' + commentToEdit + '"]');
		if ( textarea.hasClass("disabled")) {
			// alert("disabled");
			textarea.removeAttr("disabled").removeClass("disabled").focus();
			textarea.removeClass("disabled");
			$(this).parent().parent().parent().parent().find(".edit-actions").css("display","block");
		} else {
			// alert("not disabled");
			textarea.attr("disabled","").addClass("disabled");
			$(this).parent().parent().parent().parent().find(".edit-actions").css("display","none");
		}
	});
	/* cancel editing */
	$("a.ctrl.cancel").click( function() {
		comment = $(this).attr("data-reply-to");
		$('textarea[data-reply-text="' + comment + '"]').attr("disabled","").addClass("disabled").blur();
		$(this).parent().parent().css("display","none");
	});
	
	/******************************************/
	/* Notes and Commentary Expand / Collapse */
	/******************************************/

	$(function() {
	  $('#annotations').find('div.collapseme').hide();
	  $('h4.comm').bind("click", function() {
	    $(this).next('div').slideToggle(400);
	    $("i",this).toggleClass("fa-plus-circle fa-minus-circle");
	    return false;
	  });
	  $('#notes h4.comm').bind("click", function() { toggleExistingNotes(); });
	});
		
});