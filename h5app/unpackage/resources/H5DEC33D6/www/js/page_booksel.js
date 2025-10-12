function plus_io_dir(path, callback) {
    if (typeof plus === "undefined" || !plus.io) {
        console.error("plus.io is not available.");
        return;
    }

    plus.io.resolveLocalFileSystemURL(plus.io.convertLocalFileSystemURL(path), function(dirEntry) {
        var directoryReader = dirEntry.createReader();
        directoryReader.readEntries(function(entries) {
            var files = [];
            for (var i = 0; i < entries.length; i++) {
                if (entries[i].isDirectory) {
                    files.push(entries[i].name);
                }
            }
            callback(files);
        }, function(error) {
            console.error("Error reading directory entries:", error);
        });
    });
}

function booksel_init() {
    console.log("Initializing book selection...");

    plus_io_dir("_doc/books", (files) => {
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
    });

    const dropdown = document.getElementById('book-dropdown');
    dropdown.addEventListener('change', handleBookSelection);
}

function handleBookSelection() {
    const dropdown = document.getElementById('book-dropdown');
    const selectedBook = dropdown.value;

    if (selectedBook) {
        show_last_reading_date(selectedBook);
        // selectBook(selectedBook);
        // chpage('page_player');
    }
}

function show_last_reading_date(book_name) {
    var last_reading_date = localStorage.getItem(`reading-record-${book_name}`) || '1';
    $("#day-selector").val(last_reading_date);
}

function start_reading_btn() {
    var book_name = $('#book-dropdown').val();
    var day = $('#day-selector').val();
    if (!book_name) {
        alert("Please select a book.");
        return;
    }
    localStorage.setItem("last-read-book-name", book_name);
    selectBook(book_name, day);
}
