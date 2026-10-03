# JSON 结构解析文档

本文档解析所给 JSON 的整体结构。该 JSON 是《哈利·波特与魔法石》第一章 “Day 1” 的阅读数据，包含正文、逐词数据、专有名词解释、音频时间轴、笔记、课程信息和书籍信息等。

---

## 1. 顶层结构

顶层是一个 JSON 对象，包含 7 个一级字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `article_info` | Object | 文章正文、音频、笔记等核心数据 |
| `course_info` | Object | 课程信息 |
| `user_course_info` | Object | 用户学习状态 |
| `book_info` | Object | 书籍信息 |
| `share_img_url` | String | 分享图片地址 |
| `student_vocabularies` | Array | 学生词汇，当前为空数组 |
| `preview_finished` | Boolean | 是否完成预览 |

树形总览：

```json
{
  "article_info": { ... },
  "course_info": { ... },
  "user_course_info": { ... },
  "book_info": { ... },
  "share_img_url": "https://...",
  "student_vocabularies": [],
  "preview_finished": false
}
```

---

## 2. `article_info` 结构

`article_info` 是核心对象，保存文章正文及阅读辅助数据。

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | Number | 文章 ID，例如 `13531` |
| `mode` | String | 文章的解析，如 `"ENGLISH"`英语文章 或 `"WENYAN"`文言文文章 |
| `sentences` | Array | 句子对象数组，正文核心 |
| `previous` | String | 前情提要 |
| `intro` | String | 简介，当前为空 |
| `audio_list` | Object | 音频列表 |
| `words_count` | Number | 字数统计 |
| `plots` | String | 情节信息，当前为空 |
| `paragraph` | Array | 段落信息，当前为空 |
| `previous_type` | String | 前情类型，如 `"Previous Story"` |
| `share_words` | String | 分享句 |
| `article_title_en` | String | 英文标题，如 `"Day 1"` |
| `show_annotation` | Boolean | 是否显示注释 |
| `plot_cdn_name` | Null | 情节 CDN 名称 |
| `relationship_cdn_name` | Null | 关系 CDN 名称 |
| `source` | String | 来源，如 `"day1"` |
| `content_version` | String | 内容版本，如 `"原版"` |
| `is_external` | Number | 是否外部内容，`0` 表示否 |
| `article_title` | String | 文章标题，如 `"Chapter 1"` |
| `preload_audio` | String | 预加载音频地址 |
| `audio_info` | Object | 当前音频详细信息 |
| `notes` | Object | 笔记信息 |
| `has_next_chapter` | Boolean | 是否有下一章 |

---

## 3. `sentences` 句子数组

`sentences` 是数组，每个元素是一个句子对象。句子对象结构如下：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | Number | 句子 ID |
| `sentence` | String | 句子原文 |
| `data` | Array | 逐词/空格/标点拆分数据 |
| `sentence_mean` | Null/String | 句子翻译或释义，当前多为 `null` |
| `explanation_ids` | Array | 解释 ID 列表 |
| `sentence_combination_id` | Null | 句子组合 ID |
| `sentence_analysis` | Array | 句子分析 |
| `types` | Array | 句子类型，如 `["title_h1"]` |
| `pic_name` | String | 图片名 |
| `phrases` | Object | 短语信息 |
| `sentence_analysis_phrase` | Array | 句子分析短语 |
| `proper_noun_hash` | Object | 专有名词哈希表 |
| `pic_url` | String | 图片地址 |
| `means` | Array | 可选字段，部分句子有，样本中多为空数组 |

示例句子对象简化结构：

```json
{
  "id": 1086927,
  "sentence": "Mr and Mrs Dursley...",
  "data": [ ... ],
  "sentence_mean": null,
  "explanation_ids": [],
  "sentence_combination_id": null,
  "sentence_analysis": [],
  "types": [],
  "pic_name": "",
  "phrases": {},
  "sentence_analysis_phrase": [],
  "proper_noun_hash": { ... },
  "pic_url": ""
}
```

---

## 4. `data` 逐词数据数组

每个句子的 `data` 字段是一个数组，用于把句子拆成可交互的单词、空格和标点。

