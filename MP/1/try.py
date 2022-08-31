import time

start = time.time()
# 物の個数
n = 20
# 要領
capacity = 55
#物の重さ、価値
size = [3, 6, 5, 4, 8, 5, 3, 4, 3, 5, 6, 4, 8, 7, 11, 8, 14, 6, 12, 4]
price = [7, 12, 9, 7, 13, 8, 4, 5, 3, 10, 7, 5, 6, 14, 5, 9, 6, 12, 5, 9]
#最高の重さと価格と最適な組み合わせを記録する
max_size = -1
max_price = -1
combination = []
# iには2**nまでの値が入る。
for i in range(2 ** n):
    # 変数の初期化
    tmp_size = 0
    tmp_price = 0
    tmp_combination = []
    over_flag = False
    for j in range(n):
        # 2進数で計算。シフトして１ビットずつ判断。
        is_put = i >> (n - j - 1) & 1
        # 値を入力
        tmp_combination.append(is_put)
        tmp_size += is_put * size[j]
        tmp_price += is_put * price[j]
        #print(tmp_combination)
        # capa を越えたらフラグを立てて break
        if tmp_size > capacity:
            over_flag = True
            break
    # over flag が立ってない かつ 暫定 max price より高いときに更新
    if (not over_flag) and tmp_price > max_price:
        max_price = tmp_price
        max_size = tmp_size
        combination = tmp_combination
print("合計が最大になる組み合わせ")
print(combination)
print("合計価格: ", max_price)
print("合計サイズ: ", max_size)

end = time.time() - start
print(f"{end:.3f}s")