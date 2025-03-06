from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверка на принадлежность к группе moderators.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """
        Проверяет, является ли пользователь создателем курса или урока.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
