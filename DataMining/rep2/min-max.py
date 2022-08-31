import pandas as pd
from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

df = pd.read_csv("beer.csv")
temp = pd.DataFrame(df["pH"])
#min-max法
min_max_sacler = preprocessing.MinMaxScaler()
temp_minmax = min_max_sacler.fit_transform(temp)
df["pH"] = temp_minmax #pHの値をmin-max法で求めた値に置き換える
#print(df["pH"]) 置き換えられたpHの値を出力

X = df[["OG", "ABV", "pH", "IBU"]]
Y = df["style"]
Cs = [0.5, 1.0, 1.5] #ハイパーパラメータ
k_folds = 5 #5分割検定

for c in Cs:
    model = LinearSVC(C=c)
    scores = cross_val_score(model, X, Y, cv=KFold(n_splits=k_folds, shuffle=True)) 
    #KFold(n_splits(分割個数), shuffle(シャッフル), random_state(乱数シード))
    average = scores.mean()
    model.fit(X, Y)
    #print(model.predict(X))
    print(f'C = {c}: scores={scores}, average={average:.3f}')