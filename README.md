# 機能
- 01.トークン送信ブロック
- 02.招待リンクブロック(※ホワイトリスト設定可能)
- 03.短縮リンクブロック
- 04.URLフィルタリング
- 05.罵倒語ブロック
- 06.スパムブロック
- 07.絵文字スパムブロック
- 08.スポイラースパムブロック
- 09.マークダウンスパムブロック
- 10.外部アプリ権限自動/簡単無効化
# 使用方法
## ライブラリをインストールする
- ターミナルを開いて**requirements.txt**のあるディレクトリに移動する
- 以下のコードを実行する
```batch
pip install -r requirements.txt
```
## .envにbotのトークンを入れる
- **discord bot token here**と書かれたところをbotのトークンに置換する
## url_checker.pyにフィルターのURLを入れる
- **filter url here**と書かれたところをフィルターのURLに置換する

オススメは[urlhaus-filter](https://gitlab.com/malware-filter/urlhaus-filter)のuBlock Origin版です
## botを実行する
- 1.ダブルクリックする(できない場合は2へ)
- 2.ターミナルを開いてbotのあるディレクトリに移動する
- 以下のコードを実行する
```batch
py main.py
```
# 備考
それぞれのライブラリのライセンスは**LIBRARY_LICENSES**フォルダを参照してください
