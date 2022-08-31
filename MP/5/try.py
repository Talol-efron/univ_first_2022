A = [6,1,9,3]
B = [2,5,7,8]
C = [6,3,5,4]
D = [3,5,2,1]

wariate = [A,B,C,D]
#print(wariate)
perturbation = [2,3,4,1]

sum = 0
i = 0
for num in perturbation:
        sum += wariate[i][num-1]
        i += 1
        print(sum)