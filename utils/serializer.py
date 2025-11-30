from rest_framework.serializers import ModelSerializer

class BaseSerializer(ModelSerializer):
    
    class META:
        read_only_fields = ('created_date', 'updated_date', 'active',)
        exclude = ('created_by', 'updated_by')
    