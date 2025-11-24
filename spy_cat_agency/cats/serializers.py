import requests
from rest_framework import serializers
from .models import SpyCat, Mission, Target, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'text')


class TargetSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, required=False)

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete_state']

    def update(self, instance, validated_data):
        notes_data = validated_data.pop('notes', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if notes_data is not None:
            instance.notes.all().delete()
            for note_data in notes_data:
                Note.objects.create(target=instance, **note_data)

        return instance


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, required=False)
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete_state', 'targets']

    def validate(self, data):
        spy_cat = data.get('cat', None)

        if spy_cat:
            qs = Mission.objects.filter(cat=spy_cat)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError('SpyCat already on another mission')

        targets = data.get("targets", [])
        if not (0 <= len(targets) <= 3):
            raise serializers.ValidationError("A mission can have at most 3 targets")

        return data

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            notes_data = target_data.pop('notes', {})
            target = Target.objects.create(mission=mission, **target_data)
            for note_data in notes_data:
                Note.objects.create(target=target, **note_data)
        return mission


class SpyCatSerializer(serializers.ModelSerializer):
    CAT_BREED_API = "https://api.thecatapi.com/v1/breeds"

    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'year_of_experience', 'breed', 'salary', 'assigned_mission']

    def validate_breed(self, value):
        try:
            response = requests.get(self.CAT_BREED_API)
            breeds = [b['name'] for b in response.json()]
            if value not in breeds:
                raise serializers.ValidationError("Invalid cat breed")
        except requests.exceptions.Timeout:
            raise serializers.ValidationError("Breed validation service timed out.")
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
        return value
