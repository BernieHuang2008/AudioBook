import string
import json

target_json = {
    "article_info": {
        "id": 14467,
        "sentences": [
            {
                "id": 1137224,
                "sentence": "Chapter 1",
                "data": [
                    {
                        "word": "Chapter",
                        "style": [],
                        "type": 0,
                        "proper_noun_key": 0,
                        "phrase_id": 0,
                        "mean": "",
                    },
                    {"word": " ", "style": [], "type": 1},
                    {"word": "1", "style": []},
                ],
                "proper_noun_hash": {},
            }
        ],
        "previous": "",
        "intro": "",
        "audio_info": {
            "audio_info_by_speed": {
                "normal": {
                    "time_list": [
                        0.0,
                        51.57,
                        62.66,
                    ]
                }
            }
        },
        "previous_type": "Previous Story",
    },
    "problem_info": [],
}


def cvttime(time):
    # '00:13:53,650' -> 833.650
    time = time.split(",")
    time[0] = time[0].split(":")
    time = time[0] + [time[1]]
    res = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2]) + int(time[3]) / 1000

    return res


def convert(day):
    srtname = f"EN_prelude_to_foundation-{day}.srt"
    with open("C:/Users/BernieHuang/Downloads/" + srtname, "r") as f:
        lines = f.readlines()

    srt = []
    for i in range(0, len(lines), 4):
        time = lines[i + 1].split("-->")[0].strip()
        sentence = lines[i + 2].strip()
        srt.append((cvttime(time), sentence))

    sentences = []
    for s in srt:
        command = "merge"
        if s[1][0].isupper() and s[1][0] not in 'I':
            command = "new"
        elif sentences[-1]["sentence"].count(" ") >= 50:
            command = "new"

        if command == "new":
            sentences.append(
                {
                    "time": s[0],
                    "sentence": s[1],
                }
            )
        elif command == "merge":
            sentences[-1]["sentence"] += " " + s[1]

    datasentences = []
    for s in sentences:
        jso = {
            "sentence": s["sentence"],
            "data": [],
            "proper_noun_hash": {},
        }
        word = ""
        wordtype = 1

        def add_word(wd, t):
            if wd:
                jso["data"].append(
                    {
                        "word": wd,
                        "style": [],
                        "type": t,
                        "proper_noun_key": None,
                        "phrase_id": None,
                        "mean": "",
                    }
                )

        for w in s["sentence"]:
            if w.isalpha():
                word += w
                wordtype = 0
            elif w.isdigit():
                word += w
                wordtype = 1
            elif w == " ":
                add_word(word, wordtype)
                word = ""
                jso["data"].append({"word": " ", "style": [], "type": 1})
            elif w in string.punctuation:
                add_word(word, wordtype)
                word = ""
                jso["data"].append({"word": w, "style": [], "type": 2})

        add_word(word, wordtype)

        datasentences.append(jso)

    timelist = [s["time"] for s in sentences]

    datajson = target_json
    datajson["article_info"]["sentences"] = datasentences
    datajson["article_info"]["audio_info"]["audio_info_by_speed"]["normal"][
        "time_list"
    ] = timelist

    with open(f"books/prelude_to_foundation/data/{day}.json", "w") as f:
        json.dump(datajson, f, ensure_ascii=False, indent=4)


for i in range(1, 4 + 1):
    convert(i)
