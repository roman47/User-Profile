from django import forms
from django.contrib import auth
import string


from . import models


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'dob',
            'email',
            'confirm_email',
            'short_bio',
            'avatar',
        ]

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        if cleaned_data['email'] != cleaned_data['confirm_email']:
            raise forms.ValidationError("Your emails don't match")
        return cleaned_data


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d "
                                        "characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at "
                                        "least one letter and at least one digit or" \
                                        " punctuation character.")

        if len(set(string.ascii_lowercase).intersection(password1)) <= 0:
            raise forms.ValidationError("The new password must contain a "
                                        "lowercase letter")

        if len(set(string.ascii_uppercase).intersection(password1)) <= 0:
            raise forms.ValidationError("The new password must contain an "
                                        "uppercase letter")

        if len(set(string.digits).intersection(password1)) <= 0:
            raise forms.ValidationError("The new password must contain a "
                                        "digit")

        if len(set(string.punctuation).intersection(password1)) <= 0:
            raise forms.ValidationError("The new password must contain a "
                                        "special character")

        return password1
