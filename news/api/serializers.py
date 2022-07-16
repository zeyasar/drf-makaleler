from rest_framework import serializers
from news.models import Makale, Gazeteci
from datetime import datetime, date
from django.utils.timesince import timesince



class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    # yazar=serializers.StringRelatedField()
    # yazar=GazeteciSerializer()
    class Meta:
        model=Makale
        fields='__all__'
        read_only_fields = ['id', 'yaratilma_tarihi', 'güncelleneme_tarihi']

    def get_time_since_pub(self, object):
        now=datetime.now()
        pub_date=object.yayımlanma_tarihi
        if object.aktif:
            time_delta= timesince(pub_date, now)
            return time_delta
        else:
            return "aktif degil"
        

    def validate_yayımlanma_tarihi(self, tarihdegeri):
        today=date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yayimlanma tarihi bugunden sonrasi olamaz!!!')
        return tarihdegeri



class GazeteciSerializer(serializers.ModelSerializer):

    # makaleler=MakaleSerializer(many=True, read_only=True)
    makaleler=serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='makale-detay',)
    class Meta:
        model=Gazeteci
        fields='__all__'








class MakaleDefaultSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    yazar=serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayımlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncelleneme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar=validated_data.get('yazar', instance)
        instance.baslik=validated_data.get('baslik', instance)
        instance.aciklama=validated_data.get('aciklama', instance)
        instance.metin=validated_data.get('metin', instance)
        instance.sehir=validated_data.get('sehir', instance)
        instance.yayımlanma_tarihi=validated_data.get('yayımlanma_tarihi', instance)
        instance.aktif=validated_data.get('aktif', instance)
        instance.save()
        return instance

    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('baslik ve aciklama alanlari ayni olamaz...')
        return data

    def validate_aciklama(self, value):
        if len(value) < 20:
            raise serializers.ValidationError('baslik alani minimum 20 karakter olmali')
        return value
