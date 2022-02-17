from rest_framework import serializers

from Main.models import Numbers

class Numbers_Serializer(serializers.ModelSerializer):

    number  = serializers.DecimalField(
                decimal_places=20,
                max_digits=10000,
                read_only=True
            )

    class Meta:
        model  = Numbers
        fields = ['number']
