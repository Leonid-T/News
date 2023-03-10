from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    News post serializer
    """
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'},
            'like': {'read_only': True},
        }
