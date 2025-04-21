from django import forms

from .models import CrimeReports,CrimeCategoryChoices

class CrimeRegisterForm(forms.ModelForm):

    class Meta :

        model = CrimeReports 

        exclude =['uuid','active_status','user','status','p_officer','p_status']

        widgets = {

            'location':forms.TextInput(attrs={'class':'form-control',
                                                'required':'required'
                                                    }),
            'description':forms.Textarea(attrs={'class':'form-control',
                                                'required':'required',
                                                'rows': 6,
                                                'cols': 40
                                                    }),                                        
            'evidence_1':forms.FileInput(attrs={'class':'form-control',
                                           'required':'required'
                                                    }),
            'evidence_2':forms.FileInput(attrs={'class':'form-control'
                                                    }),
            'evidence_3':forms.FileInput(attrs={'class':'form-control'
                                                    })
        }
    type_of_crime = forms.ChoiceField(choices=CrimeCategoryChoices.choices,widget=forms.Select(attrs={
                                                                                            'class':'form-select form-control',
                                                                                            'required':'required'}))    