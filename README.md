# アーカイブシステム - archive_system_django

## プロジェクト概要
このプロジェクトは、アーカイブシステムをDjangoで開発したもので、歴史資料や文書を効率的に管理・閲覧できるプラットフォームを提供します。

## 機能
- 記事の作成、編集、削除、閲覧
- ユーザーの登録、ログイン、ログアウト
- ファイルのアップロード、ダウンロード
- 高度な検索オプション（AND検索、OR検索、除外検索など）
- 管理者用ダッシュボード

## インストール手順
このプロジェクトをローカル環境にインストールする手順について説明します．
開発環境の構築，開発サーバーを使用したアプリケーションの使用が可能です．
[インストール手順（環境構築）](doc/install.md)

## Dockerを使用したインストール手順
Dockerを使用してアプリケーションをインストールする方法について説明します．
Dockerを使用することで，容易にアプリケーションの環境構築を行うことができます．
[Dockerを使用したインストール方法](doc/docker_install.md)

## 環境変数の設定
プロジェクトルートにある `.env.example` をコピーして `.env` ファイルを作成し、各種キーや設定値を入力してください。例:

```bash
cp .env.example .env
# エディタで .env を開いて SECRET_KEY や OPENAI_API_KEY などを設定
```
