// (function($, config){

var addSelectedFilter = function(type, selection) {
  var $selected_filters_for_type = $(selectedFilterSelector + '.' + type),
    $selected_filters = $('#selectedFilters'),
    $no_filters_el = $(noFiltersSelector),
    filterHTML = ["<dl class=\"selected-filter ", type, "\">",
      "<dt class=\"filter\">", type, ":</dt>",
      "<dd><span>", selection, "</span>",
      "<a class=\"ctrl remove\" data-criteria=\"", type, "\">",
      "<i class=\"fa fa-times-circle-o\"></i>", "</a>", "</dd>", "</dl>"
    ].join("");

  //Type is currently exclusive, may change
  if ($selected_filters_for_type.size() > 0) {
    $selected_filters_for_type.find('dd span').html(selection);
  } else {
    $selected_filters.append(filterHTML);
  }

  $no_filters_el.hide();

};

var applyFilter = function(type, id, selection) {
  //Apply a pouroverfilter and update the selectedfilters display
  // type: filter type
  //Id: the numeric id in db
  //selection: text label
  if (type != 'KeyPitch') {
    sourceCollection.filters[type].query(id);
  }
  addSelectedFilter(type, selection);
  //Remove existing filter type
  removeFromFilterArray(type);
  filters.push({
    "type": type,
    "id": id,
    "selection": selection
  });
  //Push to session
  serializeFilters();
};

var serializeFilters = function() {
  // this function sends the current set of filters to
  // the server
  var current_filter_prefixed = config.mode + '_current_filters';
  $.post("/ocve/browse/serializeFilter/", {
    current_filter_prefixed: JSON.stringify(filters)
  });
};

var removeFromFilterArray = function(type) {
  // removes a filter from the filters array
  for (var f in filters) {
    if (filters[f].type == type) {
      filters.splice(f, 1);
    }
  }
};

var removeSelectedFilter = function(type) {
  // This function gets called when a filter is added
  // or removed brom the browser

  sourceCollection.filters[type].clearQuery();
  $('dl.selected-filter.' + type).remove();
  filterFacets(sourceview.getCurrentItems(), type);
  removeFromFilterArray(type);
  serializeFilters();
};

var filterFacets = function(filteredPages, exclude) {
  var filteredWorks = {},
    filteredGenres = {},
    filteredPublishers = {},
    // filteredDedicatees = {},
    filteredYears = {};

  for (var x = 0; x < filteredPages.length; x++) {
    try {
      if (!filteredWorks.hasOwnProperty(filteredPages[x].Work)) {
        filteredWorks[filteredPages[x].Work] = 1;
      }
      if (!filteredPublishers.hasOwnProperty(filteredPages[x].Publisher)) {
        filteredPublishers[filteredPages[x].Publisher] = 1;
      }
      // if (!filteredDedicatees.hasOwnProperty(filteredPages[x].Dedicatee)) {
      //   filteredDedicatees[filteredPages[x].Dedicatee] = 1;
      // }
      if (filteredPages[x] && filteredPages[x].Year) {
        for (var i = 0; i < filteredPages[x].Year.length; i++) {
          if (!filteredYears.hasOwnProperty(filteredPages[x].Year[i])) {
            filteredYears[filteredPages[x].Year[i]] = 1;
          }
        }
      }

      if (filteredPages[x] && filteredPages[x].Genre) {
        for (var i = 0; i < filteredPages[x].Genre.length; i++) {
          if (!filteredGenres.hasOwnProperty(filteredPages[x].Genre[i])) {
            filteredGenres[filteredPages[x].Genre[i]] = 1;
          }
        }
      }

    } catch (TypeError) {
      console.log(TypeError);
      console.log(x);
    }

  }
  if (exclude != 'Work') {
    filterSelections(works, filteredWorks, 'a.filterCtrl[data-criteria=\"Work\"]');
  }
  // if (exclude != 'Dedicatee') {
  //   filterSelections(dedicatees, filteredDedicatees, 'a.filterCtrl[data-criteria=\"Dedicatee\"]');
  // }
  if (exclude != 'Genre') {
    filterSelections(genres, filteredGenres, 'a.filterCtrl[data-criteria=\"Genre\"]');
  }
  if (exclude != 'Year') {
    filterSelections(years, filteredYears, 'a.filterCtrl[data-criteria=\"Year\"]');
  }
  if (exclude != 'Publisher') {
    filterSelections(publishers, filteredPublishers, 'a.filterCtrl[data-criteria=\"Publisher\"]');
  }
};


