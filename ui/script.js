
/* Key */
document.body.onkeydown = function (e) {
    var epr = $(".focus")[0].previousSibling;
    var ene = $(".focus")[0].nextSibling;

    switch (e.key) {
        case 'ArrowUp':
            if (epr) {
                epr.classList.add('focus');
                $(".focus")[1].classList.remove('focus');
                scrollToEle(epr);

                newtime = epr.getAttribute("timestamp");
                $("#audio")[0].currentTime = newtime;
                window.playTime.unshift(newtime);
            }
            break;
        case 'ArrowDown':
            if (ene) {
                ene.classList.add('focus');
                $(".focus")[0].classList.remove('focus');
                scrollToEle(ene);

                window.playTime.shift();
                $("#audio")[0].currentTime = window.playTime[0];
            }
            break;
        case ' ':
            $("#btn")[0].onclick();
            break;
        case 'c':
            SwitchClick();
            break;
        case 'o':
            $(".SwitchIcon").style.display = ($(".SwitchIcon").style.display == "none" ? "block" : "none");
            break;
        case 'r':
            speed(Number(prompt("New Speed:")));
            break;
        default:
            return;
    }

    e.preventDefault();
}

/* Controller */
function SwitchClick() {
    var onoffswitch = $("#toggle-button");
    if (onoffswitch.attr('checked')) {
        $(".word-cnmean").hide();
    }
    else {
        $(".word-cnmean").show();
    }
    onoffswitch.attr('checked', !onoffswitch.attr('checked'));
}

function scrollToEle(x) {
    scrollTo(0, x.offsetTop - window.innerHeight / 2 + x.offsetHeight / 2)
}

function speed(s) {
    if (s) return audio.playbackRate = s;
}

/* Article */
function render(sentences) {
    var article = $("#article");

    for (var i = 0; i < sentences.length; i++) {
        var s = sentences[i];
        var div = $("<p>");
        div.addClass('sentence');
        div.attr('timestamp', s.timestamp);

        var memory = {
            last_phrase: -1,
            last_sn: -1,
        }

        // Add words
        for (var j = 0; j < s.words.length; j++) {
            var w = s.words[j];
            var w_next = (j + 1 < s.words.length) ? s.words[j + 1] : null;
            var span = $("<span>");
            span.addClass('word');

            // word type
            switch (w.type) {
                case 0:
                    span.addClass('word-english');
                    break;
                case 1:
                    span.addClass('word-space');
                    break;
                case 2:
                    span.addClass('word-punctuation');
                    break;
            }

            // word style
            w.style.forEach(style => {
                switch (style) {
                    case "i":
                        span.addClass('italic');
                        break;
                }
            })

            // word belongs to which phrase
            if (w.phrase_id) {
                span.addClass('word-phrase');
                span.attr('phrase', w.phrase_id);
                memory.last_phrase = w.phrase_id;
            }
            else if (w.type == 1 && w_next && w_next.phrase_id == memory.last_phrase) {
                // space between words in the same phrase
                span.addClass('word-phrase');
            }
            else {
                memory.last_phrase = -1;
            }

            // special noun
            if (w.special_noun) {
                span.addClass('word-sn');
                span[0].dataset.sn = JSON.stringify(w.special_noun);
                memory.last_sn = w.special_noun;
            }
            else if (w.type == 1 && w_next && w_next.special_noun == memory.last_sn) {
                // space between words in the same phrase
                span.addClass('word-sn');
            }
            else {
                memory.last_sn = -1;
            }

            span.text(w.word);
            div.append(span);

            // chinese meaning
            if (w.mean) {
                var cnspan = $("<span>");
                cnspan.addClass('word-cnmean');
                cnspan.text(`(${w.mean.trim()})`);
                div.append(cnspan);
            }
        }

        article.append(div);
    }

    // translate listener
    $(".word.word-english").dblclick(function () {
        var word = $(this).text();
        translate_word(this, word);
    });
    $(".word.word-phrase").click(function () {
        var phrase = $(this).attr('phrase');
        translate_phrase(this, phrase);
    })

    $(".sentence")[0].classList.add('focus');
}

