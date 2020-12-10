"""
题库生成
Author: F5
Date: 2020-05-12
"""

import matplotlib.pyplot as plt
import os
import html

course = "my"  # 根据要生成的科目修改此处
data_path = "samples_" + course
tiku_path = "tiku_" + course + ".html"


def unescape(raw: str):
    """
    转换十进制Unicode表示的字符
    """
    ans = raw.strip()
    ans = html.unescape(ans)
    ans = html.unescape(ans)
    ans = ans.replace("<p>", '')
    ans = ans.replace("</p>", '')
    ans = ans.replace("<br>", '')
    ans = ans.replace(' ', '')
    ans = ans.lstrip('>')
    return ans


tiku = open(tiku_path, 'wt', encoding="utf8", errors="replace")

questions = set()
question_count = 0
question_count_list = []
total_count = 0
total_count_list = []

for dirname in os.listdir(data_path):
    for filename in os.listdir(os.path.join(data_path, dirname)):
        if "_files" in filename:
            continue

        filename = os.path.join(data_path, dirname, filename)
        f = open(filename, 'rt', encoding='GBK')
        in_context = False
        in_answer_context = False

        for line in f.readlines():
            # 题目标题
            if "_content" in line:
                total_count += 1
                low = line.find('value=') + 7
                high = line.find('><iframe') - 1
                title = unescape(line[low:high])

                if title not in questions:
                    in_context = True
                    questions.add(title)
                    question_count += 1
                    tiku.write("<h3>" + str(question_count) +
                               ". " + title + "</h3>")

                question_count_list.append(question_count)
                total_count_list.append(total_count)

            # 题目选项
            if in_context and "answer" in line and "sogoutip" not in line:
                low = line.find('answer') + 8
                tiku.write("<div>" + unescape(line[low:]) + "</div>")

            # 题目答案区域结束
            if in_answer_context and "</td>" in line:
                in_context = False
                in_answer_context = False
                tiku.write("</div>")

            # 题目答案选项内容（有多选情况）
            if in_answer_context:
                tiku.write("<div>" + unescape(line) + "</div>")

            # 题目答案区域开始
            if in_context and "[参考答案]" in line:
                in_answer_context = True
                tiku.write("<h5>参考答案</h5><div>")
        f.close()

tiku.close()
print("去重后:", question_count)
print("总计:", total_count)

# 预测题库题目数量
plt.plot(total_count_list, question_count_list)
plt.show()