var filterSelections = function(selections, validSelections, selectionSelector) {
  var $selectionSelector = $(selectionSelector);

  for (var i in selections) {
    if (!validSelections.hasOwnProperty(selections[i])) {
      $selectionSelector.find('[data-key=' + selections[i] + ']').parent('li').hide();
    } else {
      $selectionSelector.find('[data-key=' + selections[i] + ']').parent('li').show();
    }
  }
};


var outputWorkGroup = function(sourceList, opusOutput, opusid) {
  var output = ["<div id=\"opus", opusid, "\" class=\"opus\">",
    "<h2> ", workLabels[opusid],
    " <span class=\"contextual-info\">"
  ];

  if (workinfos.indexOf(opusid) > -1) {
    output = output.concat(["<a href=\"#\" class=\"ctrl more\" data-tooltip=\"\" data-reveal-ajax=\"/",
      config.mode.toLowerCase(),
      "/browse/workinformation/",
      opusid,
      "/\" title=\"Work overview\" data-reveal-id=\"opus-info\">",
      "<span class=\"fa fa-book\"></span>",
      "</a>"
    ]);
  }
  output = output.concat(["</span>", "</h2>", opusOutput, "</div>"]);
  return output.join("");
};

var outputPages = function(source, availInstruments) {
  //Output the determined number of preview pages for each source with further links
  var output = [],
    sourcePages = source.Pages,
    scid = 0,
    workid = 0;

  for (var i = 0; i < filters.length; i++) {
    if (filters[i].type == 'Work') {
      workid = filters[i].id
    }
  }

  for (var x = 0; x < sourcePages.length; x++) {
    var scInstruments;
    if (sourcePages[x].sourcecomponent_id != scid) {

      scInstruments = sourcecomponentsById[sourcePages[x].sourcecomponent_id].instruments;

      if (scInstruments) {
        for (var i = 0; i < scInstruments.length; i++) {
          availInstruments['' + scInstruments] = 1;
        }
      } else {
        scInstruments = [];
      }

      output = output.concat([" <li data-instruments=\"", scInstruments.toString(), "\"",
        " id=\"page", sourcePages[x].id, "\"",
        " class=\"page flag\">",
        "<p>", sourcecomponentsById[sourcePages[x].sourcecomponent_id].label, "</p>"
      ]);

      scid = sourcePages[x].sourcecomponent_id;

    } else {
      // TODO: scInstruments here is always empty, can we have a look
      output = output.concat(["<li data-instruments=\"", scInstruments.toString(), "\"",
        " id=\"page", sourcePages[x].id, "\" class=\"page\">"
      ]);
    }

    var source_pages_label_display = (sourcePages[x].label.length > 30) ?
      sourcePages[x].label.substring(0, 27) + "..." :
      sourcePages[x].label;

    output = output.concat(["<a class=\"pageView th\" data-sourcekey=\"", sourcePages[x].id, "\"",
      " href=\"", pageviewURL, "/", sourcePages[x].id, "/\">",
      "<img", " class=\"lazy\" data-original=\"/thumbnails/", sourcePages[x].id, ".jpg\" />",
      "</a>",
      "<span class=\"page-label\" title=\"", sourcePages[x].label, "\">",
      source_pages_label_display,
      "</span>",
      "</li>"
    ]);

  }
  return output.join("");
};

