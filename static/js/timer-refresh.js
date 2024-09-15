document.addEventListener('DOMContentLoaded', function() {
	let timerInterval;
	let countdownTime = 30; // Set initial countdown time in seconds

	function updateTimer() {
		const refreshTimerElement = document.getElementById('refresh-timer');
		if (countdownTime <= 0) {
			refreshPage();
			countdownTime = 30; // Reset timer
		} else {
			refreshTimerElement.textContent = `${countdownTime}s`;
			countdownTime--;
		}
	}

	function refreshPage() {
		window.location.reload();
	}

	function startTimer() {
		timerInterval = setInterval(updateTimer, 1000); // Update every second
	}

	function stopTimer() {
		clearInterval(timerInterval); // Stop the timer
	}

	document.getElementById('refresh-button').addEventListener('click', function() {
		stopTimer(); // Stop the countdown
		refreshPage(); // Refresh the page immediately
		countdownTime = 30; // Reset timer to 30 seconds
		startTimer(); // Restart the countdown
	});

	startTimer(); // Start the countdown timer on page load
});
