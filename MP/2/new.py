dic = {1:[3,7],2:[6,12],3:[5,9]}
rev = []
#print(type(dic[1][0]))
for i in range(2):
    value = dic[i+1][1] / dic[i+1][0]
    rev.append(value)

print(rev)