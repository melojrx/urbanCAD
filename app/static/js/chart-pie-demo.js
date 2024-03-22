function createPieChart(listOcorrenciaByStatus) {

  Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
  Chart.defaults.global.defaultFontColor = '#292b2c';

  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: listOcorrenciaByStatus.map(function(ocorrencia) {
        return ocorrencia.label;
      }),
      datasets: [{
        data: listOcorrenciaByStatus.map(function(ocorrencia) {
          return ocorrencia.data;
        }),
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
      }],
    },
  });
}
