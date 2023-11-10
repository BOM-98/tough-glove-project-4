document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      themeSystem: 'bootstrap5',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay, listWeek'
      },
      initialView: 'timeGridWeek',
      events: '/get_classes/',
      eventClick: function(info) {
            alert('Event: ' + info.event.title + '\nDescription: ' + info.event.start);
      },
      nowIndicator: true,
      slotLabelFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      },
      scrollTime: '09:00:00',
    });
    calendar.render();
  });