from django.forms import ValidationError


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def extension_type(fieldfile_obj):
    valid_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif','.docx','.pdf','.xlsx','.xls']
    if not any([True if fieldfile_obj.name.lower().endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{fieldfile_obj.name} is not a valid image format')