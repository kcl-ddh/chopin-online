(function($, JSON, PourOver, config, sources, sourcecomponents) {
  'use strict';

  // options extends the base config file; options sets up object properties for browsing
  var options = _.extend(config);
  options.workLabels = _.object(_.rest(config.works), config.work_names);
  options.filters = [];
  options.pageviewURL = '/' + options.mode.toLowerCase() + config.browse_pageview_url;

  options.sourcecomponentsById = {};

  // TODO: are these being used??? delete if not!!!
  options.pageByID = {};
  options.sourceByID = {};
  options.sourceFilterIDs = [];

  // data manipulation

  for (var i = 0, len = sources.length; i < len; i++) {
    options.sourceByID[sources[i].id] = sources[i];
    options.sourceFilterIDs.push(sources[i].id);
    for (var p in sources[i].Pages) {
      options.pageByID[sources[i].Pages[p].id] = sources[i].Pages[p];
    }
  }
  for (i = 0, len = sourcecomponents.length; i < len; i++) {
    options.sourcecomponentsById[sourcecomponents[i].id] = sourcecomponents[i];
  }

  // // //



  var addSelectedFilter = function(type, selection) {
    var $selected_filters_for_type = $(options.selectedFilterSelector + '.' + type),
      $selected_filters = $('#selectedFilters'),
      $no_filters_el = $(options.noFiltersSelector),
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

  var applyFilter = function(type, id, selection, save_to_session) {
    //Apply a pouroverfilter and update the selectedfilters display
    // type: filter type
    //Id: the numeric id in db
    //selection: text label
    // save_to_session defaults to true

    if (save_to_session === undefined) {
      save_to_session = true;
    }

    // apply filter to pourover
    options.sourceCollection.filters[type].query(id);

    // add selected html filter control
    addSelectedFilter(type, selection);

    //Remove existing filters from this type
    removeFromFilterArray(type);

    //push filter to filters list
    options.filters.push({
      "type": type,
      "id": id,
      "selection": selection
    });

    //Push to session if save_to_session is set
    if (save_to_session) {
      serializeFilters();
    }
  };

  var apply_default_filters = function(defaultFilters) {
    _.each(defaultFilters, function(filter, index) {
      var $source_title = $('#source' + filter.id + ' h5');
      if (filter.type === 'Source') {
        $source_title.trigger('click');
        $source_title.find('a').trigger('focus');
      } else {
        applyFilter(filter.type, filter.id, filter.selection, false);
      }
    });
  };

  var serializeFilters = function() {
    // this function sends the current set of filters to
    // the server
    var current_filter_prefixed = options.mode + '_current_filters',
      params = {};
    params[current_filter_prefixed] = JSON.stringify(options.filters);
    $.post("/ocve/browse/serializeFilter/", params);
  };

  var removeFromFilterArray = function(type) {
    // removes a filter from the filters array
    for (var f in options.filters) {
      if (options.filters[f].type == type) {
        options.filters.splice(f, 1);
      }
    }
  };

  var removeSelectedFilter = function(type) {
    // This function gets called when a filter is added
    // or removed brom the browser
    // clear pourover query
    options.sourceCollection.filters[type].clearQuery();

    // remove html filter control
    $('dl.selected-filter.' + type).remove();

    if ($('dl.selected-filter').length) {
      $("#no-filters").hide();
    } else {
      $("#no-filters").show();
    }

    // update facents
    filterFacets(options.sourceview.getCurrentItems(), type);

    // remove filter from array
    removeFromFilterArray(type);

    // save current filters to session
    serializeFilters();
  };

  var filterFacets = function(filteredPages, exclude) {
    if (exclude != 'Work') {
      var filteredWorks = _.chain(filteredPages) // chain following operations
        .pluck('Work')  // select Work property from all objects
        .uniq()         // produce a unique list
        .value();       // return list from chain

      // run filtersection for this set
      filterSelections(options.works, filteredWorks, 'a.filterCtrl[data-criteria=\"Work\"]');
    }

    if (exclude != 'Publisher') {
      var filteredPublishers = _.chain(filteredPages)
        .pluck('Publisher')
        .uniq()
        .value();
      filterSelections(options.publishers, filteredPublishers, 'a.filterCtrl[data-criteria=\"Publisher\"]');
    }

    if (exclude != 'Type') {
      var filteredSourceTypes = _.chain(filteredPages)
        .pluck('Type')
        .uniq()
        .value();
      filterSelections(options.sourceType, filteredSourceTypes, 'a.filterCtrl[data-criteria=\"Type\"]');
    }

    if (exclude != 'Genre') {
      var filteredGenres = _.chain(filteredPages)
        .pluck('Genre') // select Genre property from all objects (usually a list of genres)
        .flatten()      // flatten into single list
        .uniq()
        .value();
      filterSelections(options.genres, filteredGenres, 'a.filterCtrl[data-criteria=\"Genre\"]');
    }

    if (exclude != 'Year') {
      var filteredYears = _.chain(filteredPages)
        .pluck('Year')
        .flatten()
        .uniq()
        .value();
      filterSelections(options.years, filteredYears, 'a.filterCtrl[data-criteria=\"Year\"]');
    }
  };


  var filterSelections = function(selections, validSelections, selectionSelector) {
    var $filterCtrls = $(selectionSelector);
    // hide all filter controls
    $filterCtrls.parent('li').hide();

    // show only ones that are still valid selections
    $filterCtrls.filter(function(index, filterControl) {
      return _.contains(validSelections,
        $(filterControl).data('key'));
    }).parent('li').show();

  };


  var outputWorkGroup = function(sourceList, opusOutput, opusid) {
    var output = ["<div id=\"opus", opusid, "\" class=\"opus\">",
      "<h2> ", options.workLabels[opusid],
      " <span class=\"contextual-info\">"
    ];

    if (options.workinfos.indexOf(opusid) > -1) {
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

    for (var i = 0; i < options.filters.length; i++) {
      if (options.filters[i].type == 'Work') {
        workid = options.filters[i].id;
      }
    }

    for (var x = 0; x < sourcePages.length; x++) {
      var scInstruments;
      if (sourcePages[x].sourcecomponent_id != scid) {

        scInstruments = options.sourcecomponentsById[sourcePages[x].sourcecomponent_id].instruments;

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
          "<p>", options.sourcecomponentsById[sourcePages[x].sourcecomponent_id].label, "</p>"
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
        " href=\"", options.pageviewURL, "/", sourcePages[x].id, "/\">",
        "<img", " class=\"lazy\" data-original=\"", options.thumbnails_url,  sourcePages[x].id, ".jpg\" />",
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
        " data-reveal-ajax=\"/", options.mode.toLowerCase(), "/browse/sourceinformation/", sources[x].id, "/\"",
        " title=\"Witness overview\" data-reveal-id=\"witness-info\">",
        "<i class=\"fa fa-info-circle fa-lg\"></i></a>",
        "</span>",
        "<h5><a href=\"#\" class=\"expandme\"><i class=\"expandd fa fa-caret-right\"></i> ",
        sources[x].label,
        "&#160;<span class='label radius accode secondary'>",
        sources[x].accode,
        "</span></a></h5>",
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

  var SourceView = PourOver.View.extend({
    render: function() {
      var filtered = false;
      for (var i in options.sourceCollection.filters) {
        if (options.sourceCollection.filters[i].current_query) {
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
          var $this = $(this),
           $pagelist = $this.next('ul.pageList');

          // lazily fill img src attributes to be loaded
          $pagelist.find('img.lazy').each(function(index, img_el) {
            var $img_el = $(img_el);
            $img_el.attr('src', $img_el.data('original'))
          });

          // toggle list
          $pagelist.slideToggle(400);

          // switch caret
          $("i.expandd", $this).toggleClass("fa-caret-right fa-caret-down");
          return false;
        });


        $('.opusexpand').on('click', function() {
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

    $('body').on('click', '#selectedFilters a.ctrl.remove', function(e) {
      e.preventDefault();
      var type = $(this).data('criteria');
      removeSelectedFilter(type);
    });

    $("body").on("click", ".instrumentFilter", function(event) {
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

    $(options.clearFiltersSelector).on('click', function() {
      //Clear Queries
      for (var i in options.sourceCollection.filters) {
        options.sourceCollection.filters[i].clearQuery();
      }
      //Remove filters from session
      $.ajax('/ocve/browse/resetFilter/');
      options.filters = [];
      //Restore all filter choices
      $('a.ctrl:hidden').parent('li').show();

    });

    //Generic filter control for the sidebar
    $('.filterCtrl').on('click', function(e) {
      var $this = $(this),
        type = $this.data('criteria'),
        id = $this.data('key'),
        selection = $this.attr('title');

      applyFilter(type, id, selection);
      filterFacets(options.sourceview.getCurrentItems(), type);
      return false;
    });

    //
    //Instantiate PourOver filters

    var work_filter = PourOver.makeExactFilter("Work", options.works);
    var genre_filter = PourOver.makeInclusionFilter("Genre", options.genres);
    var year_filter = PourOver.makeInclusionFilter("Year", options.years);
    var publisher_filter = PourOver.makeExactFilter("Publisher", options.publishers);
    var sourcetype_filter = PourOver.makeExactFilter("Type", options.sourceType);
    var KeyMode_filter = PourOver.makeExactFilter("KeyMode", options.keyModes);

    //Create collections based on pre-exported JSON
    options.sourceCollection = new PourOver.Collection(sources);
    options.sourceCollection.addFilters([work_filter,
      genre_filter,
      publisher_filter,
      year_filter,
      sourcetype_filter,
      KeyMode_filter
    ]);

    var order_sort = new sourceSort("orderno");
    options.sourceCollection.addSorts([order_sort]);

    //views for sidebar and main
    options.sourceview = new SourceView("main_collection", options.sourceCollection);
    options.sourceview.on("update", function() {
      options.sourceview.render();
    });


    //apply default filters ffrom session
    apply_default_filters(options.defaultFilters);

  });
})(jQuery, JSON, PourOver, config, sources, sourcecomponents);