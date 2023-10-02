from layout.models import Classes

def get_available_classes():
    return Classes.objects.filter(slots_filled__lt=models.F('slots_available'))


