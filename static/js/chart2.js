// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var COLORS_LIGHT = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e70000', '#e15d03', '#fff69a'];
var COLORS_DARK = ['#2e59d9', '#17a673', '#2c9faf', '#deaf38', '#ce0018', '#ca5302', '#e5dd8a'];

function const_pie(labels_pie, values_pie){
  this.labels = labels_pie;
  this.values = values_pie;
  pie_chart()
}

function pick_colors(n) {
  var light = [];
  var dark = [];

  for (var i = 0; i < n; i++) {
    var color_idx = i % COLORS_LIGHT.length;
    light.push(COLORS_LIGHT[color_idx]);
    dark.push(COLORS_DARK[color_idx]);
  }

  return { light: light, dark: dark };
}

function pie_chart(){
  // Pie Chart Example

  var colors = pick_colors(self.labels.length)

  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: this.labels,
      datasets: [{
        data: this.values,
        backgroundColor: colors.light,
        hoverBackgroundColor: colors.dark,
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function label(tooltipItem,chart){
            var val = chart.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
            return val + '%';
          }
        }
      },
      legend: {
        display: true
      },
      cutoutPercentage: 80,
    },
  });
}