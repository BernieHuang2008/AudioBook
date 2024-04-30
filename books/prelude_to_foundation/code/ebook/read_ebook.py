from bs4 import BeautifulSoup
import json


def read_contents():
    chapters = [f"part{i}.xhtml" for i in range(2, 51)]

    return chapters


def tokenify(text, style=[]):
    res = []

    def add_word(wd, t):
        if wd:
            res.append(
                {
                    "word": wd,
                    "style": style,
                    "type": t,
                    "proper_noun_key": None,
                    "phrase_id": None,
                    "mean": "",
                }
            )

    word = ""
    wordtype = 0
    for w in text:
        if w.isalpha():
            word += w
            wordtype = 0
        elif w.isdigit():
            word += w
            wordtype = 1
        elif w == " ":
            add_word(word, wordtype)
            word = ""
            res.append({"word": " ", "style": style, "type": 1})
        elif w in ".!?;:~)]}>—’”‘“'\"*([{&-_>~":
            add_word(word, wordtype)
            word = ""
            res.append({"word": w, "style": style, "type": 2})

    add_word(word, wordtype)

    return res


def read_chapter(f_chapter):

    with open(f"books/prelude_to_foundation/ebook/xhtml/{f_chapter}") as f:
        chapter = BeautifulSoup(f.read(), "html.parser")

    paragraphs = chapter.select("p")

    # tokenify the head
    p_token = []
    for p in paragraphs:
        tokens = []
        for c in p.children:
            if c.name == "i":
                tokens += tokenify(c.text, ["i"])
            elif c.name == "b":
                tokens += tokenify(c.text, ["b"])
            else:
                tokens += tokenify(c.text)
        p_token.append(tokens)

    return p_token


def split_sentence(tokens):
    sentences = []

    for paragraph in tokens:
        # about 50 words per sentence

        last = 0
        for i in range(len(paragraph)):
            t = paragraph[i]
            if i - last >= 50 and t["type"] == 2 and t["word"] in ".!?;:~)]}>—’”":
                # end-of-sentence punctuations met
                sentences.append(paragraph[last : i + 1])
                last = i + 1

        # deal with the rest of paragraph
        if last == 0:
            sentences.append(paragraph)
        elif last < len(paragraph):
            if len(paragraph) - last <= 15:
                sentences[-1] += paragraph[last:]
            else:
                sentences.append(paragraph[last:])

    return sentences


def cvttime(time):
    # '00:13:53,650' -> 833.650
    time = time.split(",")
    time[0] = time[0].split(":")
    time = time[0] + [time[1]]
    res = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2]) + int(time[3]) / 1000

    return res


def similar(a, b):
    # 计算最小修改距离
    # 初始化dp数组
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    # 初始化边界条件
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    # 动态规划计算最小编辑距离
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len(a)][len(b)]


def find_same(qa, qb, ia, ib, WINDOW_SIZEa, WINDOW_SIZEb):
    qbm = [x["word"] for x in qb]

    choices = []
    for jb in range(WINDOW_SIZEb):
        for ja in range(WINDOW_SIZEa):
            if (
                similar(
                    qa[(ia + ja + 1) % WINDOW_SIZEa].lower(),
                    qbm[(ib + jb + 1) % WINDOW_SIZEb].lower(),
                )
                < 3
                and len(qbm[(ib + jb + 1) % WINDOW_SIZEb]) >= 5
            ):
                # 正数第j个元素
                choices.append(
                    (
                        ja,
                        jb,
                        qbm[(ib + jb + 1) % WINDOW_SIZEb],
                    )
                )
            # print(qbm[(ib + jb + 1) % WINDOW_SIZEb], qa[(ia + ja + 1) % WINDOW_SIZEa])

    if choices:
        return min(choices, key=lambda x: x[0] + x[1] / 2)
    print("".join(qa[ia:] + qa[:ia]), "".join(qbm[ib:] + qbm[:ib]), ia, ib)
    raise ValueError("No same element found")


