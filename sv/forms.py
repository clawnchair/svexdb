from django import forms


class DumpForm(forms.Form):
    ph = "KeySAVe / KeySAV2 / KeyBV output goes here"
    paste = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ph,}),
                            label="",
                            max_length=75000)
    GENERATION_CHOICES = (
        ('7', '7 (SM/USUM)'),
        ('6', '6 (XY/ORAS)'),
    )
    gen_choice = forms.ChoiceField(choices=GENERATION_CHOICES, required=True, label='Generation')
    # include_nonreddit = forms.BooleanField(label="Include matches from non-Reddit sources", required=False)
