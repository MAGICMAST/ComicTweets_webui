import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
min_words = config['potential']['min_words']
max_words = config['potential']['max_words']


# 根据小说文本进行分词
def combine_strings(strings):
    combined = []
    current_srt = ""
    for s in strings:
        if min_words <= len(current_srt + s) <= max_words:
            combined.append(current_srt + s + "\n")
            current_srt = ""
        elif len(current_srt) > max_words:
            combined.append(current_srt + "\n")
            current_srt = s
        else:
            current_srt += s
    if current_srt:
        combined.append(current_srt + "\n")
    return combined


def participle(text):
    PUNCTUATION = ["，", "。", "！", "？", "；", "：", "”", ",", "!"]

    def clause() -> list[str]:
        start = 0
        i = 0
        text_list = []
        while i < len(text):
            if text[i] in PUNCTUATION:
                try:
                    while text[i] in PUNCTUATION:
                        i += 1
                except IndexError:
                    pass
                text_list.append(text[start:i])
                start = i
            i += 1
        return text_list

    text_list = clause()
    return combine_strings(text_list)


if __name__ == "__main__":
    with open("./测试.txt", "r", encoding="utf-8") as f:
        novel = f.read().replace("\n", "").replace("\r", "").replace("\r\n", "")
    with open("./测试txt.txt", "w", encoding="utf-8") as f:
        f.writelines(participle(novel))