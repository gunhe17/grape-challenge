from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    def login(self, name: str, cell: str) -> dict:
        try:
            # 이름과 셀로 사용자 조회 (미리 등록된 사용자만 로그인 가능)
            user = self.user_repo.get_by_name_and_cell(name, cell)
            
            if not user:
                return {
                    "success": False,
                    "error": "등록되지 않은 사용자입니다. 이름과 셀 정보를 확인해주세요."
                }
            
            access_token = self.create_access_token(
                data={"sub": str(user["id"]), "name": user["name"], "cell": user["cell"], "role": user["role"]}
            )
            return {
                "success": True,
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user["id"],
                "name": user["name"],
                "cell": user["cell"],
                "role": user["role"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        payload = self.verify_token(token)
        if not payload:
            return None
        
        # JWT 토큰에서 직접 사용자 정보 반환 (DB 재조회 불필요)
        user_id = payload.get("sub")
        name = payload.get("name")
        cell = payload.get("cell")
        role = payload.get("role")
        
        if not user_id:
            return None
            
        return {
            "id": int(user_id),
            "name": name,
            "cell": cell,
            "role": role
        }