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
      "id": "uuid",
      "name": "string (required)",
      "cell": "string (required)",
      "role": "string (required)",
      "created_at": "datetime (ISO format)"
    }
  ]
}
```

**Usecase**
- **Create**:
  - 사용자 생성
- **Read**:
  - 로그인 (name, cell)
  - 사용자 정보 조회
  - (Admin) 사용자 전체 조회

---

#### Session Domain
```json
{
  "sessions": [
    {
      "id": "uuid",
      "user_id": "uuid (required, references users.id)",
      "fruit_id": "uuid (optional, references fruits.id)",
      "mission_ids": "array of uuids (optional, references missions.id)",
      "status": "string (default: 'in progress', enum: ['in progress', 'completed'])",
      "created_at": "datetime (ISO format)",
      "updated_at": "datetime (ISO format)"
    }
  ]
}
```

**Usecase**
- **Create**: 세션 시작
- **Read**:
  - 현재 세션 상태 조회
  - 진행 중인 세션 조회
- **Update**: 미션 완료 시 mission_ids 추가, 상태 변경

---

#### Fruit Template Domain
```json
{
  "fruit_templates": [
    {
      "id": "integer (auto-increment)",
      "name": "string (required)",
      "type": "string (default: 'normal', enum: ['normal', 'special'])",
      "status_images": {
        "first": "string (optional)",
        "second": "string (optional)",
        "third": "string (optional)",
        "fourth": "string (optional)",
        "fifth": "string (optional)",
        "sixth": "string (optional)",
        "seventh": "string (optional)"
      }
    }
  ]
}
```

**Usecase**
- **Create**: 새 과일 템플릿 생성 (Admin)
- **Read**: 과일 템플릿 목록 조회
- **Update**: 템플릿 정보 수정 (Admin)
- **Delete**: 불가 (기존 과일 참조 무결성 보호)

---

#### Fruit Domain
```json
{
  "fruits": [
    {
      "id": "uuid",
      "template_id": "integer (required, references fruit_templates.id)",
      "status": "string (default: 'first', enum: ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh'])",
      "created_at": "datetime (ISO format)",
      "updated_at": "datetime (ISO format)"
    }
  ]
}
```

**Usecase**
- **Create**: 과일 생성
- **Read**: 보유 과일 조회
- **Update**: 과일 상태 변경
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

**Usecase**
- **Create**: 미션 템플릿 생성 (Admin)
- **Read**: 미션 템플릿 목록 조회
- **Update**: 템플릿 내용 수정 (Admin)
- **Delete**: 불가 (기존 미션 참조 무결성 보호)

---

#### Mission Domain
```json
{
  "missions": [
    {
      "id": "uuid",
      "template_id": "integer (required, references mission_templates.id)",
      "completed_at": "datetime (ISO format)",
      "created_at": "datetime (ISO format)",
    }
  ]
}
```

**Usecase**
- **Create**: 미션 생성
- **Read**: 미션 조회
- **Delete**: 미션 삭제

---

### Page별 기능 Mapping

#### Login Page
```
Components:
├── LoginForm
└── LoginButton

트랜잭션 단위 API Flow:

1. 로그인 시도
   POST /user/login
   {
     "name": "string",
     "cell": "string"
   }

   처리 단계:
   - User 인증 (name + cell 조합으로 검증)
   - 성공 시 user 정보 및 JWT 토큰 반환
   - 실패 시 401 Unauthorized

   성공 응답:
   {
     "user": {
       "id": "uuid",
       "name": "string",
       "cell": "string",
       "role": "string"
     },
     "token": "jwt_token"
   }
```

#### Home Page
```
Components:
├── CurrentFruitProgress
│   ├── FruitImage (fruit status에 따른 이미지)
│   └── ProgressBar (7단계 진행률)
├── TodayMission
│   ├── MissionContent
│   └── CompleteButton
└── MissionHistory

트랜잭션 단위 API Flow:

