function render_dropdown(files) {
	const dropdown = document.getElementById('book-dropdown');
	dropdown.innerHTML = '<option value="">Select a book...</option>';
	files.forEach(file => {
		const option = document.createElement('option');
		option.value = file;
		option.textContent = file;
		dropdown.appendChild(option);
	});

	// set default
	var last_read_book_name = localStorage.getItem("last-read-book-name");
	if (last_read_book_name) {
		dropdown.value = last_read_book_name;
		show_last_reading_date(last_read_book_name);
	}
}

function booksel_init() {
	console.log("Initializing book selection...");

	const dropdown = document.getElementById('book-dropdown');
	dropdown.addEventListener('change', handleBookSelection);

	if (window.location.href.startsWith("file://")) {
		// For local file access (e.g., Android app)
		plus_io_dir("_doc/books", render_dropdown);
	}
	else {
		// For server access
		fetch('/resources/booklist')
			.then(response => response.json())
			.then(data => {
				render_dropdown(data.booklist);
			})
			.catch(error => {
				console.error('Error fetching book list:', error);
			});
	}
}

function handleBookSelection() {
	const dropdown = document.getElementById('book-dropdown');
	const selectedBook = dropdown.value;

	if (selectedBook) {
		show_last_reading_date(selectedBook);
	}
}

function show_last_reading_date(book_name) {
	var last_reading_date = localStorage.getItem(`reading-record-${book_name}`) || '1';
	$("#day-selector")[0].placeholder = "上次读到：" + last_reading_date;
	$("#day-selector").val("");
}

function start_reading_btn() {
	var book_name = $('#book-dropdown').val();
	var day = $('#day-selector').val();
	if (!book_name) {
		alert("Please select a book.");
		return;
	}
	localStorage.setItem("last-read-book-name", book_name);
	// selectBook(book_name, day);
	window.location.href = `read.html?book=${book_name}&day=${day}`;
}