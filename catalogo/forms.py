
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
