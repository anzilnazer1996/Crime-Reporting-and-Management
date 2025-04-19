from django import forms

from .models import Profile

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                             'required':'required',
                                                             'placeholder':'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                             'required':'required',
                                                             'placeholder':'Enter Password'}))
        
class RegisterForm(forms.ModelForm):

    class Meta :

        model = Profile  

        fields =['first_name','last_name','photo','email','password']

        widgets = {

            'first_name':forms.TextInput(attrs={'class':'form-control',
                                                'required':'required'
                                                    }),
            'last_name':forms.TextInput(attrs={'class':'form-control',
                                                'required':'required'
                                                    }),
            'photo':forms.FileInput(attrs={'class':'form-control',
                                           'required':'required'
                                                    }),
            'email':forms.EmailInput(attrs={'class':'form-control',
                                            'required':'required'
                                                }),

            'password':forms.PasswordInput(attrs={'class':'form-control',
                                                  'required':'required'
                                                    })                                        
  
        }
    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        host = email.split('@')[1]

        if host not in ['gmail.com','outlook.com','hotmail.com','mailinator.com','yahoo.com']:

            self.add_error('email','not a valid domain')

        return cleaned_data 
           