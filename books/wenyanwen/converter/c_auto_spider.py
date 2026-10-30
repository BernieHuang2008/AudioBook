"""
TO GET HERF: 
    l=[];for (var i=0; i<$$("a").length; i++) l.push($("a")[i].href);
TO GET NAME:
    l=[];for (var i=0; i<$$("a").length; i++) l.push($("a")[i].innerText);

"""

BOOK_NAME = "WENYAN_Textbook"

lst = [
    "9b5ed8061abe",
    "178197fd7202",
    "4cac23b07849",
    "8bf5847fffd5",
    "736e296de7fd",
    "4a849bab9912",
    "8def13da8f71",
    "5472fd05f090",
    "7cec0d1b3a86",
    "29fe1b347a74",
    "2a6f10fb5dec",
    "7de576f0313f",
    "95f1b5461664",
    "3827a21544f0",
    "b09aa5c9b747",
    "0456af8aceec",
    "077582755824",
    "48479bc1dedf",
    "189215dc85ba",
    "a2e7b92926c0",
    "353675c10e72",
    "7653b84d49e6",
    "c01db9833cfc",
    "573d6514abc4",
    "1a715a287bed",
    "166993e31db3",
    "6cd4e529af11",
    "f84986dafb2d",
    "a8fb4f01b418",
    "af279f0cdd95",
    "987458864738",
    "0595b5ed9fb4",
    "c72161f552bb",
]
names = [
    "劝学",
    "师说",
    "赤壁赋",
    "登泰山记",
    "子路、曾皙、冉有、公西华侍坐",
    "齐桓晋文之事",
    "庖丁解牛",
    "烛之武退秦师",
    "鸿门宴",
    "窦娥冤",
    "谏逐客书",
    "与妻书",
    "促织",
    "谏太宗十思疏",
    "答司马谏议书",
    "阿房宫赋",
    "六国论",
    "论语十二章",
    "大学之道",
    "人皆有不忍之心",
    "老子四章",
    "五石之瓠",
    "兼爱",
    "屈原列传",
    "苏武传",
    "过秦论(上篇)",
    "五代史伶官传序",
    "陈情表",
    "项脊轩志",
    "兰亭集序",
    "归去来兮辞并序",
    "种树郭橐驼传",
    "石钟山记"
]


prompt = """
阅读以下文言文，将其进行注解（拆分翻译），输出一个codeblock。需要包含标题行（使用提供的标题，并使用空行将其与正文隔开！）。
注解规则：
0. 注释格式：词1<释义1>词2<释义2>…… 释义中的换行请用\\n表示。
1. 按字拆分，逐字翻译。严格按照文言文的翻译标准，对每个字都拆开翻译。
2. 对于少数极常用的固定双音节词用法，可以不拆开，两个字做一个翻译。
3. 对于某些词是由两个表示相同/相似/相反意思的单字组合在一起的，请对两个词分别翻译，但是在词外使用[](词注释)进行词语的注解。例如，…前序文本…[乖<违背，不协调>谬<错误，荒谬>](两字均表示“错误”含义。此处指隋炀帝犯下的错误)…后续…
4. 对句子进行划分，一句一组，每组之间以空行分隔。
5. 对于字/词的注解，需要解释当前字/词在上下文中的意思。对于容易混淆词性的字词，或者特殊的词类活用、语法活用的现象，需做特别解释。如：当<应当>死<n.-v. 处死>；之<主谓之间，取消句子独立性>。
6. 对于重要的实词虚词，需要从高中标准翻译中选择意思。这类词有：而、何、乎、乃、其、且、若、所、为、焉、以、因、于、与、也、则、者、之 等。例如，属予作文以<表目的，来，用来>记之
7. 对于固定的语言结构，或者固定句式，需要采用同词注释相同的符号进行表示。例如：[为xxx<人名>所](“为……所”结构，表示被动。)害<诬陷，陷害>
8. 在逐字翻译的第二行，给出整句的翻译。

例如：
```
上<皇上>曰<说>：“然<对，是这样>。朕<我>为<作为>天子<天子>，所以<用来……的>养<养活>百姓<百姓>也<语气词>，岂<难道>可<可以>劳<使……劳苦>百姓<百姓>以<来>养<养活>己<自己>之<的>宗族<宗族>乎<吗>！”
太宗说：“有道理。朕做天子，就是为了养护百姓，怎么可以劳顿百姓来养护自己的宗族呢？”

十一月<十一月>庚寅<庚寅日>，降<降封>宗室<宗室>郡王<郡王>皆<都>为<成为>县公<县公>，惟<只有>有功<有功劳>者<的人>数人<几个人>不<不>降<降封>。
十一月庚寅日，将宗室郡王都降格为县公，只有功勋卓著的几位不降。
```

"""

import pyperclip
import requests
import json
import time
import b_llm2json


def watch_clipboard(interval=0.2, callback=None):
    """阻塞式监听剪贴板变化"""
    last = pyperclip.paste()
    while True:
        time.sleep(interval)
        try:
            cur = pyperclip.paste()
        except Exception:
            continue          # 剪贴板被别的程序占用，跳过这轮
        if cur != last:
            last = cur
            if callback:
                callback(cur)
            else:
                return cur


book_cnt = 1
for i in range(len(lst)):
    url = "https://www.guwendao.net/shiwenv_{}.aspx".format(lst[i])
    response = requests.get(url, headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
        "Sec-CH-UA": '"Chromium";v="154", "Microsoft Edge";v="154", "Not A(Brand";v="99"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0",
    }, cookies = {
        "login": "flase",
        "verificationCode": "61617CFFB34DF2A6AD751C0F7335BE447D65CBD6751A9458D499A2C066D5A72EB20FA070C7C9AD3C",
        "Hm_lvt_9811648d1409c4608cf19093200cee83": "1790986926",
        "HMACCOUNT": "44B92F854B94DDF8",
        "pcErweimaStrNew": "ccc2b9227dd94e6d8d2efe43f97f5eda17bd929a458a4a08a0c7933377af593c",
        "Hm_lpvt_9811648d1409c4608cf19093200cee83": "1790987176",
    }, timeout=10)
    content = response.text
    content = content[content.index("contson"+lst[i])+22:]
    content = content[:content.index("</div>\n</div>\n</div>")]
    content = content.replace("<p>", "\n")
    content = content.replace("</p>", "")

    l=content.split("\n")
    l2 = ["《{}（{}）》\n{}\n".format(names[i], 1, url)]
    for j in range(len(l)):
        l[j] = l[j].strip()
        if len(l2[-1]) + len(l[j]) < 1000:
            l2[-1] += "\n" + l[j]
        else:
            pyperclip.copy(prompt + l2[-1])
            pasted_text = pyperclip.paste()

            print(("\033[31m" if book_cnt%2==0 else "\033[32m")+"COPIED: 《{}（{}）》\033[0m".format(names[i], len(l2)))

            watch_clipboard(interval=0.2, callback=None)

            ai_resp = pyperclip.paste().replace("\r\n", "\n").strip()

            jjj = b_llm2json.convert(ai_resp)
            with open("../data/{}/{}.json".format(BOOK_NAME, book_cnt), "w", encoding="utf-8") as f:
                json.dump(jjj, f, ensure_ascii=False)
            book_cnt += 1

            l2.append("《{}（{}）》\n{}\n".format(names[i], len(l2)+1, url) + l[j])

    print("已完成《{}》".format(names[i]))
