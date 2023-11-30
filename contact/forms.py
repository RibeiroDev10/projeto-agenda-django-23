from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from contact.models import Contact

"""
    Quando se fala em "inicialização da classe base", 
    refere-se à execução do código no método __init__ da classe base (forms.ModelForm) para 
    realizar as configurações necessárias antes de qualquer código adicional específico da 
    classe derivada (ContactForm). Isso é uma prática comum para garantir uma inicialização adequada e a 
    configuração correta da classe derivada.
"""
class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False,
    )

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'discriptin', 'category',
            'picture'
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


class RegisterForm(UserCreationForm):

    # Definimos os campos do model
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField()

    # Definimos os campos que aparecerão no formulário
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )

    # Verifica se já existe um usuário no banco de dados com o mesmo endereço de e-mail fornecido
    def clean_email(self):
        # Usado para obter o valor do campo 'email' após a validação e limpeza
        email = self.cleaned_data.get('email') # usada para recuperar o valor associado ao campo 'email' após a validação e limpeza dos dados do formulário.

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email', # Campo do form que receberá o erro personalizado
                ValidationError('Já existe este e-mail', code='invalid') # Mensagem personalizada do erro
            )
        return email


class RegisterUpdateForm(forms.ModelForm):
    fisrt_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required. ',
        error_messages={
            'min_length': 'Please, add more than 2 letters'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required. '
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), # Tipo de input, definindo atributos CSS.
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )


    def save(self, commit=True):
        # Após a validação e limpeza bem-sucedidas, o resultado é armazenado no atributo cleaned_data do formulário. 
        # Este é um dicionário onde as chaves são os nomes dos campos do formulário e 
        # Os valores são os dados limpos associados a esses campos.
        cleaned_data = self.cleaned_data
        user = super().clean(commit=False) # O argumento commit=False indica que a limpeza deve ser realizada sem salvar os dados no banco de dados.
        password = cleaned_data.get('password1')

        if password:
            # Setando um password criptografado, com base no primeiro password passado
            user.set_password(password)
        
        if commit:
            user.save()

        return user
    

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2', # Definindo em qual campo do FORM vai aparecer o erro.
                    ValidationError('Senhas não batem')
                )

        # Garantindo que a lógica de validação padrão também seja aplicada.
        return super().clean()
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email  # Pegando o e-mail atual

        # Validando se já existe um mesmo e-mail
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email
    

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Verificando se aquele password passado no input do FORM, é valido.
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1