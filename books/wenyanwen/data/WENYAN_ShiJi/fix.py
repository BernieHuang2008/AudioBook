import json
import b_llm2json

for i in range(44, 71):
    with open("{}.json".format(i), "r", encoding="utf-8") as f:
        data = json.load(f)

    origin = data["article_info"]["sentences"][0]["sentence"] + "\n" + data["article_info"]["sentences"][0]["data"][-1]["mean"]

    origin = origin.replace("\r\n", "\n").strip()
    converted = b_llm2json.convert(origin)

    with open("{}.json".format(i), "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False)

    print("done: {}".format(i))
    
