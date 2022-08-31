#初期解を与える
#解が改善されなくなるまで解の更新を繰り返す
#指定した終了条件が満たされるまで上記を繰り返す。

A = [6,1,9,3]
B = [2,5,7,8]
C = [6,3,5,4]
D = [3,5,2,1]

wariate = [A,B,C,D]
#print(wariate)
P = [[1,2,3,4], [1,3,2,4], [1,3,4,2],[1,4,2,3],[1,4,3,2]]  #初期解
perturbation = [[3,4,1,2],[2,4,1,3], [4,2,1,3],[2,3,1,4],[3,2,1,4]] #摂動後
def improve(x):
    #f(x)を求めるアルゴリズムを記述
    #初期解がP個与えられたとき、P回繰り返す
    sum = 0
    i = 0
    for num in x:
        sum += wariate[i][num-1]
        i += 1
    
    return sum

def multi_start_local_search():
    count = 0
    for i in range(len(P)):
        initial_solution = P[i]
        #while True:#終了条件が満たされるまで繰り返す -> 終了条件更新はP回まで
        x = improve(initial_solution) #初期解を与える
        y = improve(perturbation[i])
        #x_ = x or y #最良の解を暫定解とする
        #f(X)>f(y)を満たす近傍解yが存在すれば新しい暫定解とする。
        if(y > x): #xとyどちらが良いか判定
            x_ = x
        else:
            x_ = y 
    return x_

print(multi_start_local_search())