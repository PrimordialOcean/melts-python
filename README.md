# rhyolite-melts-python
## 概要
Rhyolite-MELTSの自動化スクリプトです．手入力が面倒なので作りました．

## 各スクリプトの役割
- melts_makeinput.py: CSVファイル（デフォルトは 'start.csv' ）から 'input.csv' ファイルを作成します．input.csvのデータ数が膨大な場合にお使いください．
- melts_gen.py: csvファイル（デフォルトは 'input.csv' ）から.meltsファイルを作成します．
- melts_auto.py: Rhyolite-MELTSの計算をPyAutoGuiを使って自動で行います．
- melts_makedata.py: 計算結果から 'result.csv' を生成します．

## 環境
- Ubuntu 20.04 LTS
- python3.8

### ほかに必要なもの
- python3-tk
- python3-dev
- rename
- scrot

### 必要なサードパーティのpythonライブラリ
- pyautogui
- pandas
- xlrd
- opencv-python

## 使い方
日本語入力をoffにして必ず実行してください．onにしているとRhyolite-MELTSへのファイル名入力が文字化けして計算できません．
