# -*- coding: utf-8 -*-
import django_filters
from django_filters import rest_framework as filters
from starterkit.drf.permissions import IsAuthenticatedAndIsActivePermission
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response
from tenant_api.pagination import StandardResultsSetPagination
from tenant_api.permissions.skill_set import (
   CanListCreateSkillSetPermission,
   CanRetrieveUpdateDestroySkillSetPermission
)
from tenant_api.serializers.skill_set import (
    SkillSetListCreateSerializer,
    SkillSetRetrieveUpdateDestroySerializer
)
from tenant_foundation.models import SkillSet


class SkillSetListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SkillSetListCreateSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthenticatedAndIsActivePermission,
        CanListCreateSkillSetPermission
    )

    def get_queryset(self):
        """
        List
        """
        queryset = SkillSet.objects.all().order_by('category', 'sub_category')
        return queryset

    def post(self, request, format=None):
        """
        Create
        """
        serializer = SkillSetListCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SkillSetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSetRetrieveUpdateDestroySerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthenticatedAndIsActivePermission,
        CanRetrieveUpdateDestroySkillSetPermission
    )

    def get(self, request, pk=None):
        """
        Retrieve
        """
        skill_set = get_object_or_404(SkillSet, pk=pk)
        self.check_object_permissions(request, skill_set)  # Validate permissions.
        serializer = SkillSetRetrieveUpdateDestroySerializer(skill_set, many=False)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk=None):
        """
        Update
        """
        skill_set = get_object_or_404(SkillSet, pk=pk)
        self.check_object_permissions(request, skill_set)  # Validate permissions.
        serializer = SkillSetRetrieveUpdateDestroySerializer(skill_set, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """
        Delete
        """
        skill_set = get_object_or_404(SkillSet, pk=pk)
        self.check_object_permissions(request, skill_set)  # Validate permissions.
        skill_set.delete()
        return Response(data=[], status=status.HTTP_200_OK)