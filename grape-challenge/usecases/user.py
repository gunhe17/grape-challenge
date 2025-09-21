from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from repositories import user as user_repo
import jwt
from datetime import datetime, timedelta

# JWT 설정
JWT_SECRET_KEY = "grape-challenge-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


# 사용자 생성
@dataclass
class CreateUserCommand:
    name: str
    cell: str
    role: str = 'user'

def create_user(command: CreateUserCommand) -> Dict[str, Any]:
    """사용자 생성"""
    user = user_repo.create_user(command.name, command.cell, command.role)
    return {
        "id": user["id"],
        "name": user["name"],
        "cell": user["cell"],
        "role": user["role"],
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

# 사용자 정보 조회
@dataclass
class GetUserQuery:
    user_id: str

def get_user_info(query: GetUserQuery) -> Optional[Dict[str, Any]]:
    """사용자 정보 조회"""
    user = user_repo.get_user_by_id(query.user_id)
    if not user:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "cell": user["cell"],
        "role": user["role"],
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

# (Admin) 사용자 전체 조회
@dataclass
class GetAllUsersQuery:
    pass

def get_all_users_admin(query: GetAllUsersQuery) -> List[Dict[str, Any]]:
    """(Admin) 사용자 전체 조회"""
    users = user_repo.get_all_users()
    return [
        {
            "id": user["id"],
            "name": user["name"],
            "cell": user["cell"],
            "role": user["role"],
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        }
        for user in users
    ]

# 로그인 (name, cell) - JWT 토큰 발급
@dataclass
class LoginCommand:
    name: str
    cell: str

def login_user(command: LoginCommand) -> Optional[Dict[str, Any]]:
    """로그인 (name, cell) - JWT 토큰 발급"""
    user = user_repo.get_user_by_login(command.name, command.cell)
    if not user:
        return None

    # JWT 토큰 생성
    if jwt is None:
        # JWT가 없는 경우 임시 토큰 생성
        token = f"temp_token_{user['id']}_{datetime.utcnow().timestamp()}"
    else:
        payload = {
            "user_id": user["id"],
            "name": user["name"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "cell": user["cell"],
            "role": user["role"]
        },
        "token": token
    }

# JWT 토큰 검증
@dataclass
class VerifyTokenQuery:
    token: str

def verify_jwt_token(query: VerifyTokenQuery) -> Optional[Dict[str, Any]]:
    """JWT 토큰 검증"""
    if jwt is None:
        print("Warning: JWT functionality is disabled")
        return None

    try:
        payload = jwt.decode(query.token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Admin 권한 검증
@dataclass
class VerifyAdminQuery:
    token: str

def verify_admin_role(query: VerifyAdminQuery) -> bool:
    """Admin 권한 검증"""
    token_query = VerifyTokenQuery(token=query.token)
    payload = verify_jwt_token(token_query)
    if not payload:
        return False
    return payload.get("role") == "admin"

# 토큰에서 사용자 정보 추출
def get_user_from_token(query: VerifyTokenQuery) -> Optional[Dict[str, Any]]:
    """토큰에서 사용자 정보 추출"""
    payload = verify_jwt_token(query)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    user_query = GetUserQuery(user_id=user_id)
    return get_user_info(user_query)