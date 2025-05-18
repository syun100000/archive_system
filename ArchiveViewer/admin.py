from django.contrib import admin
# from .models import ArchiveContents
# from .models import Thumbnail
from .models import *

admin.site.register(Upload)
admin.site.register(Report)
admin.site.register(UploadHistory)
admin.site.register(ReportHistory)
admin.site.register(UploadFavorite)
admin.site.register(ReportFavorite)
admin.site.register(Tag)
