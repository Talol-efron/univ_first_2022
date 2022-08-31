import collections
import linecache
import numpy as np
import pandas as pd
import spacy
import scattertext as st
import matplotlib.pyplot as plt
import japanize_matplotlib

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

#level3で設定したclass
df["class"] = ["love", "love", "others", "others", "others",
               "others", "others","love", "others", "love",
               "others","love", "love", "others", "love",
               "love", "others", "love", "others", "love"
               ]
               
#print(df.head())
show_count = df["class"].value_counts()
#print(show_count)

# 上位2科目のみの dataframe を用意。
# (1) 比較対象をカテゴリ名として保存している列（以下では new_df['title']）と、
# (2) 処理対象となる文書（以下では new_df['comment']）を保存すること。
title1 = 'love'
title2 = 'others'
condition1 = df['class'] == title1
condition2 = df['class'] == title2
new_df = df[condition1 | condition2].loc[:,['class', 'text']]
#new_df["text"] = df["text"]
#print(new_df.head()) 分かち書き前df


# コメント文の nlp 解析結果を用意し、new_df に新しい列として保存する。
# new_df['doc'] の中は丸括弧付きで分かち書きされているように出力されるが、中身はDoc形式である点に注意。
docs = []
for comment in new_df['text']:
    doc = nlp(comment)
    docs.append(doc)

new_df['doc'] = docs
#print(new_df.head())

others = [2,3,4,5,6,8,10,13,16,18] #new_df["class"] = "others" の行番号
love_df = new_df.drop(others)
#print(love_df)

love = [0,1,7,9,11,12,14,15,17,19] #new_df["class"] = "love" の行番号
others_df = new_df.drop(love)
#print(others_df)

# case 1: 分かち書き, 原形処理(lemmatize) + カウント

def count_lemma(df, column):
    '''分かち書き1：原形処理のみ。
    args:
      df (pd.DataFrame): 読み込み対象データフレーム。
      column (str): データフレーム内の読み込み対象列名。
    return
      words_list ([token.lemma_,,,]): 原形処理済み単語のリスト。
    '''
    words_list = []
    for comment in df[column]:
        doc = nlp(comment)
        for token in doc:
            words_list.append(token.lemma_)
    return words_list

words_list = count_lemma(df, 'text')
words_count = collections.Counter(words_list)
"""
love_words_list = count_lemma(love_df, 'doc')
love_words_count = collections.Counter(love_words_list)
print(type(love_words_count.most_common(10)))

others_words_list = count_lemma(others_df, 'doc')
others_words_count = collections.Counter(others_words_list)
print(others_words_count.most_common(10))
"""

# case 4: 分かち書き, 原形処理 + ストップワード + 手動類義語処理 + 品詞別カウント

def reverse_dict(dict_with_list):
    result = {}
    for k, v_list in dict_with_list.items():
        for v in v_list:
            result[v] = k
    return result

def count_lemma4(df, column, target_poses, stop_words, similar_words):
    '''分かち書き4：原形処理し、ストップワードを除き、類義語を代表語に置き換え、品詞別にカウント。
    args:
      df (pd.DataFrame): 読み込み対象データフレーム。
      column (str): データフレーム内の読み込み対象列名。
      target_poses ([str]): カウント対象となる品詞名のリスト。
      stop_words ([str]): 削除したい単語のリスト。
      similar_words ({similar_word1:representive_word1, similar_word2:representive_word1,,}):
        類義語辞書。keyをvalueに置き換える。
    return
      words_dict ({pos1:{token1.lemma_:i, token2.lemma_:j},
                   pos2:{token3.lemma_:k, token4.lemma_:l}}): 品詞(pos)別に、単語をカウント。
    '''
    words_dict = {}
    for pos in target_poses:
        words_dict[pos] = {}

    for comment in df[column]:
        doc = nlp(comment)
        for token in doc:
            if token.lemma_ not in stop_words:
                if token.lemma_ in similar_words.keys():
                    word = similar_words[token.lemma_]
                else:
                    word = token.lemma_

                if token.pos_ in target_poses:
                    if word not in words_dict[token.pos_]:
                        words_dict[token.pos_].update({word: 1})
                    else:
                        words_dict[token.pos_][word] += 1
    return words_dict

target_poses = ['PROPN', 'NOUN', 'VERB', 'ADJ', 'ADV']
stop_words = ['こと', '\r\n', 'ため', '思う', 'いる', 'ある', 'する', 'なる']
similar_words = {'女子':['女性'], '婚カツ':['婚活', '結婚活動'], 'とても':['特に'], "独女":["独身女性"]}
similar_words = reverse_dict(similar_words)
words_dict = count_lemma4(df, 'text', target_poses, stop_words, similar_words)

for pos in target_poses:
    print('pos = ', pos)
    words_count[pos] = collections.Counter(words_dict[pos])
    print(words_count[pos].most_common(10))

# 講義名のユニーク名一覧
titles = df['class'].unique()

# 固有名詞＋名詞の上位20単語一覧
top_n = 20
total_words = {**words_dict['PROPN'], **words_dict['NOUN']}
#print(len(words_dict['PROPN']), len(words_dict['NOUN']), len(total_words))
top_n_words = collections.Counter(total_words).most_common(top_n)
top_n_words

# 授業別に top_n_words が出現した回数をカウント
words = [k for k,v in top_n_words]
zero_matrix = np.zeros((len(words), len(titles)), dtype=int)
df_title_vs_word = pd.DataFrame(zero_matrix, columns=titles, index=words)

# 授業別にコメントを前処理しておく
title_comments = {}
for title in titles:
    comments = df[df['class'] == title]['text']
    tokens = []
    comments = ' '.join(comments)
    doc = nlp(comments)
    for token in doc:
        if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
            if token.lemma_ in words:
                df_title_vs_word.loc[token.lemma_, title] += 1

df_title_vs_word

fig, ax = plt.subplots(figsize=(35, 15))
for i in range(len(df_title_vs_word)):
    ax.bar(df_title_vs_word.columns, df_title_vs_word.iloc[i], bottom=df_title_vs_word.iloc[:i].sum())

ax.legend(df_title_vs_word.index)
ax.set_title(f'カテゴリ別高頻度単語(top_n={top_n})の内訳（出現回数）', size=20)
ax.set_xlabel('カテゴリ一覧')
ax.set_ylabel('出現回数')
#plt.show()

"""
###(6)任意の2カテゴリを選び、scattertextにより単語出現分布を可視化せよ。(3)で述べたこと以外で、scattertextから分かることを述べよ。##
# 用意したdataframeと、比較対象カテゴリを保存している列(title)、Docを保存している列(doc)を指定。
corpus = st.CorpusFromParsedDocuments(new_df, category_col='class', parsed_col='doc').build()

# 上記で用意した corpusと、比較対象したいカテゴリ名（title1, title2）を指定。
html = st.produce_scattertext_explorer(corpus, category=title1, category_name=title1, not_category_name=title2)

# 生成されたHTMLを描画。
from IPython.display import display, HTML
HTML(html)
with open('sample.html', 'w') as f:
    f.write(html)

display(HTML("<br>"))
"""