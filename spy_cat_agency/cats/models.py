from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    year_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_mission = models.OneToOneField("Mission", on_delete=models.SET_NULL,
                                            null=True, blank=True,
                                            related_name='spy_cat')

    def __str__(self):
        return self.name + self.breed


class Mission(models.Model):
    cat = models.ForeignKey(SpyCat, on_delete=models.SET_NULL, null=True, blank=True)
    complete_state = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cat.name} - {self.complete_state}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    complete_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.complete_state:
            if all(target.complete_state for target in self.mission.targets.all()):
                if not self.mission.complete_state:
                    self.mission.complete_state = True
                    self.mission.save(update_fields=['complete_state'])


class Note(models.Model):
    target = models.ForeignKey(Target, related_name='notes', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
