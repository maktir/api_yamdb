from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .generators import create_confirmation_code
from .models import Comment, Review, Genre, Category, Title
from users.models import User


class EmailCodeSendSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=False)

    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        #username = validated_data['email'].split("@", 1)[0]
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=create_confirmation_code()
        )
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )
