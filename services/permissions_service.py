"""
Solicitação de permissões Android, adequada à versão do sistema:

- Android 13+ (API 33+): READ_MEDIA_IMAGES
- Android 6 a 12 (API 23-32): READ_EXTERNAL_STORAGE / WRITE_EXTERNAL_STORAGE

Em plataformas que não são Android (ex.: testes em desktop), as
chamadas são ignoradas com segurança.
"""
from kivy.utils import platform


def _sdk_int():
    from jnius import autoclass
    build_version = autoclass("android.os.Build$VERSION")
    return build_version.SDK_INT


def request_storage_permissions(callback=None):
    """
    Solicita apenas as permissões estritamente necessárias para ler
    imagens da galeria, de acordo com a versão do Android instalada.
    """
    if platform != "android":
        if callback:
            callback(True)
        return

    from android.permissions import Permission, request_permissions

    if _sdk_int() >= 33:
        perms = [Permission.READ_MEDIA_IMAGES]
    else:
        perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]

    def _on_result(permissions, grant_results):
        granted = all(grant_results)
        if callback:
            callback(granted)

    request_permissions(perms, _on_result)


def has_storage_permission():
    if platform != "android":
        return True

    from android.permissions import Permission, check_permission

    if _sdk_int() >= 33:
        return check_permission(Permission.READ_MEDIA_IMAGES)
    return check_permission(Permission.READ_EXTERNAL_STORAGE)
