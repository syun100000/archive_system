# from .forms import SearchForm
from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class SearchFunction():
    # アーカイブの検索
    def upload_search(self,raw_keywords):
        # 全角スペースを半角スペースに変換
        raw_keywords = raw_keywords.upper()
        raw_keywords = raw_keywords.replace('　', ' ')
        all_keywords = raw_keywords.split(" ")

        and_keywords = []
        or_keywords = []
        exclude_keywords = []

        # AND, OR, - で分割
        for word in all_keywords:
            if word.startswith('-'):
                exclude_keywords.append(word[1:])
            elif 'AND' in word:
                and_keywords.extend(word.split('AND'))
            elif 'OR' in word:
                or_keywords.extend(word.split('OR'))
            else:
                and_keywords.append(word)

        query = Q()
        for keyword in and_keywords:
            # AND検索
            query &= Q(title__icontains=keyword) | Q(comment__icontains=keyword) | Q(file_name__icontains=keyword) | Q(file_path__icontains=keyword) | Q(tags__name__icontains=keyword) | Q(extracted_text__icontains=keyword)
        for keyword in or_keywords:
            # OR検索
            query |= Q(title__icontains=keyword) | Q(comment__icontains=keyword) | Q(file_name__icontains=keyword) | Q(file_path__icontains=keyword) | Q(tags__name__icontains=keyword) | Q(extracted_text__icontains=keyword)
        for keyword in exclude_keywords:
            # 除外検索)
            query &= ~(Q(title__icontains=keyword) | Q(comment__icontains=keyword) | Q(file_name__icontains=keyword)) | Q(file_path__icontains=keyword) | Q(tags__name__icontains=keyword) | Q(extracted_text__icontains=keyword)

        search_results = Upload.objects.filter(query).exclude(Q(delete_flag=1) | Q(published=0)).distinct()
        # アーカイブの検索結果を返す
        return search_results
    # レポートの検索
    def report_search(self,raw_keywords):
        # 全角スペースを半角スペースに変換
        raw_keywords = raw_keywords.upper()
        raw_keywords = raw_keywords.replace('　', ' ')
        all_keywords = raw_keywords.split(" ")

        and_keywords = []
        or_keywords = []
        exclude_keywords = []

        # AND, OR, - で分割
        for word in all_keywords:
            if word.startswith('-'):
                exclude_keywords.append(word[1:])
            elif 'AND' in word:
                and_keywords.extend(word.split('AND'))
            elif 'OR' in word:
                or_keywords.extend(word.split('OR'))
            else:
                and_keywords.append(word)

        query = Q()
        for keyword in and_keywords:
            # AND検索
            query &= Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(tags__name__icontains=keyword)
        for keyword in or_keywords:
            # OR検索
            query |= Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(tags__name__icontains=keyword)
        for keyword in exclude_keywords:
            # 除外検索
            query &= ~(Q(title__icontains=keyword) | Q(description__icontains=keyword)) | Q(tags__name__icontains=keyword)

        search_results = Report.objects.filter(query).exclude(Q(is_deleted=1) | Q(is_public=0)).distinct()
        return search_results
        