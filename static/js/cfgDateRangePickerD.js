$(function() {
  $('input[name="dataD"]').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    startDate: moment().format('YYYY-MM-DD'),
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
    }
  })
})