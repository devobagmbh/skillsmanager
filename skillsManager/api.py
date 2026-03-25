from django_filters import rest_framework
from rest_framework import serializers, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from skillsManager.models import Skill, ProfileSkillReference, Profile


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SkillFilterSet(rest_framework.FilterSet):
    class Meta:
        model = Skill
        fields = ["name", "description"]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = SkillFilterSet


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileFilterSet(rest_framework.FilterSet):
    class Meta:
        model = Profile
        fields = ["given_name", "last_name", "email", "active_since", "active_until"]


class ProfileSkillReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileSkillReference
        fields = "__all__"


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = ProfileFilterSet

    @action(detail=True)
    def skills(self, request, pk=None):
        profile = self.get_object()
        referenced_skills = ProfileSkillReference.objects.filter(profile=profile)

        page = self.paginate_queryset(referenced_skills)
        if page is not None:
            serializer = ProfileSkillReferenceSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProfileSkillReferenceSerializer(referenced_skills, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileSkillReferenceFilterSet(rest_framework.FilterSet):
    class Meta:
        model = ProfileSkillReference
        fields = ["profile", "skill", "level", "favorite", "remarks"]


class ProfileSkillReferenceViewSet(viewsets.ModelViewSet):
    queryset = ProfileSkillReference.objects.all()
    serializer_class = ProfileSkillReferenceSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = ProfileSkillReferenceFilterSet


v1_router = routers.DefaultRouter()
v1_router.register("v1/skills", SkillViewSet)
v1_router.register("v1/profiles", ProfileViewSet)
v1_router.register("v1/profile-skill-references", ProfileSkillReferenceViewSet)
