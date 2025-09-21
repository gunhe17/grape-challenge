"""
Page Endpoints for Web Interface
"""
from typing import Optional, Dict, Any, List
from fastapi import Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date

from usecases.user import LoginCommand, login_user, get_user_info, GetUserQuery, verify_jwt_token, VerifyTokenQuery
from usecases.mission_workflow import CompleteMissionWorkflowCommand, complete_mission_workflow, GetRandomMissionTemplateQuery, get_random_mission_template
from repositories import session as session_repo, fruit as fruit_repo, mission as mission_repo, user as user_repo

templates = Jinja2Templates(directory="web/templates")

def get_fruit_emoji(fruit_name: str) -> str:
    """Get emoji representation for fruit names"""
    fruit_emojis = {
        '사과': '🍎', '바나나': '🍌', '포도': '🍇', '오렌지': '🍊',
        '딸기': '🍓', '복숭아': '🍑', '수박': '🍉', '파인애플': '🍍',
        '키위': '🥝', '망고': '🥭', '레몬': '🍋', '체리': '🍒',
        '자두': '🫐', '블루베리': '🫐'
    }
    return fruit_emojis.get(fruit_name, '🍎')

def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """Get user info from JWT token"""
    if not token:
        return None
    try:
        query = VerifyTokenQuery(token=token)
        payload = verify_jwt_token(query)
        if not payload:
            return None
        user_id = payload.get("user_id")
        if not user_id:
            return None
        user_query = GetUserQuery(user_id=user_id)
        return get_user_info(user_query)
    except Exception:
        return None

def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """Get current user from request cookies"""
    token = request.cookies.get("access_token")
    return get_user_from_token(token)

def require_auth(request: Request) -> Dict[str, Any]:
    """Require authentication for protected routes"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def require_admin(request: Request) -> Dict[str, Any]:
    """Require admin authentication"""
    user = require_auth(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def is_daily_mission_completed(user_id: str) -> bool:
    """Check if user has completed today's mission"""
    today = date.today().isoformat()
    all_missions = mission_repo.get_all_missions()
    return any(
        m.get('completed_at') and str(m.get('completed_at', '')).startswith(today)
        for m in all_missions
    )

def get_user_completed_fruits(user_id: str) -> List[Dict[str, Any]]:
    """Get all completed fruits for a user"""
    completed_sessions = session_repo.get_sessions_by_user(user_id, "completed")
    completed_fruits = []
    for session in completed_sessions:
        if session.get('fruit_id'):
            fruit = fruit_repo.get_fruit_by_id(session['fruit_id'])
            if fruit:
                fruit_template = fruit_repo.get_fruit_template_by_id(fruit['template_id'])
                if fruit_template:
                    completed_fruits.append({
                        'template': fruit_template,
                        'completed_date': session.get('updated_at', '')[:10] if session.get('updated_at') else '',
                        'type': fruit_template.get('type', 'normal')
                    })
    return completed_fruits

def page_login(request: Request):
    """Show login page"""
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/home", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

def page_login_post(request: Request, name: str, cell: str):
    """Handle login form submission"""
    try:
        login_cmd = LoginCommand(name=name, cell=cell)
        result = login_user(login_cmd)
        if not result:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "messages": [{"type": "error", "text": "로그인에 실패했습니다. 이름과 소속을 확인해주세요."}]
            })
        response = RedirectResponse(url="/home", status_code=302)
        response.set_cookie(
            key="access_token", value=result["token"], httponly=True,
            max_age=86400, samesite="lax"
        )
        return response
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "messages": [{"type": "error", "text": f"오류가 발생했습니다: {str(e)}"}]
        })

def page_home(request: Request):
    """Show home page"""
    user = require_auth(request)
    try:
        current_session = session_repo.get_session_by_user_and_status(user['id'], "in progress")
        current_fruit = None
        mission_count = 0

        if current_session:
            mission_count = len(current_session.get('mission_ids', []))
            if current_session.get('fruit_id'):
                fruit = fruit_repo.get_fruit_by_id(current_session['fruit_id'])
                if fruit:
                    fruit_template = fruit_repo.get_fruit_template_by_id(fruit['template_id'])
                    if fruit_template:
                        current_fruit = {
                            'template': fruit_template,
                            'status': fruit.get('status', 'first')
                        }

        today_mission_query = GetRandomMissionTemplateQuery()
        today_mission = get_random_mission_template(today_mission_query)
        daily_completed = is_daily_mission_completed(user['id'])

        return templates.TemplateResponse("home.html", {
            "request": request, "user": user, "current_fruit": current_fruit,
            "mission_count": mission_count, "today_mission": today_mission,
            "daily_completed": daily_completed
        })
    except Exception as e:
        return templates.TemplateResponse("home.html", {
            "request": request, "user": user, "current_fruit": None,
            "mission_count": 0, "today_mission": None, "daily_completed": False,
            "messages": [{"type": "error", "text": f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}"}]
        })

def page_mission_complete(request: Request, mission_template_id: str):
    """Handle mission completion"""
    user = require_auth(request)
    try:
        cmd = CompleteMissionWorkflowCommand(user_id=user['id'], mission_template_id=mission_template_id)
        result = complete_mission_workflow(cmd)
        return RedirectResponse(url="/home", status_code=302)
    except ValueError as e:
        return RedirectResponse(url="/home", status_code=302)
    except Exception as e:
        return RedirectResponse(url="/home", status_code=302)

def page_fruits(request: Request):
    """Show fruits page"""
    user = require_auth(request)
    try:
        completed_fruits = get_user_completed_fruits(user['id'])
        return templates.TemplateResponse("fruits.html", {
            "request": request, "completed_fruits": completed_fruits
        })
    except Exception as e:
        return templates.TemplateResponse("fruits.html", {
            "request": request, "completed_fruits": [],
            "messages": [{"type": "error", "text": f"과일 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}"}]
        })

def page_admin(request: Request):
    """Show admin dashboard"""
    user = require_admin(request)
    try:
        all_users = user_repo.get_all_users()
        user_stats = []
        for u in all_users:
            user_sessions = session_repo.get_sessions_by_user(u['id'])
            total_sessions = len(user_sessions)
            completed_sessions = len([s for s in user_sessions if s.get('status') == 'completed'])
            user_stats.append({
                'name': u['name'], 'cell': u['cell'], 'role': u['role'],
                'statistics': {'total_sessions': total_sessions, 'completed_sessions': completed_sessions}
            })
        stats = {'total_users': len(all_users), 'users': user_stats}
        return templates.TemplateResponse("admin.html", {"request": request, "stats": stats})
    except Exception as e:
        return templates.TemplateResponse("admin.html", {
            "request": request, "stats": {'total_users': 0, 'users': []},
            "messages": [{"type": "error", "text": f"관리자 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}"}]
        })