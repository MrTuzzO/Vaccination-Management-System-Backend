from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.doctor.user == request.user


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS

        if request.user.user_type == 'doctor':
            return True

        return request.method in permissions.SAFE_METHODS


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS

        if request.user.user_type == 'patient':
            return True

        return request.method in permissions.SAFE_METHODS