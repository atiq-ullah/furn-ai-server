from django import forms


class PromptForm(forms.Form):
    prompt = forms.CharField(required=True)
    p_type = forms.ChoiceField(
        choices=[("parse", "Parse"), ("cat", "Cat")], required=True
    )


class MessageForm(forms.Form):
    p_type = forms.ChoiceField(
        choices=[("parse", "Parse"), ("cat", "Cat")], required=True
    )
