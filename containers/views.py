# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from serializers import CgroupSerializer
from django.shortcuts import render
from cgroupspy import trees
from cgroups import Cgroup
from . import Nix_Cgroup

def get_cgroups():
    cgrp_tree = trees.Tree()
    cgrp_nodes = cgrp_tree.root.children
    cgroups = [Cgroup(name=node.name) for node in cgrp_nodes]
    nix_cgrps = []
    return nix_cgrps

nix_cgroups = get_cgroups

# Create your views here.
class CgroupViewSet(viewsets.ViewSet): # or GenericViewSet
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = CgroupSerializer

    def list(self, request):
        serializer = CgroupSerializer(instance=nix_cgroups.values(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CgroupSerializer(data=request.data)
        if serializer.is_valid():
            nix_cgroup = serializer.save()
            nix_cgroup.id = get_next_task_id()
            nix_cgroups[nix_cgroup.id] = nix_cgroup
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            nix_cgroup = nix_cgroups[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CgroupSerializer(instance=nix_cgroup)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            nix_cgroup = nix_cgroups[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CgroupSerializer(data=request.data, instance=nix_cgroup)
        if serializer.is_valid():
            nix_cgroup = serializer.save()
            nix_cgroups[nix_cgroup.id] = nix_cgroup
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            nix_cgroup = nix_cgroups[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CgroupSerializer(data=request.data, instance=nix_cgroup, partial=True)
        if serializer.is_valid():
            nix_cgroup = serializer.save()
            nix_cgroups[nix_cgroup.id] = nix_cgroup
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            nix_cgroup = nix_cgroups[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del nix_cgroups[nix_cgroup.id]
        return Response(status=status.HTTP_204_NO_CONTENT)