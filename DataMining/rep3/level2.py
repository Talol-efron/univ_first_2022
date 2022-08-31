import pandas as pd
import linecache
import spacy 

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
print(sum(li)) #総単語数

for comment in df['text']:
    doc = nlp(comment)
    for entity in doc.ents:
        print(entity.text, entity.label_)