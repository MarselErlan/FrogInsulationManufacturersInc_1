from .models import BlogComment, BlogPostCategory
from MainWepSite.models import Product
from django import forms
from .models import BlogPost

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'stock_quantity']  # и другие поля, если они есть


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import BlogPost, Tag

class BlogPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'main_image', 'b_category', 'tags']

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        self.fields['b_category'].queryset = BlogPostCategory.objects.all()
        self.fields['main_image'].required = False




from django.forms import inlineformset_factory
from .models import BlogPost, BlogPostImage

BlogPostImageFormSet = inlineformset_factory(
    BlogPost,
    BlogPostImage,
    fields=('small_image',),
    extra=1,
    can_delete=True
)
