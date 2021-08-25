// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var COLORS_LIGHT = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e70000', '#e15d03', '#fff69a'];
var COLORS_DARK = ['#2e59d9', '#17a673', '#2c9faf', '#deaf38', '#ce0018', '#ca5302', '#e5dd8a'];

function const_bar(labels_pie, values_bar){
  this.labels = labels_pie;
  this.values = values_bar;
  bar_chart()
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

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}


function bar_chart(){
  // Bar Chart Example

  var colors = pick_colors(self.labels.length)

  var ctx = document.getElementById("myReturnsChart");
  var myReturnsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: this.labels,
      datasets: [{
        label: "Average Returns",
        backgroundColor: colors.light,
        hoverBackgroundColor: colors.dark,
        borderColor: "#4e73df",
        data: this.values,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          
          maxBarThickness: 25,
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function(value, index, values) {
              return value + '%' ;
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel + '%';
          }
        }
      },
    }
  });
}