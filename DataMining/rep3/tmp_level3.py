import pandas as pd
import numpy as np
import linecache
import spacy 
import sklearn.feature_extraction.text as fe_text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
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

#df.to_csv("out_data.csv")
#print(df.head())
#print("文書数: " + str(len(file_names)))
#print("総文字数: " + str(sum(list(map(len, df['text'])))))
li = []

def text_to_sequence_of_words(text, sep=' '):
    num = 0
    '''テキストをtokenに分割し、sep区切りの文字列として結合した文字列を返す。
    args:
      text (str): 処理対象となるテキスト。
      sep (str): 処理結果を結合するための区切り文字。
    return
      str: sepで結合した分かち書き結果。
    '''
    doc = nlp(text)
    sequence = []
    for token in doc:
        sequence.append(token.lemma_)
        num += 1
    #print(num)
    li.append(num)
    return sep.join(sequence)

def df_to_sequence_of_words(df, column, sep=' '):
    '''df[column]を対象として分かち書きする。
    args:
      df (pd.DataFrame): テキストを含むデータフレーム。
      column (str): dfにおける処理対象となる列名。
      sep (str): 分かち書き結果を結合する文字。
    return
      result ([str]): text_to_sequence_of_words()で分かち書き処理された文字列のリスト。
    '''
    result = []
    for comment in df[column]:
        result.append(text_to_sequence_of_words(comment, sep))
    return result

sequence_of_words = df_to_sequence_of_words(df, 'text')
#print(df['text'][0])
#print(sequence_of_words[0])
#print(sum(li)) #総単語数

def count():
  for comment in df['text']:
    doc = nlp(comment)
    for entity in doc.ents:
        print(entity.text, entity.label_)

def bow(docs, stop_words=[]):
    '''Bag-of-Wordsによるベクトルを生成。

    :param docs(list): 1文書1文字列で保存。複数文書をリストとして並べたもの。
    :return: 文書ベクトル。
    '''
    vectorizer = fe_text.CountVectorizer(stop_words=stop_words)
    vectors = vectorizer.fit_transform(docs)
    return vectors, vectorizer

stop_words = ['こと', '\r\n', 'ため', '思う', 'いる', 'ある', 'する', 'なる']
vectors_bow, vectorizer_bow = bow(sequence_of_words, stop_words)
"""
print('# normal BoW')
print('shape = ', vectors_bow.shape)
print('feature_names[:10] = ', vectorizer_bow.get_feature_names_out()[:10])
print('vectors[0] = \n',vectors_bow[0])
print('type(vectors[0]) = ', type(vectors_bow[0]))
print(vectorizer_bow.get_feature_names_out()[594])
print(vectorizer_bow.get_feature_names_out()[93])
"""
#print(vectorizer_bow) #stopwords が出力された
#print(vectors_bow) 

query = '婚カツ女子'
sequence_of_words = text_to_sequence_of_words(query)
#print(sequence_of_words)
target_vector_bow = vectorizer_bow.transform([sequence_of_words])
#print(target_vector_bow)
#print(vectorizer_bow.get_feature_names_out()[522])
#print(vectorizer_bow.get_feature_names_out()[1304])
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

indicies, similarities = most_similar_comment_indices(vectors_bow, target_vector_bow, 3)
#print_comment_with_similarity(df, 'text', indicies, similarities)

X = df["text"]
Y = df["head"]
"""
Cs = [0.5, 1.0, 1.5] #ハイパーパラメータ
k_folds = 5 #5 分割検定
for c in Cs:
  model = LinearSVC(C=c)
  scores = cross_val_score(model, X, Y, cv=KFold(n_splits=k_folds, shuffle=True))
  #KFold(n_splits(分割個数), shuffle(シャッフル), random_state(乱数シード))
  average = scores.mean()
  #model.fit(X, Y)
  #model.predict(X)
  #print(f'C = {c}: scores={scores}, average={average:.3f}')
"""