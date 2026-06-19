# 機能
- トークン送信ブロック
- 招待リンクブロック(※ホワイトリスト設定可能)
- 短縮リンクブロック
- URLフィルタリング
- 罵倒語ブロック
- スパムブロック
- 絵文字スパムブロック
- スポイラースパムブロック
- マークダウンスパムブロック
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
```batch
py main.py
```
# 備考
それぞれのライブラリのライセンスは**LICENSES**フォルダを参照してください
