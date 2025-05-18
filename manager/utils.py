from ArchiveViewer.models import Category
from ArchiveViewer.models import Upload

import pypdfium2 as pdfium
import os
from django.conf import settings
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
import pyocr
import pyocr.builders
import cv2
import numpy as np
def get_category_choices(categories=None, parent=None, level=0, exclude_id=None):
    """
    再帰的にカテゴリーを取得し、階層的に並べたタプルのリストを返します。
    """
    if categories is None:
        categories = Category.objects.all().order_by('name')
    
    choices = []
    children = categories.filter(parent=parent).order_by('name')
    
    for child in children:
        if exclude_id and child.id == exclude_id:
            continue
        display_name = '→' * level + child.name
        choices.append((child.id, display_name))
        choices += get_category_choices(categories, parent=child, level=level+1, exclude_id=exclude_id)
    
    return choices

# アーカイブがPDFの場合，文字を抽出するプログラム
def extract_text_from_pdf(upload: Upload):
    """
    PDFファイルからテキストを抽出します。
    """
    # uploadモデルからファイルのパスを取得
    file_path = upload.file_path
    #ファイルパスの拡張子からファイルの種類を判定
    if file_path.endswith('.pdf'):
        # ファイルパスが相対パスなので、絶対パスに変換
        file_path = os.path.join(settings.BASE_DIR, file_path.lstrip('/'))
        # PDFファイルのテキストを抽出
        pdf = pdfium.PdfDocument(file_path)
        text = ''
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            textpage = page.get_textpage()
            text += textpage.get_text_bounded()
        
        # もしtextが空ならば、スキャナーで読み取った可能性があるので、OCRでテキストを抽出
        if not text:
            # 各ページを画像としてレンダリング
            pdf_path = Path(file_path)
            # 画像を保存するディレクトリを作成
            r = os.urandom(16)
            path = f'./temp/ocr_images_{r.hex()}'
            os.makedirs(path, exist_ok=True)
            #　乱数を使って一時的なディレクトリを作成
            temp_path = Path(path)
            # PDFをImage に変換(pdf2imageの関数)
            pages = convert_from_path(pdf_path, 200)
            fmt = 'jpeg'
            # 画像ファイルを１ページずつtemp_pathに保存
            for i, page in enumerate(pages):
                file_name = "{}_{:02d}.{}".format(pdf_path.stem,i+1,fmt)
                image_path = temp_path / file_name
                page.save(image_path, fmt)
            # OCRでテキストを抽出
            for image_path in temp_path.glob('*.jpeg'):
                text += str(render_doc_text(image_path))
            # 一時的なディレクトリを削除
            for image_path in temp_path.glob('*.jpeg'):
                image_path.unlink()
            temp_path.rmdir()
        return text
    else:
        raise ValueError('This file is not a PDF file.')

# OCRでテキストを抽出するプログラム
def render_doc_text(file_path):
    TESSERACT_PATH = settings.TESSERACT_PATH
    print('OCRでテキストを抽出します。')
    # ツール取得
    pyocr.tesseract.TESSERACT_CMD = TESSERACT_PATH
    tools = pyocr.get_available_tools()
    tool = tools[0]
    # 画像取得
    img = cv2.imread(file_path, 0)
    img = Image.fromarray(img)
    # OCR
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img, lang="jpn", builder=builder)
    data = clean_ocr_text(result)
    return data

import re
# OCRで抽出したテキストをクリーニングするプログラム
def clean_ocr_text(text):
    # 改行と半角スペースを削除する
    cleaned_text = re.sub(r'\s+', ' ', text)  # 連続する空白文字を1つにまとめる
    cleaned_text = re.sub(r' (?=[^a-zA-Z0-9\n])', '', cleaned_text)  # 半角スペースを削除
    cleaned_text = re.sub(r'(?<=[^\n])\n', ' ', cleaned_text)  # 改行をスペースに変更
    cleaned_text = re.sub(r'\s*\n\s*', '\n', cleaned_text)  # 複数改行を1つに

    return cleaned_text