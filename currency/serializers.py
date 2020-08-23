# from django.db import models
# from rest_framework import serializers

# from .models import Currency


# class CurrencySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Currency
#         fields = '__all__'

# class CurrencyListSerializer(serializers.ListSerializer):
#     child = CurrencySerializer()

#     def to_representation(self, data):
#         import pdb; pdb.set_trace()
#         iterable = data.all() if isinstance(data, models.Manager) else data
#         ret = {}
#         ret[iterable['short_name']] = iterable['rate']
#         return ret
        # return {item['short_name']: float(item['rate']) for item in iterable}
