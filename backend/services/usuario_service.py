from backend.entities import Usuario
from backend.repositories.usuario_repository import UsuarioRepository
from backend.schemas.requests import UsuarioLogin, UsuarioRegistro
from backend.services import auditoria, seguridad

MODULO = "Usuarios"


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def registrar(self, datos: UsuarioRegistro) -> Usuario:
        usuario = Usuario(
            nombre_completo=datos.nombre_completo,
            correo=datos.correo,
            password_hash=seguridad.hash_password(datos.password),
        )
        usuario = self.repository.add(usuario)
        auditoria.registrar(
            MODULO, "Registro", f"Se registró el usuario {usuario.nombre_completo}.",
            actor=usuario.nombre_completo,
        )
        return usuario

    def login(self, datos: UsuarioLogin) -> "Usuario | None":
        usuario = self.repository.get_by_correo(datos.correo)
        if usuario is None or not seguridad.verificar_password(datos.password, usuario.password_hash):
            return None
        auditoria.registrar(
            MODULO, "Inicio de sesión", f"{usuario.nombre_completo} inició sesión.",
            actor=usuario.nombre_completo,
        )
        return usuario
