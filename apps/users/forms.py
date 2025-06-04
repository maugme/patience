from django import forms

from apps.users.models import User, DoctorProfile, PatientProfile


class DoctorSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.role = 'doctor'

        # hash password
        user.set_password(self.cleaned_data.get('password1'))

        # save in db
        if commit:
            user.save()
            DoctorProfile.objects.create(user=user)
        return user


class CreatePatientForm(forms.ModelForm):
    birth_date = forms.DateField()
    address = forms.CharField()
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.set_unusable_password()

        data = self.cleaned_data

        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user, birth_date=data['birth_date'], address=data['address']
            )
        return user