# インストール手順（環境構築）
Dockerを使用せずにアプリをインストールする手順を説明します。
開発を行う際はこちらでインストールしてください。

## 目次
- [インストール手順（環境構築）](#インストール手順環境構築)
  - [目次](#目次)
  - [必要条件](#必要条件)
    - [Windowsの場合](#windowsの場合)
    - [Ubuntuの場合](#ubuntuの場合)
    - [Macの場合](#macの場合)
  - [管理ユーザーの作成](#管理ユーザーの作成)
  - [AI機能の有効化](#ai機能の有効化)
  - [データベースのエクスポートとインポート](#データベースのエクスポートとインポート)
    - [データベースのエクスポート](#データベースのエクスポート)
    - [データベースのインポート](#データベースのインポート)
## 必要条件

このアプリを動作させるためには、以下の環境が必要です。

- Python 3.10以上
- pip (Pythonのパッケージ管理ツール)　Pythonをインストールすると自動的にインストールされます。
- MySQL 8.0以上 またはその互換ソフトウェア

### Windowsの場合

1. **Pythonとpip, MySQLのインストール確認**

   `cmd`を開いて、以下のコマンドでインストール済みのPythonとpipのバージョンを確認します。

   ```bash
   python --version
   pip --version
   ```
   
   ```bash
   mysql --version
   ```

   インストールされていない場合は、[Python公式サイト](https://www.python.org/)からPythonをダウンロードしてインストールしてください。
   MySQLのインストールは[MySQL公式サイト](https://dev.mysql.com/downloads/mysql/)からダウンロードしてインストールしてください。

2. **リポジトリのクローン**

   任意のディレクトリを開き、以下のコマンドでリポジトリをクローンします。

   ```bash
   git clone https://github.com/syun100000/archive_system_django.git
   ```

   もしくは，リポジトリをダウンロードして解凍してください。

3. **必要なパッケージのインストール**

   クローンしたディレクトリに移動し、以下のコマンドで必要なPythonパッケージをインストールします。

   ```bash
   cd archive_system_django
   pip install -r requirements.txt
   ```

4. **データベースの作成**

   MySQLにデータベースを作成します。
   - デフォルトの設定ファイルを変更せずにデータベースを作成する場合は、以下のデータベースを構築してください。
       - データベース名: archive_system
       - ユーザー名: archive_system
       - パスワード: archive_system
       - ホスト: localhost
       - ポート: 3306
   - **archive_systemユーザーには、archive_systemデータベースのすべての権限を付与してください。**
   - **上記の環境と異なる環境で運用する場合は,`archive_system/settings_development.py` ファイルでデータベースの設定を変更してください。**

5. **マイグレート**

   以下のコマンドでマイグレーションを実行します。

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   マイグレーションが正常に完了したら、データベースにテーブルが作成されます。

6. **Djangoサーバーの起動**

   以下のコマンドでDjangoサーバーを起動します。

   ```bash
   python manage.py runserver
   ```

   ブラウザで `http://localhost:8000` にアクセスし、アプリが正しく動作していることを確認してください。

### Ubuntuの場合

1. **Pythonとpip, MySQLのインストール確認**

   ターミナルを開いて、以下のコマンドでインストール済みのPythonとpipのバージョンを確認します。

   ```bash
   python3 --version
   pip3 --version
   ```
   
   ```bash
   mysql --version
   ```

   インストールされていない場合は、以下のコマンドでPythonとpipをインストールします。

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
   MySQLのインストールは以下のコマンドで行います。
   ```bash
   sudo apt install mysql-server
   ```

2. **リポジトリのクローン**

   任意のディレクトリを開き、以下のコマンドでリポジトリをクローンします。

   ```bash
   git clone https://github.com/syun100000/archive_system_django.git
   ```

   もしくは，リポジトリをダウンロードして解凍してください。

3. **必要なパッケージのインストール**

   クローンしたディレクトリに移動し、以下のコマンドで必要なPythonパッケージをインストールします。

   ```bash
   cd archive_system_django
   pip3 install -r requirements.txt
   ```

4. **データベースの作成**

   MySQLにデータベースを作成します。
   - デフォルトの設定ファイルを変更せずにデータベースを作成する場合は、以下のデータベースを構築してください。
       - データベース名: archive_system
       - ユーザー名: archive_system
       - パスワード: archive_system
       - ホスト: localhost
       - ポート: 3306
   - **archive_systemユーザーには、archive_systemデータベースのすべての権限を付与してください。**
   - **上記の環境と異なる環境で運用する場合は,`archive_system/settings_development.py` ファイルでデータベースの設定を変更してください。**

5. **マイグレート**

   以下のコマンドでマイグレーションを実行します。

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
   マイグレーションが正常に完了したら、データベースにテーブルが作成されます。

6. **Djangoサーバーの起動**

   以下のコマンドでDjangoサーバーを起動します。

   ```bash
   python3 manage.py runserver
   ```

   ブラウザで `http://localhost:8000` にアクセスし、アプリが正しく動作していることを確認してください。

### Macの場合

1. **Pythonとpip, MySQLのインストール確認**

   ターミナルを開いて、以下のコマンドでインストール済みのPythonとpipのバージョンを確認します。

   ```bash
   python3 --version
   pip3 --version
   ```
   
   ```bash
   mysql --version
   ```

   インストールされていない場合は、以下のコマンドでHomebrewを使用してPythonとpipをインストールします。

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python
   ```
   MySQLのインストールは以下のコマンドで行います。
   ```bash
   brew install mysql
   ```

2. **リポジトリのクローン**

   任意のディレクトリを開き、以下のコマンドでリポジトリをクローンします。

   ```bash
   git clone https://github.com/syun100000/archive_system_django.git
   ```

   もしくは，リポジトリをダウンロードして解凍してください。

   
3. **必要なパッケージのインストール**

   クローンしたディレクトリに移動し、以下のコマンドで必要なPythonパッケージをインストールします。

   ```bash
   cd archive_system_django
   pip3 install -r requirements.txt
   ```

4. **データベースの作成**

   MySQLにデータベースを作成します。
   - デフォルトの設定ファイルを変更せずにデータベースを作成する場合は、以下のデータベースを構築してください。
       - データベース名: archive_system
       - ユーザー名: archive_system
       - パスワード: archive_system
       - ホスト: localhost
       - ポート: 3306
   - **archive_systemユーザーには、archive_systemデータベースのすべての権限を付与してください。**
   - **上記の環境と異なる環境で運用する場合は,`archive_system/settings_development.py` ファイルでデータベースの設定を変更してください。**

5. **マイグレート**

   以下のコマンドでマイグレーションを実行します。

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
   マイグレーションが正常に完了したら、データベースにテーブルが作成されます。

6. **Djangoサーバーの起動**

   以下のコマンドでDjangoサーバーを起動します。

   ```bash
   python3 manage.py runserver
   ```

   ブラウザで `http://localhost:8000` にアクセスし、アプリが正しく動作していることを確認してください。

## 管理ユーザーの作成
はじめてアプリを起動すると、管理者ユーザーを作成する必要があります。
管理者ユーザーを作成するには、以下のコマンドを実行します。
**仮想環境を使用している場合は、仮想環境を有効にしてからコマンドを実行してください。**

Windowsの場合
```bash
python manage.py createsuperuser
```
Ubuntuの場合
```bash
python3 manage.py createsuperuser
```

画面に従ってユーザー名、メールアドレス、パスワードを入力してください。

## AI機能の有効化
インストールした直後の状態では、AI機能を有効にしても動作しません。
AI機能を有効にするには[こちら](ai.md)を参照してください。

## データベースのエクスポートとインポート
### データベースのエクスポート
データベースをエクスポートするには、以下のコマンドを使用します。

rootユーザーで実行する場合

   (例: データベース名 `archive_system` 　パスワードが `archive_system` の場合)
   ファイル名は `archive_system.sql` とします。
```bash
mysqldump -u root -p archive_system > archive_system.sql
```

### データベースのインポート
データベースをインポートするには、以下のコマンドを使用します。

rootユーザーで実行する場合

   (例: データベース名 `archive_system` 　パスワードが `archive_system` の場合)
   ファイル名は `archive_system.sql` とします。

```bash
mysql -u root -p archive_system < archive_system.sql
```
