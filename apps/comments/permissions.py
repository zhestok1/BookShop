from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение (GET, HEAD, OPTIONS) любым пользователям,
    но редактирование (PUT, PATCH) и удаление (DELETE) — только автору комментария.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для любого запроса (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменение/удаление разрешено только если автор объекта совпадает с request.user
        return obj.author == request.user