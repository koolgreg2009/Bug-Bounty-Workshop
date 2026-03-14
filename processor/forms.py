from django import forms

from .models import Preset


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        single_image_field = forms.ImageField()
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        return [single_image_field.clean(item, initial) for item in data]


class UploadForm(forms.Form):
    image = forms.ImageField()


class PresetForm(forms.ModelForm):
    dot_spacing = forms.IntegerField(initial=10)
    style = forms.ChoiceField(
        choices=[("classic", "Classic"), ("diamond", "Diamond"), ("line", "Line")]
    )

    class Meta:
        model = Preset
        fields = ["name", "is_default"]


class PresetImportForm(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea)


class BatchUploadForm(forms.Form):
    images = MultipleImageField()
    make_public = forms.BooleanField(required=False, label="Make all images public")
