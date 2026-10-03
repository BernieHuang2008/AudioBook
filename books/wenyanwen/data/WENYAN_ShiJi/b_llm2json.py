import json

# 标点符号集合
PUNCT = set("，。！？：；、“”‘’（）《》〈〉【】—…·,.!?;:\"'()[]")


def flush_buf(buf, data_items):
    """将缓冲区中的普通词加入 data_items"""
    if buf:
        word = ''.join(buf)
        data_items.append({"word": word, "type": 0})
        buf.clear()


def parse_annotated_text(text):
    """
    解析形如：词<释义>标点 的文言文注解文本。
    返回 data 数组，每个元素为 {word, type, mean?}
    type: 0 普通词，1 空格，2 标点
    """
    data_items = []
    buf = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # 遇到 <释义>
        if ch == '<':
            j = text.find('>', i + 1)
            if j == -1:
                buf.append(ch)
                i += 1
                continue

            word = ''.join(buf).strip()
            buf.clear()
            mean2 = text[i + 1:j]
            if word:
                data_items.append({"word": word, "type": 0, "mean2": mean2})
            i = j + 1
            continue

        # 跳过 [ ] 方括号，但保留其中的 <释义> 内容
        if ch in ('[', ']'):
            flush_buf(buf, data_items)
            i += 1
            continue

        # 跳过 ( ) 圆括号内的整词注释
        if ch == '(':
            flush_buf(buf, data_items)
            depth = 1
            i += 1
            while i < n and depth > 0:
                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    depth -= 1
                i += 1
            continue

        # 标点
        if ch in PUNCT:
            flush_buf(buf, data_items)
            data_items.append({"word": ch, "type": 2})
            i += 1
            continue

        # 空白字符（空格、换行等）统一转为空格
        if ch.isspace():
            flush_buf(buf, data_items)
            data_items.append({"word": " ", "type": 1})
            i += 1
            continue

        # 普通字符
        buf.append(ch)
        i += 1

    flush_buf(buf, data_items)
    return data_items


def empty_audio_speed():
    """单个速度档位的空音频结构"""
    return {
        "audio_name": "",
        "time_list": [],
        "audio_url": ""
    }


def empty_audio_info():
    """完整的空音频信息结构"""
    return {
        "audio_name": "",
        "time_list": [],
        "audio_url": "",
        "audio_info_by_speed": {
            "new_slow": empty_audio_speed(),
            "slow": empty_audio_speed(),
            "normal": empty_audio_speed(),
            "fast": empty_audio_speed(),
            "new_fast": empty_audio_speed()
        }
    }


def convert(annotated_text):
    """将文言文注解文本转换为标准 JSON 结构"""
    paragraphs = annotated_text.strip().replace("\r\n", "\n").split("\n\n")
    sid = 0

    def process_paragraph(paragraph):
        nonlocal sid

        if "\n" in paragraph:
            origin, translation = paragraph.split("\n", 1)
            data_items = parse_annotated_text(paragraph.replace("\r\n", "\n").strip())
            data_items[-1]["mean"] = translation     # 在最后一个词条中添加译文作为 mean 字段
        else:
            origin = paragraph
            data_items = parse_annotated_text(origin)
        
        sid += 1
        return {
                "id": sid,
                "sentence": origin,
                "data": data_items,
                "sentence_mean": None,
                "explanation_ids": [],
                "sentence_combination_id": None,
                "sentence_analysis": [],
                "types": [],
                "pic_name": "",
                "phrases": {},
                "sentence_analysis_phrase": [],
                "proper_noun_hash": {},
                "pic_url": ""
            }

    sentences = list(map(process_paragraph, paragraphs))
    
    result = {
        "article_info": {
            "id": 0,
            "mode": "WENYAN",
            "sentences": sentences,
            "previous": "",
            "intro": "",
            "audio_list": {},                 # 音频列表：保留字段，空对象
            "words_count": 0,
            "plots": "",
            "paragraph": [],
            "previous_type": "Previous Story",
            "share_words": "",
            "article_title_en": "Day 1",
            "show_annotation": True,
            "plot_cdn_name": None,
            "relationship_cdn_name": None,
            "source": "day1",
            "content_version": "原版",
            "is_external": 0,
            "article_title": "Chapter 1",
            "preload_audio": "",              # 预加载音频：保留字段，空字符串
            "audio_info": empty_audio_info(), # 当前音频详细信息：保留完整空结构
            "notes": {
                "sid_to_note_ids": {},
                "note_info": {},
                "note_ids": {}
            },
            "has_next_chapter": False
        },
        "course_info": {
            "course_id": 0,
            "is_course_finish": False,
            "learn_book_count": 1,
            "course_type": 0
        },
        "user_course_info": {
            "id": 0,
            "can_read_smooth": False,
            "open_annotation": True,
            "can_query_phrase": False,
            "show_buy_vip": False,
            "reading_done": False,
            "learn_start_day": "",
            "current_learn_day": 1
        },
        "book_info": {
            "book_id": 0,
            "chapter_count": 1,
            "book_name": "文言文阅读",
            "book_name_cn": "文言文阅读",
            "book_cover_img_url": "",
            "bid": 0,
            "current_chapter": 1,
            "teacher_notes_url": "",
            "is_periodical": False,
            "periodical_list": []
        },
        "share_img_url": "",
        "student_vocabularies": [],
        "preview_finished": False
    }

    return result


if __name__ == "__main__":
    # 将文言文注解文本保存为 input.txt，然后运行本脚本
    with open("input.txt", "r", encoding="utf-8") as f:
        annotated_text = f.read()

    json_data = convert(annotated_text)
    # print(json.dumps(json_data, ensure_ascii=False, indent=2))
    output_file = "output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)
