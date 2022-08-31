import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
df = pd.read_csv("beer.csv")
#print(df)
X = df[["OG", "ABV", "pH", "IBU"]]
Y = df["style"]
"""
print("X.shape = ", X.shape) shape -> (行数, 列数)をタプルで取得
print("Y.shape = ", Y.shape)
print(X.loc[0]) loc -> 行列と列名で位置を指定
print(Y[0])

X.shape =  (150, 4)
Y.shape =  (150,)
OG     11.5
ABV     4.2
pH      4.2
IBU    14.0
Name: 0, dtype: float64
Premium Lager
"""
Cs = [0.5, 1.0, 1.5] #ハイパーパラメータ
k_folds = 5 #5分割検定

for c in Cs:
    model = LinearSVC(C=c)
    scores = cross_val_score(model, X, Y, cv=KFold(n_splits=k_folds, shuffle=True)) 
    #KFold(n_splits(分割個数), shuffle(シャッフル), random_state(乱数シード))
    average = scores.mean()
    #print(model.fit(X, Y))
    #print(model.predict(X))
    print(f'C = {c}: scores={scores}, average={average:.3f}')