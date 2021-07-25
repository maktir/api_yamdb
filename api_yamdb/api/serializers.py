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
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', required=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(),
                                               required=False,
                                               write_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                "You've already done review to this title."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(),
                                                write_only=True,
                                                required=False)
    text = serializers.CharField(required=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review',)
        model = Comment
