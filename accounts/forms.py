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
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email != confirm_email:
            raise forms.ValidationError("Your emails don't match")
        return cleaned_data


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        #username = self.user.username.encode('ascii','ignore')
        #import pdb
        #pdb.set_trace()

        try:
            auth.password_validation.validate_password(password1,
                                                       self.user)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password1', error)


        # At least MIN_LENGTH long
        if len(password1) < 14:
            raise forms.ValidationError("The new password must be at least 14 "
                                        "characters long.")

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at "
                                        "least one letter and at least one "
                                        "digit or"
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

        if len(set(string.punctuation).intersection(password1)) <= 0:
            raise forms.ValidationError("The new password must contain a "
                                        "special character")

        #if username.decode('ascii') in password1:
        #    raise forms.ValidationError("The new password must not contain "
        #                                "the username")

        return password1


class UserCreationForm(forms.ModelForm):
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            auth.password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password1', error)
        return password1