def reformat_sentence(sentences):
    # reformat sentences
    res = []
    for s in sentences:
        tokens = s
        res.append(
            {
                "id": 0,
                "sentence": "".join([x["word"] for x in tokens]),
                "data": tokens,
                "proper_noun_hash": {},
            }
        )

    return res


def attatch_timestamp(sentences, srt_bias: int = 0):
    ts = []

    # read srt files
    srt = []

    for i in range(1, 15):
        fname = f"C:/Users/BernieHuang/Downloads/prelude_to_foundation-{i}.srt"
        with open(fname, "r") as f:
            while f.readline():  # text id: ignore
                time = cvttime(f.readline().split("-->")[0].strip())
                sentence = f.readline().strip()
                f.readline()  # empty line: ignore
                srt.append((time, sentence))

    # merge timestamp
    i = 0
    srt_add = srt_bias
    srt_round = 0
    srt_last = ""
    while i < len(sentences):
        s1 = sentences[i]["sentence"]
        s2 = srt_last + srt[i + srt_add][1]
        for j in range(srt_round):
            s2 = srt[i + srt_add - j - 1][1] + "" + s2
        if srt_last and srt_round == -1:
            srt_round = 0
            s2 = srt_last
            srt_add -= 1

        # if i==50:
        #     print(i, "False")
        #     print(s1)
        #     print(s2)
        #     0/0
        if i <= 283:
            delta = 0.08
        else:
            delta = -0.05

        if similar(s1, s2) < 7:
            # if two sentences are similar, merge the timestamp
            ts.append(srt[i + srt_add - srt_round][0] - delta)
            print(i, "True")
            srt_round = 0
            srt_last = ""
        # elif srt_round == 1:
        #     print(i, "False")
        #     print(s1)
        #     print(s2)
        #     0 / 0
        elif len(s2) - len(s1) > 7:
            # if srt is longer than the sentence, cut the srt
            ts.append(srt[i + srt_add - srt_round][0] - delta)
            print(i, "True")
            srt_round = -1
            srt_last = s2[len(s1) :]
        else:
            srt_add += 1
            srt_round += 1
            continue

        i += 1

    return ts


def split_ts(ts):
    res = []

    curr = 0
    last = 0
    while curr < len(ts):
        if ts[curr] < ts[last]:
            # means a new chapter
            res.append(ts[last:curr])
            last = curr
        curr += 1

    return res


def output(chap, s, ts):
    datajson = {
        "article_info": {
            "id": 14467,
            "sentences": [],
            "previous": "",
            "intro": "",
            "audio_info": {"audio_info_by_speed": {"normal": {"time_list": []}}},
            "previous_type": "Previous Story",
        },
        "problem_info": [],
    }
    datajson["article_info"]["sentences"] = s
    datajson["article_info"]["audio_info"]["audio_info_by_speed"]["normal"][
        "time_list"
    ] = ts

    with open(f"books/prelude_to_foundation/data/{chap}.json", "w") as f:
        json.dump(datajson, f)


contents = read_contents()

"""Auto attatch tts timestamp"""
# for chap in range(len(contents)):
#     chapter_token = read_chapter(contents[chap])
#     sentences = split_sentence(chapter_token)
#     sentences = reformat_sentence(sentences)
#     output(chap+1, sentences, [1000000 for _ in range(len(sentences))])

"""Read full text"""
# full_txt = ""
# for chap in range(len(contents)):
#     chapter_token = read_chapter(contents[chap])
#     sentences = split_sentence(chapter_token)
#     txt = '\n'.join([''.join([x['word'] for x in s]) for s in sentences])
#     full_txt += txt
#
# with open("books/prelude_to_foundation/data/full.txt", "w") as f:
#     f.write(full_txt)

"""Attatch timestamp"""
sents = []
full_sent = []
for chap in range(len(contents)):
    day = chap + 1
    chapter_token = read_chapter(contents[chap])
    sentences = split_sentence(chapter_token)
    sentences = reformat_sentence(sentences)
    sents.append(sentences)
    full_sent += sentences

full_ts = attatch_timestamp(full_sent, 0)
ts = split_ts(full_ts)
for day in range(1, 50):
    output(day, sents[day - 1], ts[day - 1])
