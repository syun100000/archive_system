# AI機能の有効化
このドキュメントでは、AI機能の有効化方法について説明します。
AI機能はインストールしただけでは利用できません。有効化するための手順を以下に示します。

## 目次
- [AI機能の有効化](#ai機能の有効化)
  - [目次](#目次)
  - [概要](#概要)
  - [Open AI APIを利用する場合](#open-ai-apiを利用する場合)
  - [Ollamaを利用する場合](#ollamaを利用する場合)
    - [Dockerを使用しない場合](#dockerを使用しない場合)
    - [ollamaをDockerで使用する場合](#ollamaをdockerで使用する場合)
    - [ollamaのモデルの取得](#ollamaのモデルの取得)
      - [Dockerで動作している場合](#dockerで動作している場合)
      - [Dockerで動作していない場合](#dockerで動作していない場合)
  - [利用可能なAI機能について](#利用可能なai機能について)
    - [現在利用可能なAI機能](#現在利用可能なai機能)
    - [今後追加したいAI機能](#今後追加したいai機能)

## 概要
このシステムでは、インターネット経由で動作する有料のOpen AI社のOpen AI API、またはローカルで動作する無料のOllamaを利用することができます。

Open AI APIは高精度ですが、利用には料金が発生します。一方、Ollamaは無料で利用できますが、精度が劣る場合があります。また、Ollamaを利用するには自前でサーバーを立てる必要があります。

Ollamaの応答速度はサーバーのスペックに依存しますので、適切なサーバーを用意してください。

## Open AI APIを利用する場合
1. Open AIのAPIキーを取得します。

    Open AIプラットフォームにアクセスし、APIキーを取得してください。
    [Open AIプラトフォーム](https://platform.openai.com/docs/overview)
    アカウントが必要になるので右上からログインまたはアカウント作成をしてください。

    ChatGPTのアカウントを持っていれば同じアカウントでログインが可能です。

    ログインしたら上部メニューから「Dashboard」に移動し、左のメニューから「API keys」を選択します。ここでAPIキーの作成ができます。
    作成自体は支払い情報を登録せずともできますが、利用にはAPI用のクレジットを購入する必要があります(以前は無料クレジットが貰えていましたが廃止されたようです)。

    「+ Create new secret key」をクリックするとAPIキーを作成することができます。画面中央、上部どちらのボタンでも構いません。
    作成するAPIキーの設定を入力します。

    ```
    Owned by: 紐付け先の選択
    You: 個人アカウントに対して紐付け
    Service Account: サービスアカウントに対して紐付け
    Name: 識別用の名前。必須でない
    Project: APIキーを紐付けるプロジェクト。プロジェクトを分けたい場合は画面左上から作成可能
    Permissions: APIキーの権限
    All: 全権限を与える
    Restricted: 制限付きの権限。選択すると詳細設定欄が表示され、エンドポイントごとでの設定が可能
    Read Only: 読み取り権限のみ与える
    ```

    迷ったら何も変更せずに「Create secret key」をクリックして大丈夫です。
    作成後すぐにAPIキーが表示されるのでコピーして保管しておいてください。この画面を閉じてしまうと再表示はできません。

2. APIキーを設定します。

    ### 設定ファイルにAPIキーを設定(config.yaml)
    **注意:configはVolumeでマウントされているため、ホスト側で設定を行う必要があります。**
    APIキーを取得したら、設定ファイルにAPIキーを設定します。
    `carchive_system/config/config.yaml`を開き、以下のように設定してください。
    ```yaml
    AI:
        enabled: true   # AI機能を利用するのでtrueに設定
        gpt:
            api_key: ここにAPIキーを入力
            max_tokens: 300
            model_name: gpt-4o-mini
            url: https://api.openai.com/v1/chat/completions
        model: gpt  # Open AI APIを利用する場合はこちらを設定
        ollama:
            model_name: llava:13b
            url: http://localhost:11434
    ```
    `api_key`に取得したAPIキーを入力してください。

    **その他の設定については変更する必要はありませんが、必要に応じて変更してください。**

    - `max_tokens`は一回のリクエストで生成するトークン数です。デフォルトは300ですが,お好みで変更してください。あまり大きい値にするとAPIの使用量が増えクレジットが減ります。
    - `model_name`は使用するモデルを指定します。デフォルトは`gpt-4o-mini`ですが、他のモデルを使用する場合は変更してください。（画像の読み込みが可能なモデルを利用してください）
    - `url`はAPIのエンドポイントを指定します。変更する必要はありません。

    入力が完了したら上書き保存してください。

    ### 管理画面からAPIキーを設定
    管理画面からAPIキーを設定することもできます。
    管理者権限を持つユーザーでログインし、マイページから「管理ページへ」を選択します。
    「システム設定」から「AI設定」を選択し，一度，AIモデルをGPTに設定し，有効化を行なってから保存を押してください。
    その後,APIキーを入力します。

    **その他の設定については変更する必要はありませんが、必要に応じて変更してください。**

    - `モデル名`は使用するモデルを指定します。デフォルトは`gpt-4o-mini`ですが、他のモデルを使用する場合は変更してください。（画像の読み込みが可能なモデルを利用してください）
    - `API URL`はAPIのエンドポイントを指定します。変更する必要はありません。
    - `最大トークン数`は一回のリクエストで生成するトークン数です。デフォルトは300

    入力が完了したら「保存」を押してください。

3. 終了

    以上で設定は完了です。AI機能が有効化されました。

## Ollamaを利用する場合
**このドキュメントでは情報が不足している可能性があります。[Ollamaの公式ドキュメント](https://github.com/ollama/ollama/blob/main/README.md)も一緒に参照してください。**
Ollamaを利用する場合は，サーバーを立てる必要があります。

またOllamaで利用するモデルは画像の読み込みが可能なモデルを利用してください。

サーバーのスペックによって利用できるモデルが変わりますので、適切なサーバーを用意してください。

- 7Bモデルを実行するには少なくとも8GBのRAMが必要です。
- 13Bモデルを実行するには少なくとも16GBのRAMが必要です。
- 33Bモデルを実行するには少なくとも32GBのRAMが必要です。

### Dockerを使用しない場合
1. Ollamaのサーバーを立てる
    [Ollama](https://ollama.com/download)からOllamaのサーバーをダウンロードしてください。
    
    ollamaのセットアップについては[こちら](https://github.com/ollama/ollama/blob/main/docs/README.md)を参照してください。
    インストール完了後、ターミナルを開き、以下のコマンドを実行してください。
    ```bash
    ollama run llava
    ```
    これによってOllamaのサーバーでllavaモデルが起動します。

    他のモデルを利用する場合は`llava`の部分を変更してください。

    利用可能なモデルは[こちら](https://ollama.com/search?c=vision)から確認できます。

2. 設定ファイルに設定
    ### 設定ファイルに設定(config.yaml)
    **注意:configはVolumeでマウントされているため、ホスト側で設定を行う必要があります。**
    `carchive_system/config/config.yaml`を開き、以下のように設定してください。
    ```yaml
    AI:
        enabled: true   # AI機能を利用するのでtrueに設定
        gpt:
            api_key: ''
            max_tokens: 300
            model_name: gpt-4o-mini
            url: https://api.openai.com/v1/chat/completions
        model: ollama   # Ollamaを利用する場合はこちらを設定
        ollama:
            model_name: llava:13b　# 利用するモデルに応じて変更してください
            url: http://localhost:11434　# OllamaのサーバーのURLシステムとは別のサーバーで動作している場合は変更してください
    ```
- `model`を`ollama`に設定してください。

- `model_name`に利用するモデルを指定してください。

- `url`はOllamaのサーバーのURLを指定してください。

    入力が完了したら上書き保存してください。

    ### 管理画面から設定
    管理画面から設定することもできます。

    管理者権限を持つユーザーでログインし、マイページから「管理ページへ」を選択します。
    「システム設定」から「AI設定」を選択し，一度，AIモデルをOllamaに設定し，有効化を行なってから保存を押してください。

    その後,モデル名とURLを入力します。

    `モデル名`に利用するモデルを指定してください。（モデルが存在しない場合はなにも表示されません）
    モデルを追加するにはOllamaのサーバーで
    ```bash
    ollama list
    ```
    を実行して利用可能なモデルを確認してください。
    モデルを追加するには
    ```bash
    ollama pull モデル名
    ```
    を実行してモデルを追加してください．

    `URL`はOllamaのサーバーのURLを指定してください。

    入力が完了したら「保存」を押してください。
    
    保存をおしたあと，再度AI設定画面に入ると，設定が反映されていることを確認してください。
    適切に設定されていない場合は，エラーが表示されます。

3. 終了

    以上で設定は完了です。AI機能が有効化されました。

ollmaの詳細な扱い方については[こちら](https://github.com/ollama/ollama/blob/main/README.md)を参照してください。

### ollamaをDockerで使用する場合
Dockerを使用する場合は、Dockerをインストールしていることが前提です。
[こちら](../doc/docker_install.md)を参照してDockerでのインストールを行なってください。

その後，以下の手順でOllamaを利用することができます。

1. まずはDockerでollamaを下記の手順で立ち上げます．
    #### GPUあり
    まず、NVIDIA Container Toolkitをインストールしてください。

    **aptでインストールする場合**
    1. リポジトリを設定します。
    ```bash
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
        | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
        | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
        | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    ```
    2. NVIDIA Container Toolkit パッケージをインストールします。
    ```bash
    sudo apt-get install -y nvidia-container-toolkit
    ```
    **Yum または Dnf を使用してインストール**
    1. リポジトリを設定します。
        ```bash
        curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo \
            | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
        ```
    2. NVIDIA Container Toolkit パッケージをインストールします。
        ```bash
        sudo yum install -y nvidia-container-toolkit
        ```
    3. Dockerデーモンを再起動します。
        ```bash
        sudo systemctl restart docker
        ```
    ##### アーカイブシステムもDockerで動作している場合
    1. `*-docker-compose.yml`を編集して以下のコンテナを追加してください。
    ```yaml
    services:
    ollama:
        image: ollama/ollama
        volumes:
        - ollama:/root/.ollama
        ports:
        - "11434:11434"
        restart: always
        deploy:
        resources:
            reservations:
            devices:
                - capabilities: [gpu]
    ```
    2. `*_docker_build.sh`を実行してください。
    ```bash
    sh *_docker_build.sh
    ```

    これでアーカイブシステムとOllamaのサーバーが立ち上がります。

    ##### アーカイブシステムがDockerで動作していない場合
    1. ターミナルを開き、以下のコマンドを実行してください。
    ```bash
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```

    これでOllamaのサーバーが立ち上がります。

    #### CPUのみ
    ##### アーカイブシステムがDockerで動作している場合

    1. `*-docker-compose.yml`を編集して以下のコンテナを追加してください。
    ```yaml
    services:
    ollama:
        image: ollama/ollama
        volumes:
        - ollama:/root/.ollama
        ports:
        - "11434:11434"
        restart: always
    ```
    2. `*_docker_build.sh`を実行してください。
    ```bash
    sh *_docker_build.sh
    ```

    これでアーカイブシステムとOllamaのサーバーが立ち上がります。

    ##### アーカイブシステムがDockerで動作していない場合

    1. ターミナルを開き、以下のコマンドを実行してください。
    ```bash
    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```

    これでOllamaのサーバーが立ち上がります。

2. 利用設定
    ### 設定ファイルに設定(config.yaml)

    `carchive_system/config/config.yaml`を開き、以下のように設定してください。
    **注意:configはVolumeでマウントされているため、ホスト側で設定を行う必要があります。**
    ```yaml
    AI:
        enabled: true   # AI機能を利用するのでtrueに設定
        gpt:
            api_key: ''
            max_tokens: 300
            model_name: gpt-4o-mini
            url: https://api.openai.com/v1/chat/completions
        model: ollama   # Ollamaを利用するのでollamaに設定
        ollama:
            model_name: llava:13b　# 利用するモデルに応じて変更してください
            url: http://ollama:11434　# OllamaコンテナのURL
    ```
    ### 管理画面から設定
    管理画面から設定することもできます。

    管理者権限を持つユーザーでログインし、マイページから「管理ページへ」を選択します。

    「システム設定」から「AI設定」を選択し，一度，AIモデルを`Ollama`に設定し，有効化を行なってから保存を押してください。

    その後,モデル名とURLを入力します。

    - `モデル名`に利用するモデルを指定してください。（モデルが存在しない場合はなにも表示されません）

    - `URL`はOllamaコンテナの名前を指定してください。`http://ollama:11434`のように指定してください。
  
  ### ollamaのモデルの取得
ollamaのモデルを取得するには，以下のコマンドを実行してください．

取得可能なモデルは[こちら](https://ollama.com/search?c=vision)から確認できます。

#### Dockerで動作している場合
ターミナルで以下のコマンドを実行してください。
```bash
docker exec -it ollama ollama pull モデル名
```

#### Dockerで動作していない場合
ターミナルで以下のコマンドを実行してください。
```bash
ollama pull モデル名
```


## 利用可能なAI機能について
現在，このシステムでは以下のAI機能を利用することができます。

### 現在利用可能なAI機能
- アーカイブのタイトルの生成(画像ファイルのみ)
- アーカイブの説明文の生成(画像ファイルのみ)
- アーカイブのタグの生成(画像ファイルのみ)

### 今後追加したいAI機能
- チャット形式での記事の生成
- 画像以外のアーカイブコンテンツに対するAI機能の追加
- チャットボットでQ&Aの応答


