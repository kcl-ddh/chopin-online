// (function($, config){


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
  removeFromFilterArray(type)
  serializeFilters();
};

// })(jQuery, JSON, config);