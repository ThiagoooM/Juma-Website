
from django import forms
from django.contrib.auth.models import User
from .models import MetodoEnvio, Perfil

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","password"]
    def clean(self):
        c = super().clean()
        if c.get("password") != c.get("password2"):
            self.add_error("password2","Las contraseñas no coinciden.")
        return c

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["telefono","documento"]

class CheckoutForm(forms.Form):
    metodo_envio = forms.ChoiceField(choices=MetodoEnvio.choices, widget=forms.RadioSelect)
    nombre = forms.CharField(max_length=100, required=False, label="Nombre de quien recibe")
    telefono = forms.CharField(max_length=30, required=False)
    calle = forms.CharField(max_length=120, required=False)
    numero = forms.CharField(max_length=20, required=False)
    ciudad = forms.CharField(max_length=80, required=False)
    provincia = forms.CharField(max_length=80, required=False)
    codigo_postal = forms.CharField(max_length=20, required=False)
    aclaraciones = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={"rows":2}))
    def clean(self):
        cleaned = super().clean()
        if cleaned.get("metodo_envio") == "envio":
            for f in ["nombre","telefono","calle","numero","ciudad","provincia","codigo_postal"]:
                if not cleaned.get(f):
                    self.add_error(f, "Este campo es obligatorio para Envío a domicilio.")
        return cleaned
