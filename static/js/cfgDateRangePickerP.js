$(function() {
  dia = parseInt(moment().format('DD')) + 7
  $('input[name="dataP"]').daterangepicker({
    showDropdowns: true,
    startDate: moment().format('YYYY-MM-DD'),
    endDate: moment().format('YYYY-MM')+dia.toString(),
    locale: {
      "format": "YYYY-MM-DD",
      "separator": " / ",
      "applyLabel": "Aceitar",
      "cancelLabel": "Cancelar",
      "fromLabel": "De",
      "toLabel": "Para",
      "customRangeLabel": "Custom",
      "weekLabel": "S",
      "daysOfWeek": [
        "Dom",
        "Seg",
        "Ter",
        "Qua",
        "Qui",
        "Sex",
        "Sab"
      ],
      "monthNames": [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
      ],
      "firstDay": 1
    }, function(start, end) {
      $('p[name="dataInicio"]').val(start)
      $('p[name="qtdDias"]').val(
        moment().diff(end,'days') * -1
      )
    }
  })
})