1. 페이지 로드 (3개 API 병렬 호출)
   GET /session/user/{user_id}/in-progress
   GET /mission-template/{mission_template_id}
   GET /fruit-template/{template_id} (과일 이미지용, session에 fruit가 있을 때)

   처리 결과:
   - 현재 Session 상태 (mission_ids 개수로 진행률 표시)
   - 오늘의 Mission Template (랜덤 선택)
   - Fruit 이미지 (status에 따른 단계 이미지)

2. Mission 완료 (Atomic Transaction)
   POST /mission/complete
   {
     "user_id": "uuid",
     "mission_template_id": "integer"
   }

   처리 단계 (All or Nothing):
   a) 하루 1회 제한 체크
   b) Mission 생성 (completed_at = now)
   c) Session mission_ids 배열에 추가
   d) 첫 Mission인 경우: Fruit 생성 + Session fruit_id 업데이트
   e) 기존 Fruit status 업데이트 (mission 개수에 따라)
   f) 7개 완료 시: Session 완료 + 새 Session 생성

   성공 응답:
   {
     "mission": { "id": "uuid", "template_id": 1, "completed_at": "2024-01-01T10:00:00Z" },
     "session": { "id": "uuid", "mission_ids": ["uuid1", "uuid2"], "fruit_id": "uuid" },
     "fruit": { "id": "uuid", "status": "second", "template_id": 3 }
   }
```

#### Fruit Page
```
Components:
├── CompletedFruits
│   └── FruitCard
└── FruitGallery

트랜잭션 단위 API Flow:

1. 페이지 로드 (완료된 과일 목록 표시)
   GET /sessions/user/{user_id}?status=completed
   GET /fruit-templates (전체 템플릿 목록)

   처리 결과:
   - 완료된 Session 목록과 연결된 Fruit 정보
   - 각 Fruit의 Template 정보로 이미지 표시
   - 완료 날짜순 정렬
```

#### Admin Dashboard Page
```
Components:
├── UserStatistics
│   ├── TotalUserCount
│   └── UserTable
│       ├── UserInfo (name, cell, role)
│       └── SessionCount (total/completed)
├── SystemOverview
│   ├── DailyActiveUsers
│   └── CompletionRates
└── TemplateManagement
    ├── FruitTemplateList
    └── MissionTemplateList

트랜잭션 단위 API Flow:

1. 대시보드 로드 (통계 데이터 조회)
   GET /admin/users/statistics

   처리 결과:
   {
     "total_users": 150,
     "users": [
       {
         "id": "uuid",
         "name": "홍길동",
         "cell": "1청년부",
         "role": "member",
         "statistics": {
           "total_sessions": 12,
           "completed_sessions": 10
         }
       }
     ]
   }
```

---

### 핵심 Business Logic

#### Mission 완료 Workflow (Atomic Transaction)
```
POST /mission/complete
{
  "user_id": "uuid",
  "mission_template_id": "integer"
}

처리 순서 (Transaction):
1. 하루 1회 제한 체크 (오늘 날짜로 completed_at이 있는 mission 확인)
2. Mission 생성 (completed_at = now)
3. 현재 in-progress Session 조회
4. Session의 mission_ids에 추가
5. Session에 첫 mission인 경우:
   - Fruit 생성 (status: 'first', random template)
   - Session의 fruit_id 업데이트
6. 기존 Fruit이 있는 경우 status 업데이트
7. mission_ids.length == 7인 경우:
   - 현재 Session status = 'completed'
   - 새 Session 생성 (fruit_id = null)

성공 응답:
{
  "mission": { ... },
  "session": { ... },
  "fruit": { ... }
}
```

#### Session-Mission-Fruit 관계
```
- 한 Session은 여러 날에 걸쳐 진행됨 (최대 7일)
- 하루에 1개의 Mission만 완료 가능
- Session 시작 시 fruit_id는 null
- 첫 Mission 완료 시 Fruit 생성 및 할당
- Session 완료 시 Fruit도 최종 상태(seventh)가 됨
- 완료된 Session과 Fruit는 조회만 가능 (수정/삭제 불가)
```