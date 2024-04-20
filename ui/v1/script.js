const None = 0;

document.body.onkeydown = function (e) {
    var ne = String(Number(window.location.href.split("/Day%20")[1]) + 1);
    var pr = String(Number(window.location.href.split("/Day%20")[1]) - 1);
    var epr = $(".focus").previousSibling;
    var ene = $(".focus").nextSibling;

    if (e.keyCode == 32) { $("#btn").click(); return false; }
    if (e.keyCode == 38) { scrollToEle(nowfocus.previousSibling); nowfocus = nowfocus.previousSibling; return false; }
    if (e.keyCode == 40) { scrollToEle(nowfocus.nextSibling); nowfocus = nowfocus.nextSibling; return false; }
    if (e.keyCode == 37) { if ($("#btn").classList[0] == 'pause') { if (confirm("<-\nPrevious?")) window.location.href = `../Day ${pr}/Day ${pr}.html`; } else { playTime = bkPlayTime.slice(); xele = epr; audio.currentTime = Number(xele.dataset.timestamp); currt = 0; while ((currt = playTime.shift()) < Number(xele.dataset.timestamp)); playTime.unshift(currt); playTime.unshift(0); scrollToEle(xele); } }
    if (e.keyCode == 39) { if ($("#btn").classList[0] == 'pause') { if (confirm("->\nNext?")) window.location.href = `../Day ${ne}/Day ${ne}.html`; } else { xele = ene; audio.currentTime = Number(xele.dataset.timestamp); scrollToEle(xele); } }
    if (e.keyCode == 67) { SwitchClick($("#toggle-button").checked = !$("#toggle-button").checked); scrollToEle($(".focus")); }
    if (e.keyCode == 79) { $(".SwitchIcon").style.display = ($(".SwitchIcon").style.display == "none" ? "block" : "none"); }
    if (e.keyCode == 82) { speed(Number(prompt("New Speed:"))); }
}
function speed(s) { if (s) return audio.playbackRate = s; }
$("#progress").parentElement.onclick = function (e) {
    audio.currentTime = (e.clientX - this.offsetLeft - this.parentElement.offsetLeft) / this.offsetWidth * audio.duration;

    playTime = bkPlayTime.slice();
    while (playTime[1] < audio.currentTime)
        playTime.shift();

    var x = $("p[data-timestamp='" + playTime[0] + "']");
    scrollToEle(x);
    x.classList = "focus";

    if (prev)
        prev.classList = "";

    prev = x;
}

$("#audio-control").onclick = function (e) {
    if (window.innerHeight > window.innerWidth) {
        audio.currentTime = (e.clientX - this.offsetLeft - $("#progress").parentElement.offsetLeft) / $("#progress").parentElement.offsetWidth * audio.duration;

        playTime = bkPlayTime.slice();
        while (playTime[1] < audio.currentTime)
            playTime.shift();

        var x = $("p[data-timestamp='" + playTime[0] + "']");
        scrollToEle(x);
        x.classList = "focus";

        if (prev)
            prev.classList = "";

        prev = x;
    }
}

function $(s) {
    return document.querySelector(s);
}