var outputSources = function(sources) {
  var output = [],
    opusOutput = [],
    sourceList = [],
    opusid = 0,
    availInstruments = {
      "0": 1
    };

  //Filter matching opus quickjump
  for (var x = 0; x < sources.length; x++) {
    if (opusid == 0) {
      opusid = sources[x].Work;
    }
    if (sources[x].Work != opusid) {

      output = output.concat(
        outputWorkGroup(
          sourceList.join(""),
          opusOutput.join(""),
          opusid));
      opusid = sources[x].Work;
      opusOutput = [];
      sourceList = [];
    }
    //Write source in quick list for opus
    sourceList = sourceList.concat(["<li><a href=\"#source", sources[x].id, "\" class=\"sourceLink\"",
      " data-sourcekey=\"", sources[x].id, "\">",
      sources[x].label, "</a>"
    ]);

    //Collect all the sources in the opus
    opusOutput = opusOutput.concat(["<div id=\"source", sources[x].id, "\" class=\"source\">",
      "<span class=\"contextual-info right\" >"
    ]); //Edit link to source editor, for stage only.


    if (sources[x].achash.length > 0) {
      opusOutput = opusOutput.concat([
        "<a class=\"ctrl more\" data-tooltip=\"\"",
        " title=\"View in Annotated Catalogue\" href=\"/aco/catalogue/impression/",
        sources[x].achash, "/\">",
        "<i class=\"fa fa-link\"></i></a>&nbsp;"
      ]);
    }
    opusOutput = opusOutput.concat([
      "<a href=\"#\" class=\"ctrl more\" data-tooltip=\"\"",
      " data-reveal-ajax=\"/", config.mode.toLowerCase(), "/browse/sourceinformation/", sources[x].id, "/\"",
      " title=\"Witness overview\" data-reveal-id=\"witness-info\">",
      "<i class=\"fa fa-info-circle fa-lg\"></i></a>",
      "</span>",
      "<h5><a href=\"#\" class=\"expandme\"><i class=\"expandd fa fa-caret-right\"></i> ", sources[x].label, "</a></h5>",
      "<ul id=\"sourcePages", sources[x].id, "\" class=\"pageList movement\">",
      outputPages(sources[x], availInstruments),
      "</ul>", "</div>"
    ]);

  }

  //Output last group
  output = output.concat(
    outputWorkGroup(sourceList.join(""),
      opusOutput.join(""),
      opusid)
  );

  //Show available instrument filters
  showAvailableFilters(availInstruments);


  return output.join("");
};

var showAvailableFilters = function(availInstruments) {
  var avail = 0;
  //Show Instrument filters
  $('li.instrumentFilter').each(function(index) {
    if (availInstruments['' + $(this).data('instrument_id') + ''] == 1 && $(this).data('instrument_id') != 2) {
      avail += 1;
      $(this).show();
    } else if ($(this).data('instrument_id') != '0') {
      $(this).hide();
    }
  });
  if (avail > 2) {
    $('#instrumentFilterControl').show();
  } else {
    $('#instrumentFilterControl').hide();
    $('#instrumentToggle').html('Filter by instrument');
  }
};


// Pourover extensions
var sourceSort = PourOver.Sort.extend({
  attr: "orderno",
  fn: function(a, b) {
    if (b < a) {
      return -1;
    } else if (b > a) {
      return 1;
    } else {
      return 0;
    }
  }
});

SourceView = PourOver.View.extend({
  render: function() {
    var filtered = false;
    for (var i in sourceCollection.filters) {
      if (sourceCollection.filters[i].current_query) {
        filtered = true;
        break;
      }

    }

    if (filtered) {
      var items = this.getCurrentItems(),
        output = outputSources(items);

      $("#results").html(output);

      //Instantiate events for generated content
      $('h5').on("click", function() {
        //Load images now that tab is being opened
        var $this = $(this);

        $this.next('ul.pageList').find('img.lazy').each(function(index) {
          $this.attr('src', $this.attr('data-original'))
        });

        $this.next('ul.pageList').slideToggle(400);
        $("i.expandd", $this).toggleClass("fa-caret-right fa-caret-down");
        return false;
      });


      $('.opusexpand').click(function() {
        var opuskey = $(this).data('opuskey');

        $('#opusSummary' + opuskey).slideToggle();
      });
    } else {
      //Clear old filter
      $("#results").html('');
    }
  }
});

$(document).ready(function() {
  // setup events

  $('#selectedFilters').on('click', 'a.ctrl.remove[data-criteria]', function(e) {
    e.preventDefault();
    var type = $(this).data('criteria');
    removeSelectedFilter(type);
  });

  $("body").on("click", ".instrumentFilter", function(event) {
    // console.log(event);
    var iid = $(this).data("instrument_id");
    $('#instrumentToggle').html($(this).children('a').html());
    if (iid !== 0) {
      $("li.page[data-instruments*='" + iid + "']:hidden").fadeIn();
      $("li.page").not("[data-instruments*='" + iid + "']").fadeOut();
    } else {
      $("li.page").fadeIn();
      $('#instrumentToggle').html('Filter by instrument');
    }
    return false;
  });

});
// })(jQuery, JSON, PourOver, config);