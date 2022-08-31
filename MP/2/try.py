num = 20
x_num = []
x_weight = [3, 6, 5, 4, 8, 5, 3, 4, 3, 5, 6, 4, 8, 7, 11, 8, 14, 6, 12, 4]
x_price = [7, 12, 9, 7, 13, 8, 4, 5, 3, 10, 7, 5, 6, 14, 5, 9, 6, 12, 5, 9]
x_value = []  # 品物の価値 price / weight
x_reValue = []
max = 55
storage = 0
price = 0

#tekitou = []
#change_num = []
for i in range(num):
    value = x_price[i] / x_weight[i]
    x_value.append(value)
#print(x_value)

#価値の高い順に並び替える => 価値の高い順からバッグに入れていく
x_reValue = sorted(x_value, reverse=True)
#print(x_reValue)
"""
for i in range(num):
    for j in range(num):
        if x_reValue[i] == x_price[j] / x_weight[j]:
            if not i in tekitou:
                print(i+1, j+1)
                tekitou.append(i)
                change_num.append(j)

print(change_num) #価値の高い順番を示したlist => 失敗？
"""
#x_valueとx_reValueを比べて手動でソートする。ここのプログラム実装ができませんでした。
X_weight = [3, 4, 6, 5, 7, 6, 5, 4, 8, 5, 3, 4, 4, 6, 8, 3, 8, 11, 14, 12]
X_price = [7, 9, 12, 10, 14, 12, 9, 7, 13, 8, 4, 5, 5, 7, 9, 3, 6, 5, 6, 5]
for k in range(num):
    if storage + X_weight[k] <= max:
        storage += X_weight[k]
        price += X_price[k]
        x_num.append(1)
    else:
        x_num.append(0)


print("荷物の組み合わせ(ソート後)は")
print(x_num)
print("価格は: " + str(price))
print("最大容量は: " + str(storage))
#print(len(X_weight))
