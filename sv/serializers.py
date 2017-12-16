from rest_framework import serializers
from sv.models import Trainer, TSV


# Serializers define the API representation.
class AuxTSVSerializer(serializers.ModelSerializer):  # to fix circular dependency in the 2 serializers
    class Meta:
        model = TSV
        fields = ('tsv', 'gen', 'sub_id', 'created', 'last_seen', 'pending', 'completed', 'archived')


class TrainerSerializer(serializers.ModelSerializer):
    trainer_shiny_values = AuxTSVSerializer(many=True, read_only=True)

    class Meta:
        model = Trainer
        fields = ('username', 'flair_text', 'flair_class', 'activity', 'trainer_shiny_values')


class AuxTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ('username', 'flair_text', 'flair_class', 'activity')


class TSVSerializer(serializers.ModelSerializer):
    trainer = AuxTrainerSerializer(read_only=True)

    class Meta:
        model = TSV
        fields = ('trainer', 'tsv', 'gen', 'sub_id', 'created', 'last_seen', 'pending', 'completed', 'archived')
