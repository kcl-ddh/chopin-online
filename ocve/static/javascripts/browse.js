// (function($, config){

addSelectedFilter = function(type, selection) {
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

applyFilter = function(type, id, selection) {
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

serializeFilters = function() {
  // this function sends the current set of filters to
  // the server
  var current_filter_prefixed = config.mode + '_current_filters';
  $.post("/ocve/browse/serializeFilter/", {
    current_filter_prefixed: JSON.stringify(filters)
  });
};

removeFromFilterArray = function(type) {
  // removes a filter from the filters array
  for (var f in filters) {
    if (filters[f].type == type) {
      filters.splice(f, 1);
    }
  }
};

removeSelectedFilter = function(type) {
  // This function gets called when a filter is added
  // or removed brom the browser

  sourceCollection.filters[type].clearQuery();
  $('dl.selected-filter.' + type).remove();
  filterFacets(sourceview.getCurrentItems(), type);
  removeFromFilterArray(type);
  serializeFilters();
};

filterFacets = function(filteredPages, exclude) {
  var filteredWorks = {},
    filteredGenres = {},
    filteredPublishers = {},
    filteredDedicatees = {},
    filteredYears = {};

  for (var x = 0; x < filteredPages.length; x++) {
    try {
      if (!filteredWorks.hasOwnProperty(filteredPages[x].Work)) {
        filteredWorks[filteredPages[x].Work] = 1;
      }
      if (!filteredPublishers.hasOwnProperty(filteredPages[x].Publisher)) {
        filteredPublishers[filteredPages[x].Publisher] = 1;
      }
      if (!filteredDedicatees.hasOwnProperty(filteredPages[x].Dedicatee)) {
        filteredDedicatees[filteredPages[x].Dedicatee] = 1;
      }
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
  if (exclude != 'Dedicatee') {
    filterSelections(dedicatees, filteredDedicatees, 'a.filterCtrl[data-criteria=\"Dedicatee\"]');
  }
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



$(document).ready(function() {
  // setup events

  $('#selectedFilters').on('click', 'a.ctrl.remove[data-criteria]', function(e) {
    e.preventDefault();
    var type = $(this).data('criteria');
    removeSelectedFilter(type);
  });

});
// })(jQuery, JSON, config);