function render_questions() {
    var qs = $(".question-choices");
    for (var i = 0; i < qs.length; i++) {
        var q = qs[i];
        var choices = $(q).children();

        for (var j = 0; j < choices.length; j++) {
            var c = choices[j];

            c.innerHTML = `
            <div class="task">
            <div class="left-control" style="background: #50b5e9">
                <div class="task-control" onclick="checkQAnswer(${i}, ${j})">
                    <div class="svg-icon hide"><svg xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 16 16">
                            <path
                                d="M6.54 13c-.3 0-.59-.13-.81-.35L2 8.75l1.62-1.69 2.86 2.98L12.26 3 14 4.56l-6.59 8.02c-.21.25-.51.4-.83.42h-.04z"
                                fill-rule="evenodd"></path>
                        </svg></div>
                </div>
            </div>
            <div class="task-content">
                <p>${c.innerText}</p>
            </div>
            </div>
            `
        }
    }

    window.checkQAnswer = function (i, j) {
        var q = $(".question")[i];
        var choices = $(q).find('.question-choice');

        $(q).find('.question-analysis').show();

        choices[j].classList.add('question-selected');

        choices.each((index, ele) => {
            var task = $(ele).find('.task');
            var tastctrl = task.find('.task-control');
            tastctrl.attr('onclick', '');

            if (ele.classList.contains('question-correct')) {
                task.css('background', 'green');
            }
            else if (ele.classList.contains('question-selected')) {
                task.css('background', 'red');
                task.css('text-decoration', 'line-through');
            }
            else {
                task.css('background', 'gray');
            }

            if (ele.classList.contains('question-selected')) {
                task.find('.svg-icon').removeClass('hide');
            }
        });
    }
}

function loaddata(rawdata) {
    window.rawdata = rawdata;
    var sentences = rawdata.article_info.sentences;

    // 1. Parse words
    for (var i = 0; i < sentences.length; i++) {
        var s = sentences[i];
        var words = s.data;
        for (var j = 0; j < words.length; j++) {
            var w = words[j];
            var nw = {
                word: w.word,
                type: w.type,
                style: w.style || [],
                mean: w.mean || '',
                phrase_id: w.phrase_id,
                special_noun: w.proper_noun_key ? s.proper_noun_hash[w.proper_noun_key] : null,
            };
            words[j] = nw;
        }
    }

    // 2. Parse sentences
    var parsed_sentences = [];

    for (var i = 0; i < sentences.length; i++) {
        var s = sentences[i];
        parsed_sentences.push({
            timestamp: -1,
            words: s.data
        });
    }

    // 3. Parse time
    var times = rawdata.article_info.audio_info.audio_info_by_speed.normal.time_list;
    for (var i = 0; i < times.length; i++) {
        var t = times[i];
        parsed_sentences[i].timestamp = t;
    }

    window.parsed = parsed_sentences;
    window.playTime = times;

    // 4. Load questions
    var questions = rawdata.problem_info;
    if (questions) {
        for (var i = 0; i < questions.length; i++) {
            var q = questions[i];
            var div = $("<div>");
            div.addClass('question');

            var desc = $("<div>");
            desc.addClass('question-desc');
            desc.text(q.question.en);

            var choices = $("<div>");
            choices.addClass('question-choices');
            for (var j = 0; j < q.options.length; j++) {
                var c = q.options[j];
                var choice = $("<div>");
                choice.addClass('question-choice');
                choice.text(c.en);
                if (j == q.answer[0])
                    choice.addClass('question-correct');
                choices.append(choice);
            }

            var analysis = $("<div>");
            analysis.addClass('question-analysis');
            analysis.text(q.analysis[0]);

            div.append(desc);
            div.append(choices);
            div.append(analysis);
            $("#questions").append(div);
        }
        render_questions();
    }
    // Last: Render
    render(parsed_sentences);
}

function load(day) {
    var url = `/${window.book_name}/data/${day}.json`;
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: (data) => {
            loaddata(data);
            loadAudio(day);
        }
    });
}

/* Audio */
function loadAudio(day) {
    var url = `/${window.book_name}/audio/${day}.mp3`;
    $("#audio").attr('src', url);

    $("#audio")[0].onloadedmetadata = function () {
        var time = $("#audio")[0].duration;
        var minute = time / 60;
        var minutes = parseInt(minute);

        if (minutes < 10)
            minutes = "0" + minutes;

        var second = time % 60;
        var seconds = Math.round(second);

        if (seconds < 10)
            seconds = "0" + seconds;

        var totalT = minutes + ":" + seconds;
        $("#totalT").text(totalT);
    }

    $("#audio")[0].addEventListener("timeupdate", function () {
        time = $("#audio")[0].currentTime;

        prog = ($("#audio")[0].currentTime / $("#audio")[0].duration) * 100 + "%";
        $("#progress").css("width", prog);

        var minute = time / 60;
        var minutes = parseInt(minute);

        if (minutes < 10)
            minutes = "0" + minutes;

        var second = time % 60;
        var seconds = Math.floor(second);

        if (seconds < 10)
            seconds = "0" + seconds;

        var disTime = minutes + ":" + seconds;

        if (disTime != $("#usedT").text())
            $("#usedT").text(disTime);

        if (playTime[1] - time <= 0.2) {
            localStorage.setItem("ToKillAMockingBirdTS", $("#audio")[0].currentTime);
            playTime.shift();

            var x = $("p[timestamp='" + playTime[0] + "']");
            scrollToEle(x[0]);
            $(".focus").removeClass("focus");
            x.addClass("focus");
        }
    })

    var btn = $("#audio-control > #btn");

    function grayAll() {
        $("p.sentence").css("color", "#a3b9ae");
        $("#article").addClass("audio-playing");
    }

    function ungrayAll() {
        $("p.sentence").css("color", "black");
        $("#article").removeClass("audio-playing");
    }

    function play() {
        $("#audio")[0].play();
        btn[0].classList = "play";
        btn[0].onclick = pause;
        grayAll();
    }

    function pause() {
        $("#audio")[0].pause();
        btn[0].classList = "pause";
        btn[0].onclick = play;
        ungrayAll();
    }

    btn.click(play);
}

