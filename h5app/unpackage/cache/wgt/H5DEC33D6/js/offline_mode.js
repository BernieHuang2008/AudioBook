// auto detect
$.ajax({
	url: "https://reading.baicizhan.com/api/query_word?word=test",
	type: 'GET',
	success: () => {},
	error: () => {
		offline_mode_on();
	}
});

function offline_mode_on() {

	// 1. use offline translation: user-select to enable on-phone translation service
	console.log("OFFLINE_MODE enabled.");
	$("#article").css("user-select", "text");

	var last_selection = "";
	document.addEventListener('selectionchange', function(event) {
		const selection = window.getSelection();
		if (selection.rangeCount > 0) {
			var selectedText = selection.getRangeAt(0).toString();

			if (selectedText != "") {
				// make it pause
				if (!$("#audio")[0].paused) {
					$("#audio-control > #btn").click();
				}
			}
			if (selectedText == "" && selectedText != last_selection) {
				// make it resume
				if ($("#audio")[0].paused) {
					$("#audio-control > #btn").click();
				}
			}

			last_selection = selectedText;
		}
	});

}