# 機能
- 1.トークン送信ブロック
- 2.招待リンクブロック(※ホワイトリスト設定可能)
- 3.短縮リンクブロック
- 4.URLフィルタリング
- 5.罵倒語ブロック
- 6.スパムブロック
- 7.絵文字スパムブロック
- 8.スポイラースパムブロック
- 9.マークダウンスパムブロック
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
