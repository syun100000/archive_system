from ollama import RequestError, Client

# 設定ファイルの読み込み
# from django.conf import settings
from archive_system import settings
import logging
logger = logging.getLogger(__name__)

# 環境設定ファイルの読み込み
import yaml
try:
    CONFIG_FILE = settings.CONFIG_FILE
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logger.error(f"設定ファイルが見つかりません: {CONFIG_FILE}")
    raise FileNotFoundError(f"設定ファイルが見つかりません: {CONFIG_FILE}")
# OLLAMAの設定
OLLAMA_MODEL = config['AI']['ollama']['model_name']
OLLAMA_API_URL = config['AI']['ollama']['url']
# 画像ファイルをバイト列として読み込む関数
def read_image_file(image_path: str) -> bytes:
    try:
        with open(image_path, 'rb') as image_file:
            return image_file.read()
    except FileNotFoundError:
        # パスの先頭に/がついている場合は削除して再試行
        if image_path.startswith("/"):
            image_path = image_path[1:]
            try:
                with open(image_path, 'rb') as image_file:
                    return image_file.read()
            except FileNotFoundError:
                logger.error(f"画像ファイルが見つかりません: {image_path}")
                raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
        else:
            logger.error(f"画像ファイルが見つかりません: {image_path}")
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
class OllamaClient:
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = model
        self.client = Client(
            host=OLLAMA_API_URL,
            headers={'x-some-header': 'some-value'}
            )
        # 利用可能なモデルのリストを取得して、指定されたモデルが存在するか確認する
        # try:
        #     available_models = self.client.list()
        # except RequestError as e:
        #     logger.error(f"モデルの取得に失敗しました: {e}")
        #     raise RequestError(f"モデルの取得に失敗しました: {e}")
        # model_names = [model['name'] for model in available_models['models']]
        model_names = self.list_models()
        print(f"利用可能なモデル: {model_names}")
        if self.model not in model_names:
            logger.error(f"指定されたモデルが存在しません: {self.model}")
            try:
                # pullできるか試す
                logger.info(f"pullを試みます: {self.model}")
                self.client.pull(model=self.model)
            except Exception as e:
                logger.error(f"pullできませんでした: {e} llava:latestを使用します")
                logger.error(f"pullできませんでした: {e}")
                logger.info("llava:latestを使用します")
                if self.model not in model_names:
                    self.client.pull(model=self.model)
        logger.info(f"OLLAMAクライアントを初期化しました。モデル: {self.model}")
                
    # 利用可能なモデルのリストを取得する
    def list_models(self) -> list:
        try:
            available_models = self.client.list()
        except RequestError as e:
            logger.error(f"モデルの取得に失敗しました: {e}")
            raise RequestError(f"モデルの取得に失敗しました: {e}")
        model_names = [model['name'] for model in available_models['models']]
        return model_names
    def generate_tags_with_image(self, image_path: str) -> dict:
        logger.info(f"タグ生成を開始します。画像パス: {image_path}")
        res = self.client.generate(
            model=self.model,
            prompt="次の画像に関連するタグを生成し、それぞれのタグについて日本語でJSON形式で出力してください。タグは名前だけで結構です.フォーマットは以下の通りです：\n\n{\n  \"tags\": [\n    \"タグ名\"\n  ]\n}",
            images=[read_image_file(image_path)]
        )
        response = res['response']
        #　```jsonの部分と```を削除
        response = response.replace("```json", "").replace("```", "")
        return response
    def generate_title_with_image(self, image_path: str) -> str:
        logger.info(f"タイトル生成を開始します。画像パス: {image_path}")
        res = self.client.generate(
            model=self.model,
            prompt="次の画像に関連するタイトルを生成してください。タイトルは日本語で出力してください。",
            images=[read_image_file(image_path)]
        )
        return res['response']
    def describe_image(self, image_path: str, description: str = None) -> str:
        logger.info(f"画像の説明を開始します。画像パス: {image_path}")
        res = self.client.generate(
            model=self.model,
            prompt='添付した画像を説明してください．あなたが出したレスポンスはそのままアーカイブシステムで使われるのでそれを前提に説明して余計なテキストは含めないでください。',
            images=[read_image_file(image_path)]
        )
        response = res['response']
        #　先頭と末尾に"がある場合は削除
        if response.startswith("\"") and response.endswith("\""):
            response = response[1:-1]
        return response

if __name__ == "__main__":
    ollama = OllamaClient()
    print(ollama.generate_tags_with_image("/media/IMG_20241115133130_20241115133157.jpeg"))
    # print(ollama.describe_image("/media/IMG_20241115133130_20241115133157.jpeg"))