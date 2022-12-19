from rest_framework import permissions

class IsWorker(permissions.IsAuthenticated):
    """
    Permissions для пользователей.
    """

    def has_permission(self, request, view):
        return request.user.is_worker


class IsWorkerOrCurrent(permissions.IsAuthenticated):
    """
    Permissions для пользователей.
    """

    def has_permission(self, request, view):
        return request.user.is_worker or request.user.id == obj.id
