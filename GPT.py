import base64
import requests
import os
import json
from urllib.parse import unquote
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archive_system.settings')
# 設定ファイルの読み込み
from django.conf import settings
import yaml
# 環境設定ファイルの読み込み
CONFIG_FILE = settings.CONFIG_FILE
with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
# GPT-3のAPIキー
OPENAI_API_KEY = config['AI']['gpt']['api_key']
GPT_MODEL = config['AI']['gpt']['model_name']
API_URL = config['AI']['gpt']['url']
MAX_TOKENS = config['AI']['gpt']['max_tokens']
class GPT:
    def __init__(self, prompt="", file_path="",description=""):
        self.api_key = OPENAI_API_KEY
        self.model = GPT_MODEL
        self.max_tokens = MAX_TOKENS
        self.prompt = prompt
        self.url = API_URL
        self.file_path = file_path
        self.description = description
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.response = None

        if self.file_path:
            self.format_file_path()
        if not self.api_key:
            raise ValueError("APIキーが設定されていません")
        if not self.model:
            raise ValueError("モデルが設定されていません")

    def send_request(self):
        if not self.prompt:
            raise ValueError("プロンプトを指定してください")
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompt
                        },
                    ]
                }
            ],
            "max_tokens": self.max_tokens
        }
        if self.file_path:
            base64_image = self.encode_image()
            payload["messages"][0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

        response = requests.post(self.url, headers=self.headers, json=payload)
        self.response = response.json()

    def get_response_message(self) -> str:
        if not self.response:
            raise ValueError("リクエストを送信してください")
        return self.response["choices"][0]["message"]["content"]

    def encode_image(self):
        self.format_file_path()
        if not self.file_path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".ico")):
            raise ValueError("指定されたファイルは画像ではありません.利用可能なファイル形式はjpg, jpeg, png, gif, bmp, tiff, tif, webp, icoです.")
        with open(self.file_path, "rb") as image:
            encoded_string = base64.b64encode(image.read())
        return encoded_string.decode("utf-8")

    def describe_image(self):
        self.prompt = "添付した画像を説明してください．あなたが出したレスポンスはそのままアーカイブシステムで使われるのでそれを前提に説明して余計なテキストは含めないでください。"
        if self.description:
            self.prompt = self.prompt + "画像についての追加情報：" + self.description
        self.send_request()
        return self.get_response_message()

    def format_file_path(self):
        if not self.file_path:
            raise ValueError("ファイルパスを指定してください")
        self.file_path = unquote(self.file_path)
        if self.file_path[0] == "/":
            self.file_path = self.file_path[1:]
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("ファイルが見つかりません")
        return self.file_path

    # 画像に関連するタグを生成し，辞書型で返す
    def generate_tags(self) -> dict:
        self.prompt = "次の画像に関連するタグを生成し、それぞれのタグについて簡単な説明をJSON形式で出力してください。フォーマットは以下の通りです：\n\n{\n  \"tags\": [\n    {\"tag\": \"タグ名\", \"description\": \"タグの説明\"}\n  ]\n}"
        if self.description:
            self.prompt = self.prompt + "画像についての追加情報：" + self.description
        self.send_request()
        # JSON文字列を辞書型に変換
        response_message = self.get_response_message()
        # テストコード
        # response_message = '```json\n{\n  "tags": [\n    {\n      "tag": "マップ",\n      "description": "迷路や場所の配置を示すグリッド形式の図。"\n    },\n    {\n      "tag": "強化学習",\n      "description": "エージェントが最適な行動を学ぶための機械学習手法。"\n    },\n    {\n      "tag": "状態",\n      "description": "環境の特定の状況を示すもので、各セルが異なる状態を表す。"\n    },\n    {\n      "tag": "開始地点",\n      "description": "エージェントが迷路内で行動を開始する位置。"\n    },\n    {\n      "tag": "ゴール地点",\n      "description": "エージェントが目指すべき最終目的地。"\n    },\n    {\n      "tag": "Python",\n      "description": "プログラミング言語で、強化学習のアルゴリズムやシミュレーションに広く使用される。"\n    },\n    {\n      "tag": "データサイエンス",\n      "description": "データの分析や解釈を行う学問領域。"\n    }\n  ]\n}\n```'
        # コードブロックを除去する
        if response_message.startswith("```json"):
            response_message = response_message[7:-4]  # "```json" と "```" を削除
        try:
            response_dict = json.loads(response_message)
        except json.JSONDecodeError as e:
            raise ValueError("JSONのデコードに失敗しました。レスポンス内容を確認してください。") from e
        
        return response_dict
    def generate_title(self) -> str:
        self.prompt = "次の画像に関連するタイトルを生成してください。タイトルは日本語で出力してください。"
        if self.description:
            self.prompt = self.prompt + "画像についての追加情報：" + self.description
        self.send_request()
        # レスポンスの先頭と末尾に"がある場合は削除
        if self.get_response_message().startswith("\"") and self.get_response_message().endswith("\""):
            return self.get_response_message()[1:-1]
        return self.get_response_message()

# テスト
if __name__ == "__main__":
    gpt = GPT(file_path="media/スクリーンショット 2023-12-11 22.06.00.png")
    tags_json = gpt.generate_tags()
    print(tags_json)
    input("Press Enter to continue...")