from rest_framework import permissions

class IsWorkerOrOwner(permissions.IsAuthenticated):
    """
    Permissions для автомобилей.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_worker or request.user.id == obj.user_id
