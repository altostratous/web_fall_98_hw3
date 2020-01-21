from django.db import models, transaction


class Virus(models.Model):

    number_of_copies = models.IntegerField(default=0)
    copied_from_id = models.IntegerField(default=0)

    @staticmethod
    def grow_one_generation():
        if not Virus.objects.exists():
            Virus.objects.create()

        for virus in Virus.objects.all():
            virus_copy = virus
            virus_copy.copied_from_id = virus.id
            virus_copy.id = None
            virus_copy.save()
            virus.number_of_copies += 1
            virus.save()


class EvenMicrosecondObject(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_one():
        while True:
            obj = EvenMicrosecondObject.objects.create()
            if obj.created.microsecond % 2 == 0:
                break
            else:
                obj.delete()