audio = $("#audio");
audio.oncanplay = function () {
    var time = audio.duration;
    var minute = time / 60;
    var minutes = parseInt(minute);

    if (minutes < 10)
        minutes = "0" + minutes;

    var second = time % 60;
    var seconds = Math.round(second);

    if (seconds < 10)
        seconds = "0" + seconds;

    var totalT = minutes + ":" + seconds;
    $("#totalT").innerText = totalT;
}
function play() {
    audio.play();
    $("#btn").classList = "play";
    $("#btn").onclick = pause;
}
function pause() {
    audio.pause();
    $("#btn").classList = "pause";
    $("#btn").onclick = play;
}
function lastTime() {
    playTime = bkPlayTime.slice();
    var x;
    while ((x = playTime.shift()) < Number(localStorage.ToKillAMockingBirdTS));
    playTime.unshift(x);
    audio.currentTime = Number(localStorage.ToKillAMockingBirdTS);
    focus($("p[data-timestamp='" + playTime[0] + "']"));
}
function focus(x) {
    scrollToEle(x);
    x.classList = "focus";
    if (prev) prev.classList = "";
    prev = x;
}
var playTime = [];
var bkPlayTime = [];
var curr = -1;
function scrollToEle(x) {
    scrollTo(0, x.offsetTop - window.innerHeight / 2 + x.offsetHeight / 2)
}
var prev = null;
audio.addEventListener("timeupdate", function () {
    time = Math.floor(audio.currentTime);

    prog = (audio.currentTime / audio.duration) * 100 + "%";
    $("#progress").style.width = prog;

    var minute = time / 60;
    var minutes = parseInt(minute);

    if (minutes < 10)
        minutes = "0" + minutes;

    var second = time % 60;
    var seconds = Math.floor(second);

    if (seconds < 10)
        seconds = "0" + seconds;

    var disTime = minutes + ":" + seconds;

    $("#usedT").text(disTime);

    if (playTime[1] - time <= 0.2) {
        localStorage.setItem("ToKillAMockingBirdTS", audio.currentTime);
        playTime.shift();
        curr++;
        var x = $("p[data-timestamp='" + playTime[0] + "']");
        scrollToEle(x); x.classList = "focus";

        if (prev)
            prev.classList = "";

        prev = x;
        nowfocus = x;
    }
})
window.onload = function () {
    word_list_dict = {}
    for (var i = 0; i < word_list.length; i++) {
        word_list_dict[word_list[i].word] = word_list[i]
    }
    prev = $("p");
    nowfocus = prev;
    scrollToEle(prev);
    document.querySelectorAll("p").forEach(node => { playTime.push(Number(node.dataset.timestamp)); bkPlayTime.push(Number(node.dataset.timestamp)); })
    function tagChinese(strValue) {
        if (strValue != null && strValue != "") {
            var lst = strValue.match(/\([\u4e00-\u9fa5]*\)/g)
            if (lst) lst.forEach(s => {
                strValue = strValue.replace(s, "<cn>" + s + "</cn>")
            })
            return strValue;
        }
        else
            return "";
    }
    document.querySelectorAll("p").forEach(it => { it.innerHTML = tagChinese(it.innerText) });
}
function showCn() { $("style").innerText = "cn{display:inline-block;}" }
function hideCn() { $("style").innerText = "cn{display:none;}" }



