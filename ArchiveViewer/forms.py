from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', max_length=100)
    searchOption = forms.ChoiceField(label='検索対象', choices=[('report', '記事'), ('upload', 'アーカイブコンテンツ')], widget=forms.RadioSelect)