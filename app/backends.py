from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    """
    Cho phép người dùng đăng nhập bằng username hoặc email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Tìm user có username = input HOẶC email = input
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Trường hợp hiếm: nếu có nhiều user trùng email (thường Django chặn cái này rồi)
            user = User.objects.filter(email=username).order_by('id').first()

        # Kiểm tra mật khẩu
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None