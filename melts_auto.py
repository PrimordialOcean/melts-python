# -*- coding: utf-8 -*-
import subprocess
import pyautogui
import time
import os

def start_melts():
    # y->n->yでver1.2.0を選択
    subprocess.run("echo 'y\nn\ny\n' | ./Melts-rhyolite-public ./melts_mv.sh &", shell=True)

# "in"ディレクトリからファイル名を抽出する
def getfilelist():
    files = os.listdir('in')
    filenames = list(map(lambda x: x[0:4], files))
    filenames = sorted(filenames)
    return filenames

# 画像認識を利用して目的のボタンをクリック
# バージョンアップしてUIが変化すると動作しなくなる可能性あり
def show_click(imgname):
    while pyautogui.locateOnScreen('img/'+imgname, confidence=0.6) is None:
        time.sleep(3)
    position = pyautogui.locateOnScreen('img/'+imgname, confidence=0.6)
    pyautogui.click(position)

# CSVファイルを操作
def make_csv(filename):
    subprocess.run("mkdir out/"+filename, shell=True)
    subprocess.run("rename 's/tbl/csv/;' *.tbl", shell=True)
    subprocess.run("mv *.csv out/"+filename+"/", shell=True)
    subprocess.run("rm *.inp *.out", shell=True)

def calc_melts(filename):
    # パラメータの設定
    waittime_input = 2 # 入力から計算開始までの待ち時間[sec]
    waittime_calc = 15 # 計算待ち時間[sec]
    waittime_close = 3 # MELTSを再起動するまでの時間[sec]

    # Rhyolite-MLETSの操作
    start_melts()                 # Melts-rhyolite-publicを起動
    show_click('melts120_title.png')
    pyautogui.hotkey('ctrl', 'o') # 「ファイルを開く」ダイアログを開く
    show_click('fileselection.png')
    pyautogui.write('in/'+filename+'.melts', interval = 0.1)
    pyautogui.press('enter')
    time.sleep(waittime_input)    # 読み込まれるまでラグがあるので時間を空ける
    pyautogui.hotkey('ctrl', 'e') # 計算を実行
    time.sleep(waittime_calc)     # 計算時間分だけ空ける

    # 計算結果のファイルをoutフォルダに移動
    make_csv(filename)

    # MELTSを終了
    show_click('melts120_title.png')   # 他をクリックしていた場合の誤作動防止のため，MELTSのウィンドウに移動
    pyautogui.hotkey('ctrl', 'c')      # 終了ダイアログを表示
    show_click('close.png')
    pyautogui.press(['left', 'enter']) # 閉じるを選択して実行
    time.sleep(waittime_close)

def main():
    filenames = getfilelist()
    total = len(filenames)
    count = 0
    for filename in filenames:
        calc_melts(filename)
        count += 1
        print(str(filename))
        print(str(count)+'/'+str(total)+' files are finished.')

if __name__ == '__main__':
    main()
