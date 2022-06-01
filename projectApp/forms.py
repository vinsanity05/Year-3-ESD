from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

#Forms used to take user input.

class TimeInput(forms.TimeInput): 
    input_type = 'time'

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class StudentClubForm(forms.ModelForm):
    class Meta:
        model = StudentClub
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class deleteStudentClubForm(forms.Form):
    delete_club = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=StudentClub.objects.all(),
        initial=0
        )


class ClubRepresentativeForm(forms.ModelForm):
    class Meta:
        model = ClubRepresentative
        fields = '__all__'
        exclude = ['post_code']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }

class deleteClubRepForm(forms.Form):
    delete_rep = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=ClubRepresentative.objects.all(),
        initial=0
        )


class sStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ['user', 'account', 'valid', 'user_name', 'balance']
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ['user', 'account', 'valid', 'user_name', 'balance']
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

class deleteStudentForm(forms.Form):
    delete_student = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Student.objects.all(),
        initial=0
    )

class StudentFormValidation(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ['user', 'account', 'balance', 'user_name']
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class addStudentAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ['discountRate', 'balance',]
    def __init__(self, *args, **kwargs):
        super(addStudentAccountForm, self).__init__(*args, **kwargs)
        self.fields['club'].required = False

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

class deleteFilmForm(forms.Form):
    delete_film = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Film.objects.all(),
        initial=0
        )


class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = '__all__'

class deleteScreenForm(forms.Form):
    delete_Screen = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Screen.objects.all(),
        initial=0
        )


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
        exclude = ['sold_tickets']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        '   time': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Select a time', 'type':'time'}),
        }

class deleteShowForm(forms.Form):
    delete_Show = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Show.objects.all(),
        initial=0
        )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'expiry_date': DateInput(attrs={'type': 'date'}),
        }

class deleteAccountForm(forms.Form):
    delete_Account = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Account.objects.all(),
        initial=0
        )

class repTicketQuantityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(repTicketQuantityForm, self).__init__(*args, **kwargs)
        self.fields['studentQty'].widget.attrs['min'] = 10

    class Meta:
        model = Booking
        fields = ['studentQty']

class custTicketQuantityForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['studentQty', 'adultQty', 'childQty']

class custCardDetailsForm(forms.ModelForm):
    class Meta:
        model = CardDetails
        fields = ['name', 'card_number', 'expiry_date']

class changeTicketPricesForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['adult_price', 'student_price', 'child_price']

class requestDiscountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['discount_rate']

class loginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
