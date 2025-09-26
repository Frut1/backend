from rest_framework import serializers
from django.db.models import Exists, OuterRef
from .models import FarmProfile, FarmFollow
from users.models import User, UserTypeChoices


class FarmListSerializer(serializers.ModelSerializer):
    """농장 목록용 시리얼라이저 - 최소 정보만 포함"""
    farm_id = serializers.IntegerField(source='id', read_only=True)
    farm_name = serializers.CharField(source='farm_name', read_only=True)
    farm_image = serializers.CharField(source='farm_image', read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = FarmProfile
        fields = ['farm_id', 'farm_name', 'farm_image', 'is_following']

    def get_is_following(self, obj):
        """현재 사용자의 팔로우 여부 반환"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FarmFollow.objects.filter(
                user=request.user,
                farm=obj
            ).exists()
        return False


class FarmFollowSerializer(serializers.Serializer):
    """농장 팔로우/언팔로우용 시리얼라이저"""
    farm_id = serializers.IntegerField()

    def validate_farm_id(self, value):
        """농장 ID 유효성 검사"""
        try:
            farm = FarmProfile.objects.get(id=value)

            # 자기 자신 팔로우 방지
            request = self.context.get('request')
            if request and request.user == farm.user:
                raise serializers.ValidationError("자기 자신을 팔로우할 수 없습니다.")

            return value
        except FarmProfile.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 농장입니다.")

    def create(self, validated_data):
        """팔로우 토글 처리"""
        farm_id = validated_data['farm_id']
        user = self.context['request'].user

        try:
            farm = FarmProfile.objects.get(id=farm_id)
            follow_relation, created = FarmFollow.objects.get_or_create(
                user=user,
                farm=farm
            )

            if created:
                # 팔로우 생성 시 카운트 증가
                farm.follower_count = farm.follower_count + 1
                farm.save()
                return {
                    'is_following': True,
                    'follower_count': farm.follower_count,
                    'message': '농장을 팔로우하였습니다.'
                }
            else:
                # 이미 팔로우 중이면 언팔로우
                follow_relation.delete()
                farm.follower_count = max(0, farm.follower_count - 1)
                farm.save()
                return {
                    'is_following': False,
                    'follower_count': farm.follower_count,
                    'message': '농장 팔로우를 취소하였습니다.'
                }

        except FarmProfile.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 농장입니다.")