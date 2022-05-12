from rest_framework import serializers
from core.models import Tag, Ingredient,Recipe

class TagSerializer(serializers.ModelSerializer):
    '''Serializador para objeto de Tag'''

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_Fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    '''Serializador para objeto de ingredientes'''
    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_Fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):
    '''Serializador para objeto Recetas'''

    #todo: Cuando se realiza en models ManyToManyField se debe realizar query
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        # obtener todos los campos
        queryset=Ingredient.objects.all()

        )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        # obtener todos los campos
        queryset=Tag.objects.all()
        )
    class Meta:
        model = Recipe
        fields = ('id','title','ingredients','tags','time_minutes','price','link',)
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    '''Serializar detalle de Receta'''
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True,read_only=True)

class RecipeImageSerializer(serializers.ModelSerializer):
    '''Serializar imagenes'''
    class Meta:
        model=Recipe
        fields = ('id','image')
        read_only_fields=('id',)
