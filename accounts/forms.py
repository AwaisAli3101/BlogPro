from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pw2 = cleaned.get('password2')
        if pw and pw2 and pw != pw2:
            self.add_error('password2', 'Passwords do not match')
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-dashed border-cyan-500/50 rounded-lg focus:outline-none focus:border-cyan-400 bg-slate-900/50 text-slate-100 file:bg-cyan-500 file:text-slate-900 file:px-4 file:py-2 file:rounded file:border-0 file:font-semibold file:cursor-pointer',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 5,
                'class': 'w-full px-4 py-3 border-2 border-cyan-500/40 rounded-lg focus:outline-none focus:border-cyan-400 bg-white text-black placeholder-slate-400',
                'placeholder': 'Write something about yourself...'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar

        # validate content type
        content_type = getattr(avatar, 'content_type', '')
        if not content_type.startswith('image/'):
            raise forms.ValidationError('Uploaded file is not an image')

        # validate file size (2.5 MB limit)
        limit_mb = 2.5
        if avatar.size > limit_mb * 1024 * 1024:
            raise forms.ValidationError(f'Image file too large (>{limit_mb} MB)')

        return avatar
