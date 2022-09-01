#python3.7

#仕様1
#4バイトを準備してbfindexとする
#仕様2
#システムに登録するファイルはテキストファイルとする
#仕様3
#システムに登録された情報からbfindexを作成する
#仕様4
#ユーザが入力したキーワードに対して作成されたbfindexで検索できるようにする
#仕様5
#positiveかnegativeかを返す(TPとFPが発生していることに注意)

#------------モジュール-----------------------------------
import array
import glob
import copy
import shutil
import os
import sys

#------------定数-----------------------------------
SIZE = 32
FILE = 0
USER = 1

FLAG = ""
SAMPLE = "0"
REGISTER = "1"

if getattr(sys, "frozen", False):
    path_to = os.path.dirname(sys.executable)
else:
    path_to = os.path.dirname(__file__)
samp_path_ast = os.path.join(path_to, "sample_file\\*")
regi_path = os.path.join(path_to, "register_file")
regi_path_ast = os.path.join(path_to, "register_file\\*")

#--------------関数---------------------------------
##仕様1
#初期配列の生成
def initial_bf():
    bfindex = array.array("B", [0, 0, 0, 0])
    return bfindex

##仕様2
#登録されたファイルを保存するディレクトリを初期化する
def initialize_dir():
    shutil.rmtree(regi_path)
    os.mkdir(regi_path)

#サンプルか登録したファイルで検索するのか決定、FLAGでコントロールする     
def register_or_sample():
    global FLAG
    print("サンプルファイルで検索する場合は0\nファイルを登録してから検索する場合は1\nを入力してください。\n")
    while True:
        cont = input("0 or 1\n")
        if cont == SAMPLE:
            FLAG = SAMPLE
            break
        elif cont == REGISTER:
            FLAG = REGISTER
            break
        else:
            print("0か1を入力してください。")

#ファイルの登録をおこなう
def file_register():
    print("ファイルの登録をおこないます。\nファイルの絶対パスを1つ入力してください。")
    print("ファイルの登録を終える時はendと入力してください。")
    print('例1：C:\\Users\\sample1.txt　例2：\"C:\\Users\\sample1.txt\"')
    while True:
        file_path = ""
        count = len(glob.glob(regi_path_ast))
        print(f"\n登録されたファイル：{count}個")
        file_path = input("path：")
        if file_path[0] == '"':
            file_path = file_path.replace('"', '')
        if file_path == "end":
            print("\n登録を終わります。")
            break
        else:
            try:
                shutil.copy(file_path, regi_path)
            except FileNotFoundError:
                print("そのようなファイルはありません。")

#ディレクトリの初期化、サンプルか登録、ファイル登録をまとめておこなう
def file_control():
    initialize_dir()
    register_or_sample()
    if FLAG == SAMPLE: pass
    elif FLAG == REGISTER:
        file_register()

#サンプルまたは登録されるファイルのパスをリストにする
def file_list():
    if FLAG == SAMPLE:
        files = glob.glob(samp_path_ast)
    elif FLAG == REGISTER:
        files = glob.glob(regi_path_ast)
    return files

#ファイルの読み込み
def read_file(path):
    with open(path, 'r', encoding="utf-8") as f:
        data = f.read()
    return data

#パスのリストからファイルの中身を読み込んでリスト化
def get_data(files):
    contents = []
    for file in files:
        data = read_file(file)
        contents.append(data)
    return contents

##仕様3
#ハッシュ値計算3つ オレオレhash
def hash3(word):
    out1 = 0; out2 = 0; out3 = 0
    for chara in word:
        num = ord(chara)
        out1 = out1 * 2 + num + 1
        out2 = out2 * 3 + num + 2
        out3 = out3 * 5 + num + 3
    return [out1 % SIZE, out2 % SIZE, out3 % SIZE]

#配列bのnビット目(左から0～31)を立てる
def bit_one(n, b):
    if 0 <= n <= 7: indexb = 0
    elif 8 <= n <= 15: indexb = 1
    elif 16 <= n <= 23: indexb = 2
    elif 24 <= n <= 31: indexb = 3
    num = n % 8
    indexn = 2**(7 - num)
    b[indexb] = int(b[indexb]) | indexn

#配列bと登録するファイルfileでbfindexを1つ作る
def create_bfindex(b, file, ver=FILE):
    if ver == FILE: contents = file.split()
    elif ver == USER: contents = file.split(",")
    for content in contents:
        hashs = hash3(content)
        bit_one(hashs[0], b)
        bit_one(hashs[1], b)
        bit_one(hashs[2], b)

#初期配列bと全ての登録するファイルfilesでbfindexのリストを作る
def create_bf_list(b, files):
    bf_list = []
    for file in files:
        bf = copy.deepcopy(b)
        create_bfindex(bf, file)
        bf_list.append(bf)
    return bf_list

##仕様4
def get_keywords():
    print("\n検索をおこないます。\n検索したいキーワードを入力してください。")
    print("複数のキーワードを検索する場合は\',\'で区切ってください。")
    print("例1：apple　例2：apple,iphone")
    a = input("keyword：")
    return a

#初期配列bとキーワードkeywordsからbfindexを作る
def create_search_bf(b, keywords):
    bf = copy.deepcopy(b)
    create_bfindex(bf, keywords, USER)
    return bf

#配列bの1のビットの数を数える
def bit_count(b):
    count = 0
    for num in b:
        count += bin(num).count("1")
    return count

##仕様5
#配列bが入ったbsリストと検索用の配列keで両方共にビットが立っている数を数える
def bit_search_result(bs, ke):
    counts = []
    for s in bs:
        a1 = s[0] & ke[0]
        a2 = s[1] & ke[1]
        a3 = s[2] & ke[2]
        a4 = s[3] & ke[3]
        count = bit_count([a1, a2, a3, a4])
        counts.append(count)
    return counts

#ビット1の数のリストboxと検索用の配列のビット1の数countで判定
#ここでのpositiveはTPとFPを含む
def nega_posi(box, count, files):
    print("\n検索結果を表示します。")
    for i in range(len(files)):
        file_name = files[i].split("\\")
        if box[i] == count:
            print(f"{file_name[-1]}：positive")
        else:
            print(f"{file_name[-1]}：negative")

#------------------実行部-----------------------------
def main():
    b = initial_bf()                       #仕様(1)の部分
    file_control()                         #仕様(2)の部分
    files = file_list()
    files_bin = get_data(files)
    bs = create_bf_list(b, files_bin)      #仕様(3)の部分
    keywords = get_keywords()              #仕様(4)の部分
    key_bf = create_search_bf(b, keywords)
    b_count = bit_count(key_bf)
    counts = bit_search_result(bs, key_bf) #仕様(5)の部分
    nega_posi(counts, b_count, files)
    a = input()

if __name__ == '__main__':
    main()