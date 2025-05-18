# context_processors.py
# このファイルは、テンプレートに渡すコンテキストを定義するためのファイルです。
from django.conf import settings
import yaml
# 設定の読み込み
CONFIG_FILE = settings.CONFIG_FILE
def site_settings(request):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return {
        'site_title': config.get('site_title', 'Default Site Title'),
        'location_name': config.get('location_name', 'Default Location Name'),
        'location_address': config.get('location_address', 'Default Location Address'),
        'location_tel': config.get('location_tel', 'Default Location Tel'),
        'location_fax': config.get('location_fax', 'Default Location Fax'),
        'location_web': config.get('location_web', 'Default Location Website'),
        'about_page': config.get('about_page', 'このシステムについて'),
        'can_edit_report': config['staff_authority'].get('can_edit_report', False),
        'can_edit_upload': config['staff_authority'].get('can_edit_upload', False),
        'can_edit_announcement': config['staff_authority'].get('can_edit_announcement', False),
        'can_edit_tag': config['staff_authority'].get('can_edit_tag', False),
        'can_edit_category': config['staff_authority'].get('can_edit_category', False),
        'AI_enabled': config['AI'].get('enabled', False),
    }