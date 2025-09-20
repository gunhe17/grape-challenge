from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..repositories.user_repository import UserRepository  
from ..routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/users", tags=["users"])
user_repo = UserRepository()

@router.get("/")
def get_all_users(current_user: Dict[str, Any] = Depends(require_admin)):
    """관리자만 전체 사용자 목록 조회 가능"""
    return user_repo.get_all_users()

@router.get("/{user_id}")
def get_user(user_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    """특정 사용자 정보 조회"""
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user