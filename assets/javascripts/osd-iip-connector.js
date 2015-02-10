/********************
 * IIP Connector for easy use of
 * OpenSeaDragon with IIPSVR.
 *
 * Requires:
 * 	- JQuery
 * 	- OpenSeaDragon
 */

/**
 * Finds parameters
 *
 * url: URL to search
 *
 * Returns the parameter value
 */
function getParams(url)
{
    var vars = [], hash;
    var hashes = url.slice(url.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

/**
 * Simple function to get the URL before the
 * params
 */
function getURLBeforeParams(url)
{
	return url.split("?")[0] || null;
}

/**
 * Converts IMG elements to OSD
 */
function imgToOSD()
{
	// Rather annoyingly, OSD requires the *absolute* URL to the
	// images folder it provides. This script assumes that the
	// images folder is a subfolder of the folder containing
	// openseadragon.js or openseadragon-min.js - whichever you
	// choose to use.
	var tilesource = $('script[src*="openseadragon.min.js"],script[src*="openseadragon.js"]').attr('src');
	tilesource = tilesource.substr(0, tilesource.lastIndexOf("\/")) + "/images/"

	$("img.osd-iip").each(function()
	{
		// Fetch the image URL and parameters
		var src = $(this).attr("src");
		var params = getParams(src);
		var height = $(this).attr("height") > 0 ? $(this).attr("height") + "px" : '';
		var width = $(this).attr("width") > 0 ? $(this).attr("width") + "px" : '';

		jQuery('<div/>', {
		    id: $(this).attr("id"),
			class: $(this).attr("class"),
			style: 'height: ' + height + '; width: ' + width + ';'
		}).insertAfter(this);

		// Remove the img element
		$(this).remove();
        var ts=getURLBeforeParams(src) + "?DeepZoom=" + params['FIF'] + ".dzi"
        console.log(ts);
		OpenSeadragon({
			id: $(this).attr("id"),
			prefixUrl: tilesource,
			tileSources: getURLBeforeParams(src) + "?DeepZoom=" + params['FIF'] + ".dzi"
		});
	});
}

/**
 * Run the script!
 * Moved to main init by EH

$("document").ready(function()
{

});
 */