var HttpClient = function () {
    this.get = function (aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function () {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open("GET", aUrl, true);
        anHttpRequest.send(null);
    }
}


function tran(str, fun) {
    str = str.trim();
    var tdict = JSON.parse(sessionStorage.transDict);
    if (word_list_dict[str.toLowerCase()]) {
        popReplace(`<h3 onclick='speech(this.innerText)'>` + word_list_dict[str.toLowerCase()].word + "</h3><text>" + word_list_dict[str.toLowerCase()].accent + "</text><br><text>" + word_list_dict[str.toLowerCase()].mean + "</text>", trans_e);
        document.body.onclick = function () {
            popOut();
            document.body.onclick = null;
        };
        return;
    }
    if (tdict[str.toLowerCase()]) {
        showTrans(str, tdict[str.toLowerCase()]);
        return;
    }
    var trans_appid = "20230130001543678";
    var trans_appkey = "ESo6MS7QBk4J9M2dglrN";
    var salt = Math.ceil(Math.random() * Math.random() * Math.pow(Math.random() * 10, Math.random() * 10) * 10000);
    var str1 = `${trans_appid}${str}${salt}${trans_appkey}`;
    var sign = md5(str1);
    var url = `https://api.fanyi.baidu.com/api/trans/vip/translate?q=${encodeURI(str)}&from=auto&to=zh&appid=${trans_appid}&salt=${salt}&sign=${sign}`;
    // var client = new HttpClient();
    // client.get(url,function(response){
    //     fun(response)
    // })
    var scriptDom = document.createElement("script");
    scriptDom.src = url + "&callback=" + fun.name;
    document.body.appendChild(scriptDom);
}
document.getElementsByTagName("body")[0].ondblclick = function (e) {
    text = window.getSelection().toString();
    if (text == '') {
        target = e.path[0];
        num = e.clientX / 16 - Number(target.parentElement.style.left.split("em")[0]);
        num = (num - 0.01 * num - 8 / 16) * 2.23
        str = "";
        start = Math.floor(num); end = start;
        while (target.innerText[start] != ' ' && start >= 0) start--;
        while (target.innerText[end] != ' ' && end < target.innerText.length) end++;
        if (start == end) {
            end++;
            while (target.innerText[end] != ' ' && end < target.innerText.length) end++;
        }
        text = target.innerText.substring(start, end)
    }
    popIn("<h3>Translating...</h3>", e);
    trans_e = e;
    tran(text, trans_recall);

    document.body.onclick = function () {
        popOut();
        document.body.onclick = null;
    };
    return false;
}

var trans_e = null;

if (!sessionStorage.transDict)
    sessionStorage.transDict = "{}";

function trans_recall(s) {
    var tdict = JSON.parse(sessionStorage.transDict);
    tdict[s["trans_result"][0]["src"].toLowerCase()] = s["trans_result"][0]["dst"];
    sessionStorage.transDict = JSON.stringify(tdict);
    showTrans(s["trans_result"][0]["src"], s["trans_result"][0]["dst"]);
}

function showTrans(origin, translated) {
    popReplace(`<h3 onclick='speech(this.innerText)'>` + origin + "</h3><text>" + translated + "</text>", trans_e);
    document.body.onclick = function () {
        popOut();
        document.body.onclick = null;
    };
}


document.getElementById('bubble').style.display = "none";

function popIn(s, e) {
    b = document.getElementById('bubble');
    b.innerHTML = s;
    b.style.display = "block";
    b.style.top = String(Math.max(e.clientY - b.offsetHeight - 20, 0)) + "px";
    b.style.left = String(Math.max(e.clientX - b.offsetWidth / 2, 0)) + "px";
    b.style.animationName = "bounceinB";
    setTimeout(function () {
        b.style.animationName = "";
    }, 200)
}

function popOut() {
    b = document.getElementById('bubble');
    b.style.animationName = "bounceoutB";
    setTimeout(function () {
        b.style.animationName = "";
        b.style.display = "none";
    }, 170)
}

function popReplace(s, e) {
    b = document.getElementById('bubble');
    b.innerHTML = s;
    b.style.display = "block";
    b.style.top = String(Math.max(e.clientY - b.offsetHeight - 20, 0)) + "px";
    b.style.left = String(Math.max(e.clientX - b.offsetWidth / 2, 0)) + "px";
}

function SwitchClick() {
    var onoffswitch = document.getElementById("toggle-button");
    if (onoffswitch.checked) {
        hideCn();
    }
    else {
        showCn();
    }
}


function speech(text) {
    var voice = speechSynthesis.getVoices().filter(x => x.lang === 'en-US')[5];
    var speech = new window.SpeechSynthesisUtterance(text);
    speech.rate = 1; // the speech rate, between 0.1 and 10, with 1 being the default
    speech.pitch = 1; // the speech pitch, between 0 and 2, with 1 being the default
    speech.lang = 'en-US';
    speech.voice = voice;
    window.speechSynthesis.speak(speech);
}


// MD5.js

!function (n) { "use strict"; function d(n, t) { var r = (65535 & n) + (65535 & t); return (n >> 16) + (t >> 16) + (r >> 16) << 16 | 65535 & r } function f(n, t, r, e, o, u) { return d((u = d(d(t, n), d(e, u))) << o | u >>> 32 - o, r) } function l(n, t, r, e, o, u, c) { return f(t & r | ~t & e, n, t, o, u, c) } function g(n, t, r, e, o, u, c) { return f(t & e | r & ~e, n, t, o, u, c) } function v(n, t, r, e, o, u, c) { return f(t ^ r ^ e, n, t, o, u, c) } function m(n, t, r, e, o, u, c) { return f(r ^ (t | ~e), n, t, o, u, c) } function c(n, t) { var r, e, o, u; n[t >> 5] |= 128 << t % 32, n[14 + (t + 64 >>> 9 << 4)] = t; for (var c = 1732584193, f = -271733879, i = -1732584194, a = 271733878, h = 0; h < n.length; h += 16)c = l(r = c, e = f, o = i, u = a, n[h], 7, -680876936), a = l(a, c, f, i, n[h + 1], 12, -389564586), i = l(i, a, c, f, n[h + 2], 17, 606105819), f = l(f, i, a, c, n[h + 3], 22, -1044525330), c = l(c, f, i, a, n[h + 4], 7, -176418897), a = l(a, c, f, i, n[h + 5], 12, 1200080426), i = l(i, a, c, f, n[h + 6], 17, -1473231341), f = l(f, i, a, c, n[h + 7], 22, -45705983), c = l(c, f, i, a, n[h + 8], 7, 1770035416), a = l(a, c, f, i, n[h + 9], 12, -1958414417), i = l(i, a, c, f, n[h + 10], 17, -42063), f = l(f, i, a, c, n[h + 11], 22, -1990404162), c = l(c, f, i, a, n[h + 12], 7, 1804603682), a = l(a, c, f, i, n[h + 13], 12, -40341101), i = l(i, a, c, f, n[h + 14], 17, -1502002290), c = g(c, f = l(f, i, a, c, n[h + 15], 22, 1236535329), i, a, n[h + 1], 5, -165796510), a = g(a, c, f, i, n[h + 6], 9, -1069501632), i = g(i, a, c, f, n[h + 11], 14, 643717713), f = g(f, i, a, c, n[h], 20, -373897302), c = g(c, f, i, a, n[h + 5], 5, -701558691), a = g(a, c, f, i, n[h + 10], 9, 38016083), i = g(i, a, c, f, n[h + 15], 14, -660478335), f = g(f, i, a, c, n[h + 4], 20, -405537848), c = g(c, f, i, a, n[h + 9], 5, 568446438), a = g(a, c, f, i, n[h + 14], 9, -1019803690), i = g(i, a, c, f, n[h + 3], 14, -187363961), f = g(f, i, a, c, n[h + 8], 20, 1163531501), c = g(c, f, i, a, n[h + 13], 5, -1444681467), a = g(a, c, f, i, n[h + 2], 9, -51403784), i = g(i, a, c, f, n[h + 7], 14, 1735328473), c = v(c, f = g(f, i, a, c, n[h + 12], 20, -1926607734), i, a, n[h + 5], 4, -378558), a = v(a, c, f, i, n[h + 8], 11, -2022574463), i = v(i, a, c, f, n[h + 11], 16, 1839030562), f = v(f, i, a, c, n[h + 14], 23, -35309556), c = v(c, f, i, a, n[h + 1], 4, -1530992060), a = v(a, c, f, i, n[h + 4], 11, 1272893353), i = v(i, a, c, f, n[h + 7], 16, -155497632), f = v(f, i, a, c, n[h + 10], 23, -1094730640), c = v(c, f, i, a, n[h + 13], 4, 681279174), a = v(a, c, f, i, n[h], 11, -358537222), i = v(i, a, c, f, n[h + 3], 16, -722521979), f = v(f, i, a, c, n[h + 6], 23, 76029189), c = v(c, f, i, a, n[h + 9], 4, -640364487), a = v(a, c, f, i, n[h + 12], 11, -421815835), i = v(i, a, c, f, n[h + 15], 16, 530742520), c = m(c, f = v(f, i, a, c, n[h + 2], 23, -995338651), i, a, n[h], 6, -198630844), a = m(a, c, f, i, n[h + 7], 10, 1126891415), i = m(i, a, c, f, n[h + 14], 15, -1416354905), f = m(f, i, a, c, n[h + 5], 21, -57434055), c = m(c, f, i, a, n[h + 12], 6, 1700485571), a = m(a, c, f, i, n[h + 3], 10, -1894986606), i = m(i, a, c, f, n[h + 10], 15, -1051523), f = m(f, i, a, c, n[h + 1], 21, -2054922799), c = m(c, f, i, a, n[h + 8], 6, 1873313359), a = m(a, c, f, i, n[h + 15], 10, -30611744), i = m(i, a, c, f, n[h + 6], 15, -1560198380), f = m(f, i, a, c, n[h + 13], 21, 1309151649), c = m(c, f, i, a, n[h + 4], 6, -145523070), a = m(a, c, f, i, n[h + 11], 10, -1120210379), i = m(i, a, c, f, n[h + 2], 15, 718787259), f = m(f, i, a, c, n[h + 9], 21, -343485551), c = d(c, r), f = d(f, e), i = d(i, o), a = d(a, u); return [c, f, i, a] } function i(n) { for (var t = "", r = 32 * n.length, e = 0; e < r; e += 8)t += String.fromCharCode(n[e >> 5] >>> e % 32 & 255); return t } function a(n) { var t = []; for (t[(n.length >> 2) - 1] = void 0, e = 0; e < t.length; e += 1)t[e] = 0; for (var r = 8 * n.length, e = 0; e < r; e += 8)t[e >> 5] |= (255 & n.charCodeAt(e / 8)) << e % 32; return t } function e(n) { for (var t, r = "0123456789abcdef", e = "", o = 0; o < n.length; o += 1)t = n.charCodeAt(o), e += r.charAt(t >>> 4 & 15) + r.charAt(15 & t); return e } function r(n) { return unescape(encodeURIComponent(n)) } function o(n) { return i(c(a(n = r(n)), 8 * n.length)) } function u(n, t) { return function (n, t) { var r, e = a(n), o = [], u = []; for (o[15] = u[15] = void 0, 16 < e.length && (e = c(e, 8 * n.length)), r = 0; r < 16; r += 1)o[r] = 909522486 ^ e[r], u[r] = 1549556828 ^ e[r]; return t = c(o.concat(a(t)), 512 + 8 * t.length), i(c(u.concat(t), 640)) }(r(n), r(t)) } function t(n, t, r) { return t ? r ? u(t, n) : e(u(t, n)) : r ? o(n) : e(o(n)) } "function" == typeof define && define.amd ? define(function () { return t }) : "object" == typeof module && module.exports ? module.exports = t : n.md5 = t }(this);
//# sourceMappingURL=md5.min.js.map




