# tesseractを用いたOCR
tesseractを用いたOCRのセットアップと使い方について説明します。

これをセットアップすることでPDFファイルの検索順位を向上させることができます。

ここでの解説では，すでに`pyhon manage.py runserver`が実行できる状態であることを前提としています。

**Dockerにはすでに設定済みです。**

##　目次
- [tesseractを用いたOCR](#tesseractを用いたocr)
  - [セットアップ](#セットアップ)
    - [Windows](#windows)
    - [macOS](#macos)
    - [Ubuntu](#ubuntu)
  - [使い方](#使い方)

## セットアップ
1. まずは、tesseractをインストールします。

### Windows

1. Tesseractのインストール
   - [Tesseractの公式リリースページ](https://github.com/tesseract-ocr/tesseract/releases)からWindows用のインストーラをダウンロードしてインストールします。

2. 環境変数の設定
   - インストールディレクトリ（例: `C:\Program Files\Tesseract-OCR`）をシステムの環境変数`PATH`に追加します。

3. インストール確認
   - コマンドプロンプトを開き、以下のコマンドを実行してインストールが成功したか確認します。

### macOS

1. Homebrewのインストール
   - Homebrewがインストールされていない場合は、[公式サイト](https://brew.sh/index_ja)の指示に従ってインストールします。

2. Tesseractのインストール
   - ターミナルを開き、以下のコマンドを実行してTesseractをインストールします。
     ```sh
     brew install tesseract
     ```

3. インストール確認
   - 以下のコマンドを実行してインストールが成功したか確認します。
     ```sh
     tesseract --version
     ```

### Ubuntu

1. パッケージリストの更新
   - ターミナルを開き、以下のコマンドを実行してパッケージリストを更新します。
     ```sh
     sudo apt update
     ```

2. Tesseractのインストール
   - 以下のコマンドを実行してTesseractをインストールします。
     ```sh
     sudo apt install tesseract-ocr
     ```

3. インストール確認
   - 以下のコマンドを実行してインストールが成功したか確認します。
     ```sh
     tesseract --version
     ```

4. 次に, 日本語言語データをインストールします。
   ```
    sudo apt install tesseract-ocr-jpn
    ```
## 使い方

1. OCRを実行する画像ファイルを用意します。

2. 以下のコマンドを実行して画像からテキストを抽出します。
   ```sh
   tesseract path/to/image.png output -l jpn