"""
User domain endpoint helpers
"""
from typing import Optional, Dict, Any, List
from usecases import user


def api_create_user(name: str, cell: str, role: str = 'user') -> Dict[str, Any]:
    """사용자 생성 API"""
    command = user.CreateUserCommand(name=name, cell=cell, role=role)
    return user.create_user(command)


def api_login(name: str, cell: str) -> Optional[Dict[str, Any]]:
    """로그인 API"""
    command = user.LoginCommand(name=name, cell=cell)
    return user.login_user(command)


def api_get_user_info(user_id: str) -> Optional[Dict[str, Any]]:
    """사용자 정보 조회 API"""
    query = user.GetUserQuery(user_id=user_id)
    return user.get_user_info(query)


def api_get_all_users() -> List[Dict[str, Any]]:
    """(Admin) 사용자 전체 조회 API"""
    query = user.GetAllUsersQuery()
    return user.get_all_users_admin(query)


def api_verify_token(token: str) -> Optional[Dict[str, Any]]:
    """JWT 토큰 검증 API"""
    query = user.VerifyTokenQuery(token=token)
    return user.verify_jwt_token(query)


def api_verify_admin(token: str) -> bool:
    """Admin 권한 검증 API"""
    query = user.VerifyAdminQuery(token=token)
    return user.verify_admin_role(query)


def api_get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """토큰에서 사용자 정보 추출 API"""
    query = user.VerifyTokenQuery(token=token)
    return user.get_user_from_token(query)