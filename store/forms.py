from django import forms
from .models import Comment, Order


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class AddToCartProductForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1,31)]

    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)

    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone_Number', 'address', 'order_notes', )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'order_notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'If you have any notes write here, otherwise please it empty!'}),
            
        }


    

        