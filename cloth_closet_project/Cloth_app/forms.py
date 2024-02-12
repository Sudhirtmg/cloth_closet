from django import forms
from Cloth_app.models import Post

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': '商品名'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Separate with comma'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input', 'placeholder': '詳細'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'description']
