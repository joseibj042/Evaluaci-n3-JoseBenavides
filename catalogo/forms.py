from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from .models import Perfil
from django import forms
from .models import Celular

class CelularForm(forms.ModelForm):

    class Meta:
        model = Celular

        fields = [
            'marca',
            'codigo',
            'nombre',
            'descripcion',
            'precio',
            'stock',
            'estado',
            'imagen',
            'activo',
        ]

        labels = {
            'marca': 'Marca',
            'codigo': 'Código del celular',
            'nombre': 'Nombre del celular',
            'descripcion': 'Descripción',
            'precio': 'Precio en pesos chilenos',
            'stock': 'Cantidad disponible',
            'estado': 'Estado',
            'imagen': 'Fotografía del celular',
            'activo': 'Producto activo',
        }

        widgets = {
            'marca': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'codigo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'estado': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'imagen': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean_codigo(self):

        codigo = self.cleaned_data['codigo'].strip().lower()

        existe = Celular.objects.filter(
            codigo=codigo
        ).exclude(
            pk=self.instance.pk
        ).exists()

        if existe:
            raise forms.ValidationError(
                'Ya existe un celular con este código.'
            )

        return codigo

    def clean_precio(self):

        precio = self.cleaned_data['precio']

        if precio < 0:
            raise forms.ValidationError(
                'El precio no puede ser negativo.'
            )

        return precio

    def clean_stock(self):

        stock = self.cleaned_data['stock']

        if stock < 0:
            raise forms.ValidationError(
                'El stock no puede ser negativo.'
            )

        return stock

class RegistroForm(UserCreationForm):

    rut = forms.CharField(
        max_length=15,
        label='RUT'
    )

    telefono = forms.CharField(
        max_length=20,
        label='Teléfono'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'rut',
            'telefono',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-control'

    def clean_rut(self):

        rut = self.cleaned_data['rut'].strip().upper()

        if Perfil.objects.filter(rut__iexact=rut).exists():
            raise forms.ValidationError(
                'Este RUT ya está registrado.'
            )

        return rut

class AccesoForm(AuthenticationForm):

    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil

        fields = [
            'rut',
            'telefono',
        ]

        labels = {
            'rut': 'RUT',
            'telefono': 'Teléfono',
        }

        widgets = {
            'rut': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'telefono': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_rut(self):

        rut = self.cleaned_data['rut'].strip().upper()

        if rut:
            existe = Perfil.objects.filter(
                rut__iexact=rut
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if existe:
                raise forms.ValidationError(
                    'Este RUT pertenece a otra cuenta.'
                )

        return rut
