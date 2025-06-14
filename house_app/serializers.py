from datetime import datetime
from rest_framework import serializers

from .models import Houses, Flats


class HouseCreateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=100)
    build_year = serializers.IntegerField()
    developer = serializers.CharField(max_length=50)

    class Meta:
        model = Houses
        fields = ["address", "build_year", "developer"]

    def validate_build_year(self, value):
        """Кастомная валидация для года постройки"""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Год постройки не может быть больше текущего ({current_year})"
            )
        return value

    def create(self, validated_data):
        """Создание дома с автоматическим заполнением дат"""
        house = Houses.objects.create(
            address=validated_data['address'],
            build_year=validated_data['build_year'],
            developer=validated_data.get('developer'),
        )
        return house


class FlatCreateSerializer(serializers.ModelSerializer):
    flat_number = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    rooms = serializers.IntegerField()
    address = serializers.CharField(max_length=100)

    class Meta:
        model = Flats
        fields = ["flat_number", "price", "rooms", "address"]

    def create(self, validated_data):
        """Создаем квартиру, привязанную к дому"""
        house_address = validated_data.pop("address")
        house = Houses.objects.filter(address=house_address).first()
        house_id = house.house_id

        flat = Flats.objects.create(
            flat_number=validated_data['flat_number'],
            price=validated_data['price'],
            rooms=validated_data['rooms'],
            status='created',
            house=house,
        )

        # Обновляем дату последнего изменения дома
        house.update_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
        house.save()

        return flat

    def to_representation(self, instance):
        """Формат ответа после создания"""
        return {
            'id': instance.flat_id,
            'house_id': instance.house.house_id,
            'price': instance.price,
            'rooms': instance.rooms,
            'status': instance.status,
        }


class FlatDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flats
        fields = ['flat_id', 'flat_number', 'price', 'rooms', 'status']


class HouseFlatListSerializer(serializers.ModelSerializer):
    """"""
    flats = serializers.SerializerMethodField()
    
    class Meta:
        model = Houses
        fields = ['house_id', 'address', 'build_year', 'developer', 'flats']
    
    def get_flats(self, obj):
        """Фильтрация квартир по статусу для разных пользователей"""
        #request = self.context.get('request')
        flats = Flats.objects.all().filter(house=obj)  # Все квартиры дома
        
        # Для обычных пользователей показываем только approved
        #if request and not request.user.is_moderator:
        #    flats = flats.filter(status='approved')
            
        return FlatDetailSerializer(flats, many=True).data
    

class FlatStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=20)
    
    class Meta:
        model = Flats
        fields = ['status']
        read_only_fields = ['id', 'house', 'price', 'rooms']
    
    def validate_status(self, value):
        """Дополнительная валидация статуса"""
        instance = self.instance  # Текущий объект квартиры
        
        # Проверка допустимых переходов статуса
        valid_transitions = {
            'created': ['on_moderation'],
            'on_moderation': ['approved', 'declined'],
            'approved': [],
            'declined': []
        }
        
        if instance.status in valid_transitions and value not in valid_transitions[instance.status]:
            raise serializers.ValidationError(
                f"Недопустимый переход статуса с {instance.status} на {value}"
            )
            
        return value
    
    def update(self, instance, validated_data):
        """Логика обновления статуса с проверкой прав"""
        #request = self.context.get('request')
        
        # Только модератор может менять статус
        #if not request or request.user.user_type != 'moderator':
        #    raise PermissionDenied("Только модератор может изменять статус квартиры")
        
        # Если статус меняется на 'on_moderation', проверяем, что квартиру еще не взяли
        if validated_data['status'] == 'on_moderation' and instance.status == 'on_moderation':
            raise serializers.ValidationError(
                "Эта квартира уже находится на модерации другим модератором"
            )
        
        instance.status = validated_data['status']
        instance.save()
        return instance
    