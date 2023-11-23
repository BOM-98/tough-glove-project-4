/**
 * Initializes and renders a FullCalendar instance on a webpage.
 * 
 * This script sets up a calendar using the FullCalendar library, tailored for displaying
 * class events on a calendar element. It waits for the DOM content to be fully
 * loaded before executing. The calendar is configured with various options including theme,
 * header toolbar, initial view, event sources, and more.
 * 
 * Usage:
 * - Ensure this script is included in a webpage with a DOM element having the ID 'calendar'.
 * - The script will automatically execute upon full page load.
 * - Requires FullCalendar library and Bootstrap 5 to be included in the webpage.
 *
 * Functions:
 * - N/A
 *
 * Configuration:
 * - Theme: Bootstrap 5
 * - Header Toolbar: Includes navigation, title, and view change buttons.
 * - Initial View: Week view with time grids.
 * - Events Source: URL endpoint '/get_classes/'.
 * - Event Interaction: Clicking an event shows an alert with event details.
 * - Styling: Events are colored red.
 * - Time Indicator: Shows the current time.
 * - Time Slot Formatting: 24-hour format with hour and minute.
 * - Scroll Start Time: Calendar view starts at 9 AM.
 */
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
      eventColor: '#ff0000',
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