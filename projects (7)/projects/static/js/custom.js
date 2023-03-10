var $populationChart = $("#population-chart");
$.ajax({
  url: $populationChart.data("url"),
  success: function (data) {
    // ...
  }
});