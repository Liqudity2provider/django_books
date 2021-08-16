from django import forms
from .models import Comment, Book, Author
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'content')

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book model
    """
    name = forms.CharField()
    author = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['name', 'author', ]


class ReviewForm(forms.ModelForm):
    """
    Form for creating and updating Review model
    """
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = Book
        fields = ['title', 'content', ]
