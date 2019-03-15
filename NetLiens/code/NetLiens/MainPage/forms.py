from django import forms

from .models import AnnuCats

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    family_name = forms.CharField(max_length=50)
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(max_length=1000)
    copy = forms.BooleanField(help_text="Mark if you want a copy", required=False)

    def clean_message(self):
        message = self.cleaned_data['message']
        if "pizza" in message:
          raise forms.ValidationError("Error ! Pizza Key work founded !!")

        return message

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Keywords',
               'class': 'w3-input w3-border w3-animate-input',
               'style': 'width:80%; height:50px; font-size:32px;'
               }), label='')

    categoryOptions = forms.ChoiceField(choices=tuple([(cat.cat_id, cat.cat_name) for cat in
                                                       AnnuCats.objects.filter(cat_parent__contains=0)])
                                        , label='')

