num = 8
x_num = []
x_num = []
x_weight = [3, 6, 5, 4, 8, 5, 3, 4]
x_price = [7, 12, 9, 7, 13, 8, 4, 5]
x_value = [] #品物の価値 price / weight
x_reValue = []
max = 25
storage = 0
price = 0

for i in range(num):
    value = x_price[i] / x_weight[i]
    x_value.append(value)

for j in range(num):
    if storage + x_weight[j] <= max:
        storage += x_weight[j]
        price += x_price[j]
        x_num.append(1)
    else:
        x_num.append(0)

print("荷物の組み合わせは")
print(x_num)
print("価格は: " + str(price))
print("最大容量は: " + str(storage))