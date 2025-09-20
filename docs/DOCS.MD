### 서비스 정의 및 기능 명세서

#### 서비스 개요
**서비스명**: 성광교회 청년부 말씀 Tree System  
**대상**: 구리 성광교회 1·2청년부  
**목적**: 매일 말씀 읽기를 통한 신앙 성장 동기 부여

---

### Domain 구조 및 JSON 스키마

#### User Domain
```json
{
  "users": [
    {
      "id": "integer (auto-increment)",
      "name": "string (required)",
      "role": "string (default: 'user', enum: ['user', 'admin'])",
      "created_at": "datetime (ISO format)",
      "updated_at": "datetime (ISO format)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: 회원가입
- **Read**: User 정보 조회, 전체 User 목록 (Admin)
- **Update**: User 정보 수정
- **Delete**: 회원 탈퇴

---

#### Session Domain
```json
{
  "sessions": [
    {
      "id": "integer (auto-increment)",
      "user_id": "integer (required, references users.id)",
      "fruit_id": "integer (optional, references fruit_templates.id)",
      "mission_ids": "array of integers (completed mission ids)",
      "status": "string (default: 'active', enum: ['active', 'completed'])",
      "created_at": "datetime (ISO format)",
      "updated_at": "datetime (ISO format)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: 새로운 Growth Session 시작
- **Read**: 현재 Session 상태 조회
- **Update**: Mission 완료시 mission_ids 추가, 상태 변경
- **Delete**: Session 초기화

---

#### Fruit Template Domain
```json
{
  "fruit_templates": [
    {
      "id": "integer (auto-increment)",
      "name": "string (required)",
      "type": "string (default: 'normal', enum: ['normal', 'special'])",
      "seed_image": "string (optional)",
      "germination_image": "string (optional)",
      "seedling_image": "string (optional)",
      "juvenile_image": "string (optional)",
      "vegetative_image": "string (optional)",
      "reproductive_image": "string (optional)",
      "fruiting_image": "string (optional)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: 새 과일 Template 생성 (Admin)
- **Read**: 과일 Template 목록 조회
- **Update**: Template 정보 수정 (Admin)
- **Delete**: Template 삭제 (Admin)

---

#### Fruit Domain
```json
{
  "fruits": [
    {
      "id": "integer (auto-increment)",
      "template_id": "integer (required, references fruit_templates.id)",
      "status": "string (default: '씨앗', enum: ['씨앗', '새싹', '나무', '열매'])",
      "created_at": "datetime (ISO format)",
      "updated_at": "datetime (ISO format)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: Session 완료시 과일 생성
- **Read**: 보유 과일 조회
- **Update**: 과일 Growth 상태 변경
- **Delete**: 과일 삭제

---

#### Mission Template Domain
```json
{
  "mission_templates": [
    {
      "id": "integer (auto-increment)",
      "name": "string (required)",
      "type": "string (default: 'normal', enum: ['normal', 'special'])",
      "content": "string (required)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: 새 Mission Template 생성 (Admin)
- **Read**: Mission Template 목록 조회
- **Update**: Template 내용 수정 (Admin)
- **Delete**: Template 삭제 (Admin)

---

#### Mission Domain
```json
{
  "missions": [
    {
      "id": "integer (auto-increment)",
      "template_id": "integer (required, references mission_templates.id)",
      "status": "string (default: 'pending', enum: ['pending', 'completed'])",
      "created_at": "datetime (ISO format)",
      "completed_at": "datetime (ISO format, optional)"
    }
  ]
}
```

**CRUD Operations**
- **Create**: 일일 Mission 생성
- **Read**: Mission 상태 조회
- **Update**: Mission 완료 처리
- **Delete**: Mission 삭제

---

### JSON Repository Pattern

#### Base Repository
```python
class BaseRepository:
    def __init__(self, json_path):
        self.json_path = json_path
    
    def load_data(self):
        """JSON 파일에서 데이터 로드"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """JSON 파일에 데이터 저장"""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
```

#### User Repository
```python
class UserRepository(BaseRepository):
    def create(self, name, role='user')
    def get_by_id(self, user_id)
    def get_all(self)
    def update(self, user_id, **kwargs)
    def delete(self, user_id)
```

#### Session Repository
```python
class SessionRepository(BaseRepository):
    def create(self, user_id, fruit_id=None)
    def get_by_user_id(self, user_id)
    def get_all(self)
    def update_mission_ids(self, session_id, mission_ids)
    def update_status(self, session_id, status)
    def delete(self, session_id)
```

#### Fruit Template Repository
```python
class FruitTemplateRepository(BaseRepository):
    def create(self, name, type, **images)
    def get_by_id(self, template_id)
    def get_all(self)
    def update(self, template_id, **kwargs)
    def delete(self, template_id)
```

#### Fruit Repository
```python
class FruitRepository(BaseRepository):
    def create(self, template_id, status)
    def get_by_id(self, fruit_id)
    def update_status(self, fruit_id, status)
    def delete(self, fruit_id)
```

#### Mission Template Repository
```python
class MissionTemplateRepository(BaseRepository):
    def create(self, name, type, content)
    def get_by_id(self, template_id)
    def get_all(self)
    def update(self, template_id, **kwargs)
    def delete(self, template_id)
```

#### Mission Repository
```python
class MissionRepository(BaseRepository):
    def create(self, template_id, status)
    def get_by_id(self, mission_id)
    def get_all(self)
    def update_status(self, mission_id, status)
    def check_daily_limit(self, user_id, date)
    def delete(self, mission_id)
```

---

### API Endpoints

#### Authentication
```
POST /login
Body: { "name": "string" }
Response: { "user_id": int, "role": "string", "token": "string" }
```

#### User APIs
```
POST /users
Body: { "name": "string", "role": "string" }

GET /users/{user_id}
Response: { "id": int, "name": "string", "role": "string" }

GET /users
Response: [{ "id": int, "name": "string", "role": "string" }]

PUT /users/{user_id}
Body: { "name": "string", "role": "string" }

PATCH /users/{user_id}
Body: { "name": "string" }

DELETE /users/{user_id}
```

#### Session APIs
```
POST /sessions
Body: { "user_id": int, "fruit_id": int }

GET /sessions/user/{user_id}
Response: { "id": int, "user_id": int, "fruit_id": int, "mission_ids": [], "status": "string" }

GET /sessions
Response: [{ "id": int, "user_id": int, "mission_ids": [], "status": "string" }]

PUT /sessions/{session_id}
Body: { "fruit_id": int, "mission_ids": [], "status": "string" }

PATCH /sessions/{session_id}/missions
Body: { "mission_ids": [] }

PATCH /sessions/{session_id}/status
Body: { "status": "string" }

DELETE /sessions/{session_id}
```

#### Fruit Template APIs
```
POST /fruit-templates
Body: { "name": "string", "type": "string", "seed_image": "string", ... }

GET /fruit-templates
Response: [{ "id": int, "name": "string", "type": "string", ... }]

GET /fruit-templates/{template_id}
Response: { "id": int, "name": "string", "type": "string", ... }

PUT /fruit-templates/{template_id}
Body: { "name": "string", "type": "string", "seed_image": "string", ... }

PATCH /fruit-templates/{template_id}
Body: { "name": "string" }

DELETE /fruit-templates/{template_id}
```

#### Fruit APIs
```
POST /fruits
Body: { "template_id": int, "status": "string" }

GET /fruits/{fruit_id}
Response: { "id": int, "template_id": int, "status": "string", "created_at": "datetime" }

PUT /fruits/{fruit_id}
Body: { "template_id": int, "status": "string" }

PATCH /fruits/{fruit_id}/status
Body: { "status": "string" }

DELETE /fruits/{fruit_id}
```

#### Mission Template APIs
```
POST /mission-templates
Body: { "name": "string", "type": "string", "content": "string" }

GET /mission-templates
Response: [{ "id": int, "name": "string", "type": "string", "content": "string" }]

GET /mission-templates/{template_id}
Response: { "id": int, "name": "string", "type": "string", "content": "string" }

PUT /mission-templates/{template_id}
Body: { "name": "string", "type": "string", "content": "string" }

PATCH /mission-templates/{template_id}
Body: { "content": "string" }

DELETE /mission-templates/{template_id}
```

#### Mission APIs
```
POST /missions
Body: { "template_id": int, "status": "string" }

GET /missions/{mission_id}
Response: { "id": int, "template_id": int, "status": "string", "created_at": "datetime", "completed_at": "datetime" }

GET /missions
Response: [{ "id": int, "template_id": int, "status": "string", "created_at": "datetime" }]

PUT /missions/{mission_id}
Body: { "template_id": int, "status": "string" }

PATCH /missions/{mission_id}/complete
Body: { "completed_at": "datetime" }

DELETE /missions/{mission_id}
```

---

### Page별 기능 Mapping

#### Login Page
```
Components:
├── LoginForm
└── LoginButton

APIs:
└── POST /login
```

#### Home Page
```
Components:
├── CurrentFruitProgress
│   ├── FruitImage (mission_ids count에 따른 이미지)
│   └── ProgressBar (7단계 진행률)
├── TodayMission
│   ├── MissionContent
│   └── CompleteButton
└── MissionHistory

APIs:
├── GET /sessions/user/{user_id}
├── GET /fruit-templates/{template_id}
├── GET /mission-templates
├── POST /missions
└── PATCH /sessions/{session_id}/missions
```

#### Fruit Page
```
Components:
├── CompletedFruits
│   └── FruitCard
└── FruitGallery

APIs:
├── GET /sessions/user/{user_id}
└── GET /fruit-templates
```

#### Admin Dashboard Page
```
Components:
├── UserStats
│   ├── UserList
│   ├── ParticipationRate
│   └── CompletionStats
└── OverallStats

APIs:
├── GET /users
├── GET /sessions
└── GET /missions
```

#### Admin Fruit Page
```
Components:
├── FruitTemplateList
├── AddFruitForm
└── EditFruitForm

APIs:
├── GET /fruit-templates
├── POST /fruit-templates
├── PUT /fruit-templates/{template_id}
└── DELETE /fruit-templates/{template_id}
```

---

### 핵심 Business Logic

#### Mission 완료 Process
```
1. 하루 1회 제한 체크 (오늘 날짜로 completed mission 존재 여부)
2. Mission 생성 및 완료 처리
3. Session의 mission_ids에 추가
4. mission_ids count가 7이면:
   - 현재 session status = 'completed'
   - 새로운 session 생성
```

#### Fruit Image 표시 Logic
```
mission_ids count:
0-1: seed_image
2: germination_image
3: seedling_image
4: juvenile_image
5: vegetative_image
6: reproductive_image
7: fruiting_image (완성)
```