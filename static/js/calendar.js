document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: '/get_classes/',
        eventClick: function(info) {
            alert('Event: ' + info.event.title + '\nDescription: ' + info.event.extendedProps.description);
        }
    });
    calendar.render();
  });