document.getElementById("booking-cancel").addEventListener("click", function() {
    window.location.href = "{% url'user_bookings' %}"
});