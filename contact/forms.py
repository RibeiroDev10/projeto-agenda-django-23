from django import forms
from django.core.exceptions import ValidationError
from . import models

from contact.models import Contact

"""
    Quando se fala em "inicialização da classe base", 
    refere-se à execução do código no método __init__ da classe base (forms.ModelForm) para 
    realizar as configurações necessárias antes de qualquer código adicional específico da 
    classe derivada (ContactForm). Isso é uma prática comum para garantir uma inicialização adequada e a 
    configuração correta da classe derivada.
"""
class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder': 'Aqui veio do init',
            }
        ),
        label='Primeiro Nome',
        help_text='Texto de ajuda para seu usuário',
    )

    # Chama o método init da classe base (forms.ModelForm)
    # Prática comum quando estendemos uma classe e,
    # Precisamos garantir que a inicialização da classe base seja executada antes da inicialização da classe derivada.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'discriptin', 'category',
        )
    
    # Pegando campos do formulário de Contato e adicionando validação em cima desses campos
    # Pegamos os dados limpos de todos os campos, especificamos os campos usando get('nome_do_campo'), neste caso.
    # 
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid',
            )
        
        if first_name == last_name:
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        # Chama o método clean da classe base - (forms.ModelForm)
        # Usado para garantir que a lógica de limpeza padrão da classe base seja aplicada,
        # Após a lógica personalizada no método clean da ContactForm.
        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Veio do add_error',
                    code='invalid'
                )
            )

        return first_name