| 字段 | 类型 | 说明 |
|---|---|---|
| `word` | String | 单词、空格或标点 |
| `type` | Number | 数据类型，样本中为 `0`、`1`、`2` |
| `style` | Array | 可选，样式，如 `["i"]` 表示斜体 |
| `mean` | String | 可选，中文释义或注释，将以（）形式显示 |
| `mean2` | String | 可选，中文释义或注释，将在双击时作为第一释义显示在弹出窗口中 |
| `proper_noun_key` | String | 可选，关联 `proper_noun_hash` 的键 |
| `phrase_id` | Number | 可选，关联短语 ID |

根据样本推断：

| `type` 值 | 含义 |
|---|---|
| `0` | 普通单词或文本 |
| `1` | 空格 |
| `2` | 标点符号或特殊符号 |

示例：

```json
{
  "word": "Privet",
  "type": 0,
  "mean": "女贞",
  "proper_noun_key": "2"
}
```

---

## 5. `proper_noun_hash` 专有名词表

当 `data` 中的词带有 `proper_noun_key` 时，可通过该键在句子的 `proper_noun_hash` 中找到对应解释。

结构：

```json
{
  "2": {
    "proper_type": "culture",
    "culture_type": "地名场所",
    "lemma": {
      "word": "Privet Drive",
      "mean": "女贞路",
      "base_desc": "女贞路位于英国萨里郡的小惠金区...",
      "extend_desc": "",
      "image_url": ""
    },
    "base": null
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `proper_type` | String | 专有名词类型，样本中为 `"culture"` |
| `culture_type` | String | 文化分类，如 `人物`、`地名场所`、`魔法生物`、`魔法制品`、`日常生活` |
| `lemma` | Object | 词条信息 |
| `lemma.word` | String | 专有名词原文 |
| `lemma.mean` | String | 中文译名 |
| `lemma.base_desc` | String | 基础描述 |
| `lemma.extend_desc` | String | 扩展描述 |
| `lemma.image_url` | String | 图片地址 |
| `base` | Null | 基础信息，样本中多为 `null` |

---

## 6. `notes` 笔记结构

`notes` 保存用户笔记与句子的关联。

```json
{
  "sid_to_note_ids": {
    "1087018": [8540355]
  },
  "note_info": {
    "8540355": {
      "mark": 1,
      "comment": 0
    }
  },
  "note_ids": {
    "1087018": 8540355
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `sid_to_note_ids` | Object | 句子 ID 到笔记 ID 数组的映射 |
| `note_info` | Object | 笔记详细信息 |
| `note_info[noteId].mark` | Number | 标记状态 |
| `note_info[noteId].comment` | Number | 评论数或评论状态 |
| `note_ids` | Object | 句子 ID 到笔记 ID 的简化映射 |

---

## 7. 音频结构

`article_info` 中有两个音频相关字段：`audio_list` 和 `audio_info`。

### 7.1 `audio_list`

`audio_list` 是对象，键为音频档位标识，例如 `"3"`、`"4"`、`"6"`、`"9"`、`"10"`。

每个值包含：

| 字段 | 类型 | 说明 |
|---|---|---|
| `audio_name` | String | 音频文件名 |
| `time_list` | Array | 时间点数组，通常与句子时间轴对应 |

### 7.2 `audio_info`

`audio_info` 是当前音频的详细信息：

| 字段 | 类型 | 说明 |
|---|---|---|
| `audio_name` | String | 音频文件名 |
| `time_list` | Array | 时间点数组 |
| `audio_url` | String | 音频地址 |
| `audio_info_by_speed` | Object | 不同速度的音频信息 |

`audio_info_by_speed` 包含：

| 字段 | 说明 |
|---|---|
| `new_slow` | 新慢速 |
| `slow` | 慢速 |
| `normal` | 正常速度 |
| `fast` | 快速 |
| `new_fast` | 新快速 |

每个速度对象包含 `audio_name`、`time_list`、`audio_url`。

`time_list` 用于音频播放时定位句子，例如高亮当前朗读句子。

---

## 8. 其他顶层对象

### 8.1 `course_info`

| 字段 | 类型 | 说明 |
|---|---|---|
| `course_id` | Number | 课程 ID |
| `is_course_finish` | Boolean | 课程是否完成 |
| `learn_book_count` | Number | 学习书籍数量 |
| `course_type` | Number | 课程类型 |

### 8.2 `user_course_info`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | Number | 用户课程 ID |
| `can_read_smooth` | Boolean | 是否可流畅阅读 |
| `open_annotation` | Boolean | 是否开启注释 |
| `can_query_phrase` | Boolean | 是否可查询短语 |
| `show_buy_vip` | Boolean | 是否显示购买 VIP |
| `reading_done` | Boolean | 阅读是否完成 |
| `learn_start_day` | String | 开始学习日期 |
| `current_learn_day` | Number | 当前学习天数 |

### 8.3 `book_info`

| 字段 | 类型 | 说明 |
|---|---|---|
| `book_id` | Number | 书籍 ID |
| `chapter_count` | Number | 章节数 |
| `book_name` | String | 英文书名 |
| `book_name_cn` | String | 中文书名 |
| `book_cover_img_url` | String | 封面图地址 |
| `bid` | Number | 业务 ID |
| `current_chapter` | Number | 当前章节 |
| `teacher_notes_url` | String | 老师笔记地址 |
| `is_periodical` | Boolean | 是否为期刊 |
| `periodical_list` | Array | 期刊列表 |

---

## 9. 数据关系

核心关系如下：

```text
article_info.sentences[]
  ├── sentence          句子原文
  ├── data[]            逐词拆分
  │   ├── word
  │   ├── type
  │   ├── mean
  │   ├── mean2
  │   ├── proper_noun_key ──► proper_noun_hash[key]
  │   └── phrase_id ──► 短语信息
  ├── proper_noun_hash  专有名词解释
  └── id ──► notes.sid_to_note_ids
```

音频关系：

```text
article_info.audio_info.audio_info_by_speed.*.time_list
  └── 与 sentences 的时间轴对应
```

课程与书籍关系：

```text
course_info + user_course_info + book_info
  └── 提供学习进度、课程状态、书籍元信息
```

---

## 10. 简化示例

```json
{
  "article_info": {
    "id": 13531,
    "sentences": [
      {
        "id": 1086927,
        "sentence": "Mr and Mrs Dursley, of number four, Privet Drive...",
        "data": [
          { "word": "Mr", "type": 0 },
          { "word": " ", "type": 1 },
          { "word": "Privet", "type": 0, "mean": "女贞", "proper_noun_key": "2" }
        ],
        "proper_noun_hash": {
          "2": {
            "proper_type": "culture",
            "culture_type": "地名场所",
            "lemma": {
              "word": "Privet Drive",
              "mean": "女贞路",
              "base_desc": "女贞路位于英国萨里郡的小惠金区...",
              "extend_desc": "",
              "image_url": ""
            },
            "base": null
          }
        }
      }
    ],
    "notes": {
      "sid_to_note_ids": {
        "1087018": [8540355]
      },
      "note_info": {
        "8540355": {
          "mark": 1,
          "comment": 0
        }
      }
    }
  },
  "book_info": {
    "book_id": 343,
    "book_name": "Harry Potter and the Philosopher’s Stone",
    "book_name_cn": "哈利·波特与魔法石"
  }
}
```

---

## 11. 注意事项

1. JSON 中大量中文以 `\uXXXX` 形式转义，解析后会显示为中文。
2. `null` 表示当前字段无值。
3. 空数组 `[]` 和空对象 `{}` 表示暂无数据。
4. 部分字段并非每个句子都有，例如 `means`、`style`、`mean`、`mean2`、`proper_noun_key`、`phrase_id`。
5. `type` 的 `0/1/2` 含义是根据样本推断：`0` 普通文本，`1` 空格，`2` 标点或特殊符号。
6. `time_list` 通常与句子时间轴对应，用于音频播放时同步高亮。
7. `proper_noun_key` 与 `proper_noun_hash` 的键对应，用于展示专有名词解释。
8. `notes` 用于关联用户笔记与句子。
