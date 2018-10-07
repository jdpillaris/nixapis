from . import Nix_Cgroup, Process
from rest_framework import serializers

class CgroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    cpu_limit = serializers.FloatField()
    memory_limit = serializers.FloatField()

    def create(self, validated_data):
        return Nix_Cgroup(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class ProcessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return CGroup(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance