from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated


class ArticleViewPermission(BasePermission):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super(UsersViewSet, self).get_permissions()