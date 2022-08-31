import pandas as pd
import numpy as np
import linecache
import spacy 
#import sklearn.feature_extraction.text as fe_text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

file_names = ['4778030','4778031','4782522','4788357','4788362',
              '4788373','4788374','4788388','4791665','4796054',
              '4799780','4799892','4799908','4799929','4799933',
              '4809271','4809276','4809277','4814763','4814765']

df = pd.DataFrame()
nlp = spacy.load('ja_ginza') # 事前学習済みモデルを用意

for file_name in file_names:
    data = ""
    dr = pd.read_csv('Corpus/dokujo-tsushin-' + file_name + '.txt', sep=" ",header= None, names=[0,"URL", "date", "head", "text"])
    for i in range(46): #全文章を4~最後の行までとるように。-> 一番長い文章が49行目まである
        data += linecache.getline(
            'Corpus/dokujo-tsushin-' + file_name + '.txt', 4+i).strip()
    #names=を設定しないと pandas.errors.ParserError: Error tokenizing data. C errorが出る
    #１列目->URl, 2列目->日付, 3行目-> 見出し, 4列目->文章(text)が格納されたDataFrame
    loc = pd.Series([dr[0][0], dr[0][1], dr[0][2], data], index=["URL", "date", "head","text"])
    df = df.append([loc],ignore_index=True)

def word2vec(df, column):
  vectors = []
  for text in df[column]:
    doc = nlp(text)
    vectors.append(doc.vector)
  return np.array(vectors)

vectors_w2v = word2vec(df, "text")
#print("# word2vec")
#print("vectors_w2v[0] = ", len(vectors_w2v[0]))  #[0]~[20]まで全て300ずつ
#print("vectors_w2v = ", vectors_w2v) #20*300の数値が入っている

def most_similar_comment_indices(vectors, query_vector, n=3):
    similarities = cosine_similarity(vectors, query_vector)
    similarities = similarities.reshape(len(similarities)) # 1行に整形
    most_similar_indicies = np.argsort(similarities)[::-1][:n]
    most_similarities = np.sort(similarities)[::-1][:n]
    return most_similar_indicies, most_similarities

def print_comment_with_similarity(df, column, indicies, similarities):
    for i in range(len(indicies)):
        comment = df[column][indicies[i]]
        similarity = similarities[i]
        print(f'similarity = {similarity:.3f} => {comment}')

query = "婚カツ女子"
target_vector_w2v = [nlp(query).vector]
#print(target_vector_w2v[0][:3])

indicies, similarities = most_similar_comment_indices(vectors_w2v, target_vector_w2v, 3)
#print_comment_with_similarity(df, 'text', indicies, similarities)
#print(target_vector_w2v) #len(target_vector_w2v) -> 1, 
#print(len(target_vector_w2v[0]))

#class分け 恋愛や結婚関連 -> love, その他 -> others
#各文書(text)を見て、恋愛や結婚に関するものか否かでclass分けを行った。
df["class"] = ["love", "love", "others", "others", "others",
               "others", "others","love", "others", "love",
               "others","love", "love", "others", "love",
               "love", "others", "love", "others", "love"
               ]

#df.to_csv("out_data.csv")

X = vectors_w2v
Y = df["class"]

Cs = [0.5, 1.0, 1.5] #ハイパーパラメータ
k_folds = 5 #5 分割検定

print("LinearSVC")
for c in Cs:
  model = LinearSVC(C=c)
  scores = cross_val_score(model, X, Y, cv=KFold(n_splits=k_folds, shuffle=True))
  #KFold(n_splits(分割個数), shuffle(シャッフル), random_state(乱数シード))
  average = scores.mean()
  model.fit(X, Y)
  model.predict(X)
  #print(f'C = {c}: scores={scores}, average={average:.3f}')

"""
#print("SVC")
for c in Cs:
  model = SVC(C=c)
  model.fit(X, Y)
  model.predict(X)
  scores = cross_val_score(model, X, Y, cv=KFold(n_splits=k_folds, shuffle=True))
  #KFold(n_splits(分割個数), shuffle(シャッフル), random_state(乱数シード))
  average = scores.mean()
  
  #print(f'C = {c}: scores={scores}, average={average:.3f}')
"""
pre_model = model.predict(X)

cm = confusion_matrix(df["class"], pre_model)
#print(cm)
sns.heatmap(cm, square=True, cbar=True, annot=True, cmap='Blues')
cm = pd.DataFrame(data=cm, index=["love", "others"], 
                           columns=["love", "others"])
sns.heatmap(cm, square=True, cbar=True, annot=True, cmap='Blues')
plt.yticks(rotation=0)
plt.xlabel("Predict", fontsize=13, rotation=0)
plt.ylabel("True", fontsize=13)

#plt.savefig('sklearn_confusion_matrix.png')
print(df.head())