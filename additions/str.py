data="""强制 (qiángzhì) - Принуждать, заставлять (HSK 4).
情况 (qíngkuàng) - Ситуация, обстоятельства (HSK 4).
立刻 (lìkè) - Немедленно, сразу (HSK 4).
物品 (wùpǐn) - Вещь, предмет (HSK 4).
否
"""

result = data.split("\n")
result = [element.split(" ")[0] for element in result]
for i in result:
    print(i, end=",")

