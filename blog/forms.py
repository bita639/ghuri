from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required = False, widget = forms.Textarea)

class BlogPostCreateForm(forms.ModelForm):

    # card_number = forms.IntegerField(
	# 	label='Card Number',
	# 	required=True,
	# 	widget=forms.NumberInput(
	# 		attrs={'class': 'form-control', 'type': 'number', 'placeholder': '16 Digit Card Number'}
	# 	)
	# )

    # tags = forms.CharField(
	# 	label='Post tag',
    #         max_length=100,
    #         required=True,
    #         widget=forms.TextInput(
    #             attrs={'class': 'form-control', 'type': 'text',
    #                    'placeholder': 'travel, package, trip'}
    #         )
	# )

    title = forms.CharField(
		label='Post Name',
            max_length=250,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Type a Blog Post Name'}
            )
	)

    slug = forms.CharField(
		label='Post URL',
            max_length=250,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Make a Post SLug for URL'}
            )
	)

    body = forms.CharField(
		label='Post Body',
            required=True,
            widget=forms.Textarea(
                attrs={'class': 'form-control', 'type': 'textarea',
                       'placeholder': 'Post Details'}
            )
	)

    photo = forms.ImageField(
		label='Upload Post Photo',
        required=False,
		widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('title','slug','body','photo',)