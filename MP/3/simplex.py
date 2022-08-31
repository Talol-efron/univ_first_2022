#タブローのアルゴリズムの実装ができなかった。
#タブロー以外の処理は行えた

from traceback import print_tb


Z = [0, -1, -1, -1]
X_4 = [8, 1, -1, 2]
X_5 = [1, 2, -3, -1]

def draw_1():
    print("   | 定  -X_1  -X_2  -X_3")
    print("-------------------------")
    print("X_4|" + " " + str(X_4[0]) + "    " + str(X_4[1]) + "    " + str(X_4[2]) + "     " + str(X_4[3]))
    print("X_5|" + " " + str(X_5[0]) + "    " + str(X_5[1]) + "    " + str(X_5[2]) + "     " + str(X_5[3]))
    print("Z  |" + " " + str(Z[0]) + "    " + str(Z[1]) + "    " + str(Z[2]) + "     " + str(Z[3]))
    print("")

def draw_2():
    print("   | 定  -X_5  -X_4  -X_3")
    print("-------------------------")
    print("X_2|" + " " + str(X_2[0]) + "    " + str(X_2[1]) + "    " + str(X_2[2]) + "     " + str(X_2[3]))
    print("X_1|" + " " + str(X_1[0]) + "    " + str(X_1[1]) + "    " + str(X_1[2]) + "     " + str(X_1[3]))
    print("Z  |" + " " + str(Z[0]) + "    " + str(Z[1]) + "    " + str(Z[2]) + "     " + str(Z[3]))
    print("")
print("最初のシンプレックスのタブローは")
print("")
draw_1()
##PEを探す過程#############
def search_PE_1(list):#絶対値が大きい列の番号を返す
    num = 0
    result = max(list, key=abs)
    for i in range(len(list)):
        if result == list[i]:
            num += i
            #print(num)
            return num

search_PE_1(Z)#1を返す

def search_PE_2(list1, list2): #1回目はX_5を返す　2回目 -> x ...
    num1 = list1[0] / list1[search_PE_1(Z)]
    num2 = list2[0] / list2[search_PE_1(Z)]
    if list1[search_PE_1(Z)] >= 0 and list2[search_PE_1(Z)] >= 0:
        if num1 >= num2:
            return list2
        else:
            return list1
    elif list1[search_PE_1(Z)] < 0:
        return list2
    else:
        return list1

#print(search_PE_2(X_4, X_5))

##ここから求めたPEを対象に計算###########

def calc_PE(list):
    for i in range(len(list)):
        if not i == search_PE_1(Z): #PE以外の同じ行の値をPEで割る
            list[i] = list[i] / list[search_PE_1(Z)]
    #最後にPEをPE自身で割る -> 1になる
    list[search_PE_1(Z)] = 1
    #計算結果を上書き
    X_5 = list

calc_PE(search_PE_2(X_4, X_5))
print("PEを探し、計算すると")
print("")
draw_1()

X_2 = [15/2, 0, 1/2, 5/2]
X_1 = X_5
Z = [1/2, 0, -5/2, -3/2]

print("次のシンプレックスタブローは")
print("")
draw_2()#次のシンプレクスタブロー

search_PE_1(Z) #-2.5が絶対値最大なので2を返す
#print(search_PE_2(X_1, X_2))
calc_PE(search_PE_2(X_1, X_2))
print("PEを探し、計算すると")
print("")
draw_2()
X_1 = [23, 1, 0, 7]
Z = [38, 0, 0, 11]

print("次のタブローを計算すると")
print("")
draw_2()
##最後に条件を満たしているか判断###########
def check_finish(list):
    for i in range(len(list)):
        if list[i] >= 0:
            return True          
        else:
            return False

def final_check():
    if check_finish(Z) == True:
        print("条件を満たしています")
    else:
        print("条件を満たしていません")

check_finish(Z)
final_check()

print("従って、求める答えは")
print("X_1= " + str(X_1[0]))
print("X_2= " + str(X_2[0]))
print("X_3= 0")
print("Z= " + str(Z[0]))