from django import forms
from .models import Comment, Order, Contact

from django.utils.translation import gettext_lazy as _



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class AddToCartProductForm(forms.Form):


    COLOR_CHOICES = (
        (_('Blue'), 'BLUE'),
        (_('pistachio nut'), 'Pistachio nut'),
        (_('Green'), 'Green'),
        (_('Black'), 'Black'),
        (_('Purple'), 'Purple'),
        (_('Pink'), 'Pink'),
        (_('White'), 'White'),
        (_('Red'), 'Red'),
        (_('Brown'), 'Brown'),
        (_('Gold'), 'Gold'),
        (_('Silver'), 'Silver'),

    )
    
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1,31)]

    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)

    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)

    color = forms.TypedChoiceField(choices=COLOR_CHOICES, coerce=str)
    
    


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone_Number', 'address', 'order_notes', )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'order_notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'If you have any notes write here, otherwise please it empty!'}),
            
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'address', 'body']

    

        