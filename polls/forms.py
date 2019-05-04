from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from polls.models import Poll, Question, Comment, Choice


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


class PollForm(forms.Form):
    title = forms.CharField(label="ชื่อโพล", max_length=100, required=True)
    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10,
                                      required=True, validators=[validate_even])
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    # def clean_title(self):
    #     data = self.cleaned_data['title']
    #
    #     if "ไอทีหมีแพนด้า" not in data:
    #         raise forms.ValidationError("คุณลืมชื่อคณะ")
    #
    #     return data
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start = cleaned_data.get('start_date')
    #     end = cleaned_data.get('end_date')
    #
    #     if start and not end:
    #         # raise forms.ValidationError("โปรดเลือกวันสิ้นสุด")
    #         self.add_error('end_date', "โปรดเลือกวันสิ้นสุด")
    #     elif not start and end:
    #         # raise forms.ValidationError("โปรดเลือกวันเริ่มต้น")
    #         self.add_error('start_date', "โปรดเลือกวันเริ่มต้น")


class QuestionForm(forms.ModelForm):
    question_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Question
        exclude = ['poll']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


class QuestionModelForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ['del_flag']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    # def clean_title(self):
    #     data = self.cleaned_data['title']
    #
    #     if "ไอทีหมีแพนด้า" not in data:
    #         raise forms.ValidationError("คุณลืมชื่อคณะ")
    #
    #     return data
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start = cleaned_data.get('start_date')
    #     end = cleaned_data.get('end_date')
    #
    #     if start and not end:
    #         # raise forms.ValidationError("โปรดเลือกวันสิ้นสุด")
    #         self.add_error('end_date', "โปรดเลือกวันสิ้นสุด")
    #     elif not start and end:
    #         # raise forms.ValidationError("โปรดเลือกวันเริ่มต้น")
    #         self.add_error('start_date', "โปรดเลือกวันเริ่มต้น")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'body', 'email', 'tel']

    # title = forms.CharField(max_length=100, required=True)
    # body = forms.CharField(max_length=500, required=True)
    # email = forms.EmailField(validators=[validators.validate_email])
    # tel = forms.IntegerField(min_value=10, max_value=10)

    # def clean_title(self):
    #     data = self.cleaned_data['title']
    #
    #     if not data:
    #         raise forms.ValidationError("ต้องกรอก email หรือ Mobile Number")
    #
    #     return data

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('tel')

        if not email and not mobile:
            self.add_error('tel', "ต้องกรอก email หรือ Mobile Number")
            # raise forms.ValidationError("โปรดเลือกวันสิ้นสุด")
        try:
            int(mobile)
        except:
            self.add_error('tel', "หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        if len(mobile) < 10:
            # raise forms.ValidationError("โปรดเลือกวันเริ่มต้น")
            self.add_error('tel', "หมายเลขโทรศัพท์ต้องมี 10 หลัก")
        # elif not validators.validate_email(email):
        #     self.add_error('email', "Email a valid email address")


# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField()
#     sender = forms.EmailField()
#     recipients =

class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'


class CreateQuestion(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    value = forms.IntegerField(max_value=1)
