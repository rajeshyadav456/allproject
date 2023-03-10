
// $(document).ready(function() {
//     $('#example').DataTable();
//     } );
    
//     /****chart***/
//     window.onload = function () {
    
//         var config_2 = {
//             type: 'bar',
//                 data: {
//                   labels: ['Jan','Feb','March'],
//                   datasets: [{
//                     label: 'Population',
//                     backgroundColor: 'blue',
//                     data:['1','2','3']
//                   }]          
//                 },
//                 options: {
//                   responsive: true,
//                   legend: {
//                     position: 'top',
//                   },
//                   title: {
//                     display: true,
//                     text: 'Population Bar Chart'
//                   }
//                 }
//         };
    
//         var ctx_2 = document.getElementById('graph-chart').getContext('2d');
//         window.myColumn = new Chart(ctx_2, config_2);
    
    
//         var config = {
//             type: 'pie',
//             data: {
//               datasets: [{
//                 data: ['129900','1234567890','0987654321'],
//                 backgroundColor: [
//                   '#ff0000', '#0000ff', '#ff0080', '#73ffff', '#5c26ff', '#002db3', '#ffff26', '#4cff4c', '#ff00ff'
//                 ],
//                 label: 'Population'
//               }],
//               labels: ['Manila City', 'Davao City', 'Makati']
//             },
//             options: {
//               responsive: true
//             }
//           };
    
//           var ctx = document.getElementById('pie-chart').getContext('2d');
//           window.myPie = new Chart(ctx, config);
    
    
    
//     }
    








































var $populationChart = $("#population-chart");
$.ajax({
  url: $populationChart.data("url"),
  success: function (data) {
    // ...
  }
});









    