/* Translate */

function translate_word(ele, word) {
    // SN word
    if (ele.classList.contains('word-sn')) {
        var sn = JSON.parse(ele.dataset.sn);
        translate_render_sn(sn, ele);
        return;
    }

    var url = `https://reading.baicizhan.com/api/query_word?word=${word}`;
    window.canContinue = true;
    $("#audio")[0].pause();
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: (data) => {
            var mean = data;
            translate_render_word(word, mean, ele);
        }
    });
}

function translate_render_word(word, mean, ele) {
    var cover = $("#cover");
    cover[0].innerHTML = `
    <div id="translate" onclick="event.stopPropagation()">
        <div id="translate-title">
            <h3 id="translate-word">${word}</h3>
            <div id="translate-audio">
                <div id="trans-audio-uk"></div>
                <div id="trans-audio-us"></div>
            </div>
        </div>
        <div id="translate-mean"></div>
    </div>
    `
    // render mean
    mean.mean_info.forEach(m => {
        var div = $("<div>");
        div.addClass('trans-mean');
        div[0].innerHTML = `
        <i>${m.type}</i>
        <span>${m.means}</span>
        `
        $("#translate-mean").append(div);
    })

    // render audio
    $("#trans-audio-uk")[0].innerHTML = `
        <audio id="uk-audio" src="${mean.audio_info.uk.audio}" hidden></audio>
        <span onclick="this.previousElementSibling.play()">${mean.audio_info.uk.accent}</span>
    `
    $("#trans-audio-us")[0].innerHTML = `
        <audio id="us-audio" src="${mean.audio_info.us.audio}" hidden></audio>
        <span onclick="this.previousElementSibling.play()">${mean.audio_info.us.accent}</span>
    `

    cover.show();

    // height
    var height = $("#translate")[0].offsetHeight;
    var top = ele.offsetTop - window.scrollY + ele.offsetHeight;
    if (top + height > window.innerHeight) {
        top = ele.offsetTop - window.scrollY - height;
    }

    $("#translate").css("top", top + "px");
}

function translate_phrase(ele, phrase) {
    var url = `https://reading.baicizhan.com/api/query_phrase?phrase_id=${phrase}`;
    window.canContinue = true;
    $("#audio")[0].pause();
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: (data) => {
            var mean = data.data;
            translate_render_phrase(mean, ele);
        }
    });
}



function translate_render_phrase(mean, ele) {
    var cover = $("#cover");
    cover[0].innerHTML = `
    <div id="translate" onclick="event.stopPropagation()">
        <div id="translate-title">
            <h3 id="translate-word">${mean.phrase}</h3>
        </div>
        <div id="translate-mean"></div>
    </div>
    `
    // render mean
    var div = $("<div>");
    div.addClass('trans-mean');
    div[0].innerHTML = `
        <span>${mean.mean}</span>
    `
    $("#translate-mean").append(div);

    cover.show();

    // height
    var height = $("#translate")[0].offsetHeight;
    var top = ele.offsetTop - window.scrollY + ele.offsetHeight;
    if (top + height > window.innerHeight) {
        top = ele.offsetTop - window.scrollY - height;
    }

    $("#translate").css("top", top + "px");
}

function translate_render_sn(sn, ele) {
    var cover = $("#cover");
    cover[0].innerHTML = `
    <div id="translate" onclick="event.stopPropagation()">
        <div id="translate-title">
            <h3 id="translate-word">${sn.lemma.word}</h3>
        </div>
        <div id="translate-mean">${sn.lemma.mean}</div>
        <div id="translate-desc">${sn.lemma.base_desc}</div>
        <div id="translate-tags"><span>${sn.culture_type}</span></div>
    </div>
    `
    cover.show();

    // height
    var height = $("#translate")[0].offsetHeight;
    var top = ele.offsetTop - window.scrollY + ele.offsetHeight;
    if (top + height > window.innerHeight) {
        top = ele.offsetTop - window.scrollY - height;
    }

    $("#translate").css("top", top + "px");
}
