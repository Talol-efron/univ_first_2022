import itertools
import time

start = time.time() #時間計測開始
weight_list = [3, 6, 5, 4, 8, 5, 3, 4, 3, 5, 6, 4, 8, 7, 11]#, 8, 14, 6, 12, 4]
all_weight_list = []  # 全ての容量を組み合わせたリスト
comp_weight_list = []  # 55を超えないリストの中身
record_num = []  # 25を超えない組み合わせのリストのnumber -> 引数として使う。
price_list = [7, 12, 9, 7, 13, 8, 4, 5, 3, 10, 7, 5, 6, 14, 5]#, 9, 6, 12, 5, 9]
all_price_list = []  # 全ての値段を組み合わせたリスト
comp_price_list = []  # 55を超えないもののうち、値段の組み合わせ
seek_maxPrice = []  # 値段の最大値を探すために各リストの値段を足し合わせて合計を出す。
maximize = 0
num = 0

#ナップサックに入れる組み合わせが何通りあるか調べる。
for i in range(len(weight_list)+1):
    for conb in itertools.combinations(weight_list, i):
        all_weight_list.append(list(conb))  # タプルをリスト型に変換
#print(len(all_weight_list)) #2^20?　

#全ての組み合わせの容量
for i in range(len(all_weight_list)):
    for j in range(len(all_weight_list[i])):
        num += all_weight_list[i][j]
    if num < 56:  # 合計容量が55以下の組み合わせをcomp_weight_listに追加
        comp_weight_list.append(all_weight_list[i])
        record_num.append(i)
    num = 0

##########      price編         ###########
for i in range(len(price_list)+1):
    for conb in itertools.combinations(price_list, i):
        all_price_list.append(list(conb))  # タプルをリスト型に変換
#print(len(all_price_list)) 2^20

for i in range(len(all_price_list)):
    for j in range(len(record_num)):
        if i == record_num[j]:
            comp_price_list.append(all_price_list[i])

#print(comp_price_list)
sum = 0
for i in range(len(comp_price_list)):
    for j in range(len(comp_price_list[i])):
        sum += comp_price_list[i][j]
    seek_maxPrice.append(sum)
    sum = 0
#print(seek_maxPrice)
bigest = max(seek_maxPrice)
print("最大価格:" + str(bigest))

for i in range(len(seek_maxPrice)):
    if bigest == seek_maxPrice[i]:
        hozon = i
#print(hozon)
ult = comp_weight_list[hozon]
print("重量の組み合わせは:" + str(ult))
end = time.time() - start #時間計測終了
print(f"{end:.3f}s")