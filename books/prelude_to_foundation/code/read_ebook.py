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


def attatch_timestamp(sentences):

    # reformat sentences, by the way
    res = []
    for s in sentences:
        tokens = s
        res.append(
            {
                "id": 0,
                "data": tokens,
                "proper_noun_hash": {},
            }
        )

    # read all srt files
    srt = []
    for i in range(1, 5):
        fname = (
            f"F:\\Data Set\\L\\000036\\audiobook\\srt\\prelude_to_foundation-{i}.srt"
        )
        with open(fname, "r") as f:
            while f.readline():  # text id: ignore
                time = cvttime(f.readline().split("-->")[0].strip())
                sentence = f.readline().strip()
                f.readline()  # empty line: ignore
                srt.append((time, sentence.split(" ")))

    WINDOW_SIZE_SRT = 30
    WINDOW_SIZE_EBK = WINDOW_SIZE_SRT * 3

    ts = []
    tail_srt = [0, 0]
    tail_ebk = [0, 0]
    window_srt = [""] * WINDOW_SIZE_SRT
    window_srt_i = -1
    window_ebk = [{"word": ""}] * WINDOW_SIZE_EBK
    window_ebk_i = -1

    def fillq(x):
        nonlocal window_srt_i, window_ebk_i
        if x == "srt":
            # queue push
            window_srt_i += 1
            window_srt_i %= WINDOW_SIZE_SRT
            window_srt[window_srt_i] = srt[tail_srt[0]][1][tail_srt[1]]

            tail_srt[1] += 1
            if tail_srt[1] >= len(srt[tail_srt[0]][1]):
                tail_srt[0] += 1
                tail_srt[1] = 0
        if x == "ebk":
            window_ebk_i += 1
            window_ebk_i %= WINDOW_SIZE_EBK
            if tail_ebk[0] >= len(sentences):
                return True

            window_ebk[window_ebk_i] = sentences[tail_ebk[0]][tail_ebk[1]]

            tail_ebk[1] += 1
            if tail_ebk[1] >= len(sentences[tail_ebk[0]]):
                tail_ebk[0] += 1
                tail_ebk[1] = 0

    def popq(i, j):
        for _ in range(i + 1):
            if fillq("srt"):
                return True
        for _ in range(j + 1):
            if fillq("ebk"):
                return True

    popq(WINDOW_SIZE_SRT - 1, WINDOW_SIZE_EBK - 1)
    while 1:
        i, j, s = find_same(
            window_srt,
            window_ebk,
            window_srt_i,
            window_ebk_i,
            WINDOW_SIZE_SRT,
            WINDOW_SIZE_EBK,
        )
        print(tail_srt, s)
        if abs(i - j / 2) > 20:
            window_ebk = list(map(lambda x: x["word"], window_ebk))
            w_srt = window_srt[window_srt_i:] + window_srt[:window_srt_i]
            w_ebk = window_ebk[window_ebk_i:] + window_ebk[:window_ebk_i]

            print(
                w_srt[i],
                "\n",
                w_ebk[j],
                "\n",
                " ".join(w_srt[:i] + [f"\033[1;34m{w_srt[i]}\033[0m"] + w_srt[i + 1 :]),
                "\n",
                "".join(w_ebk[:j] + [f"\033[1;34m{w_ebk[j]}\033[0m"] + w_ebk[j + 1 :]),
                i,
                j,
            )
            raise ValueError("No same element found")

        same_index_ebk = [tail_ebk[0], tail_ebk[1] - (10 - j)]
        while same_index_ebk[1] < 0:
            same_index_ebk[0] -= 1
            same_index_ebk[1] += len(sentences[same_index_ebk[0]])

        if len(ts) > same_index_ebk[0]:
            # already have timestamp
            if popq(i, j):
                return res, ts
            continue

        same_index_srt = [tail_srt[0], tail_srt[1] - (10 - i) - same_index_ebk[1]]
        while same_index_srt[1] < 0:
            same_index_srt[0] -= 1
            same_index_srt[1] += len(srt[same_index_srt[0]][1])

        if (
            same_index_srt[1] < len(srt[same_index_srt[0]][1]) // 2
            and ts
            and ts[-1] < srt[same_index_srt[0]][0]
        ):
            # close to the start of the srt
            ts.append(srt[same_index_srt[0]][0])
            if popq(i, j):
                return res, ts
        else:
            ts.append(srt[same_index_srt[0] + 1][0])
            if popq(i, j):
                return res, ts

    return res, ts


def output(s, ts):
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

    with open("data.json", "w") as f:
        json.dump(datajson, f)


contents = read_contents()
chapter_token = read_chapter(contents[0])
sentences = split_sentence(chapter_token)
sentences, ts = attatch_timestamp(sentences)
output(sentences, ts)
