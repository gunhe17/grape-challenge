# 페이지별 상세 기능 명세서

## 1. Login Page (/login)

### 기능 요구사항
- 사용자 이름과 셀(다윗셀/아브라함셀) 선택으로 로그인
- JWT 토큰 발급 및 로컬 스토리지 저장
- 로그인 성공 시 홈 페이지로 자동 이동
- 관리자 계정 별도 처리

### UI 컴포넌트
```
LoginPage
├── LoginForm
│   ├── NameInput (텍스트 입력)
│   ├── CellSelector (다윗셀/아브라함셀 선택)
│   └── LoginButton
└── ErrorMessage (로그인 실패 시)
```

### API 호출
```javascript
POST /api/login
Request: {
  "name": "string",
  "cell": "string"  // "다윗셀" or "아브라함셀"
}
Response: {
  "success": true,
  "user_id": 1,
  "name": "홍길동",
  "cell": "다윗셀",
  "role": "user",
  "token": "jwt_token_string"
}
```

### 상태 관리
- `isLoading`: 로그인 처리 중 상태
- `error`: 에러 메시지
- `currentUser`: 로그인된 사용자 정보

---

## 2. Home Page (/)

### 기능 요구사항
- 현재 진행 중인 과일 성장 상태 표시 (7단계)
- 오늘의 미션 표시 및 완료 처리
- 미션 완료 시 과일 성장 애니메이션
- 7개 미션 완료 시 새로운 세션 자동 생성

### UI 컴포넌트
```
HomePage
├── Header
│   ├── UserInfo (이름, 셀)
│   └── LogoutButton
├── CurrentFruitProgress
│   ├── FruitImage
│   │   └── 단계별 이미지 표시
│   │       - 0-1개: seed_image
│   │       - 2개: germination_image
│   │       - 3개: seedling_image
│   │       - 4개: juvenile_image
│   │       - 5개: vegetative_image
│   │       - 6개: reproductive_image
│   │       - 7개: fruiting_image
│   └── ProgressBar
│       └── 7단계 진행률 표시 (mission_ids.length / 7)
├── TodayMission
│   ├── MissionCard
│   │   ├── MissionTitle
│   │   ├── MissionContent
│   │   └── CompleteButton
│   └── CompletionStatus (완료/미완료)
└── RecentActivity
    └── 최근 3일간 미션 완료 현황
```

### API 호출 순서
```javascript
// 1. 사용자 세션 조회
GET /api/sessions/user/{user_id}
Response: {
  "id": 1,
  "user_id": 1,
  "fruit_id": 1,
  "mission_ids": [1, 2, 3],  // 완료된 미션 ID 목록
  "status": "active"
}

// 2. 현재 과일 템플릿 정보 조회
GET /api/fruit-templates/{template_id}
Response: {
  "id": 1,
  "name": "포도",
  "type": "normal",
  "seed_image": "url",
  "germination_image": "url",
  ...
}

// 3. 미션 템플릿 조회
GET /api/mission-templates
Response: [{
  "id": 1,
  "name": "말씀 묵상",
  "type": "normal",
  "content": "오늘의 말씀을 읽고 묵상하세요"
}]

// 4. 미션 생성 (하루 1회)
POST /api/missions
Request: {
  "template_id": 1,
  "user_id": 1,
  "status": "pending"
}

// 5. 미션 완료 처리
PATCH /api/missions/{mission_id}/complete
Response: {
  "success": true,
  "mission": {...}
}

// 6. 세션 업데이트 (미션 ID 추가)
PATCH /api/sessions/{session_id}/missions
Request: {
  "mission_ids": [1, 2, 3, 4]  // 새로운 미션 ID 추가
}

// 7. 7개 완료 시 세션 종료 및 새 세션 생성
PATCH /api/sessions/{session_id}/status
Request: {
  "status": "completed"
}

POST /api/sessions
Request: {
  "user_id": 1,
  "fruit_id": null  // 새로운 과일로 시작
}
```

### 비즈니스 로직
```javascript
// 미션 완료 프로세스
function completeMission() {
  // 1. 오늘 이미 완료했는지 확인
  if (hasCompletedToday()) return showError("오늘은 이미 완료했습니다");

  // 2. 미션 완료 처리
  const mission = await completeMissionAPI(missionId);

  // 3. 세션에 미션 ID 추가
  session.mission_ids.push(mission.id);
  await updateSession(session.id, session.mission_ids);

  // 4. 7개 완료 확인
  if (session.mission_ids.length === 7) {
    // 현재 세션 완료
    await updateSessionStatus(session.id, "completed");
    // 새 세션 생성
    await createNewSession(userId);
    // 열매 생성
    await createFruit(templateId, "열매");
  }

  // 5. UI 업데이트
  updateFruitImage(session.mission_ids.length);
  showSuccessAnimation();
}
```

---

## 3. Fruit Page (/fruits)

### 기능 요구사항
- 완성된 과일 목록 표시 (갤러리 형태)
- 과일별 완성 날짜 표시
- 현재 진행 중인 과일 별도 표시
- 과일 상세 정보 모달

### UI 컴포넌트
```
FruitPage
├── CurrentFruit
│   ├── FruitCard (진행 중)
│   └── ProgressIndicator
├── CompletedFruits
│   ├── FruitGrid
│   │   └── FruitCard[]
│   │       ├── FruitImage
│   │       ├── FruitName
│   │       └── CompletionDate
│   └── EmptyState (완성된 과일 없음)
└── FruitModal
    ├── FruitDetails
    ├── GrowthHistory
    └── CloseButton
```

### API 호출
```javascript
// 1. 사용자 세션 조회 (현재 진행 중인 과일)
GET /api/sessions/user/{user_id}

// 2. 완성된 과일 목록 조회
GET /api/fruits?user_id={user_id}&status=열매

// 3. 과일 템플릿 정보
GET /api/fruit-templates
```

---

## 4. Admin Dashboard Page (/admin)

### 기능 요구사항
- 전체 사용자 참여 현황 대시보드
- 셀별 통계 (다윗셀/아브라함셀)
- 일일/주간/월간 통계
- 사용자별 상세 현황 조회

### UI 컴포넌트
```
AdminDashboard
├── StatsOverview
│   ├── TotalUsers
│   ├── ActiveUsers (오늘 미션 완료)
│   ├── CompletionRate
│   └── TotalFruits
├── CellComparison
│   ├── DavidCellStats
│   └── AbrahamCellStats
├── UserTable
│   ├── SearchFilter
│   ├── UserList
│   │   ├── UserRow[]
│   │   │   ├── Name
│   │   │   ├── Cell
│   │   │   ├── CurrentProgress
│   │   │   ├── TotalFruits
│   │   │   └── LastActivity
│   └── Pagination
└── Charts
    ├── DailyActivityChart
    └── WeeklyProgressChart
```

### API 호출
```javascript
// 1. 전체 사용자 목록
GET /api/users

// 2. 전체 세션 정보
GET /api/sessions

// 3. 전체 미션 정보
GET /api/missions

// 4. 통계 계산 (클라이언트 사이드)
function calculateStats(users, sessions, missions) {
  return {
    totalUsers: users.length,
    activeToday: missions.filter(m => isToday(m.created_at)).length,
    davidCell: users.filter(u => u.cell === "다윗셀").length,
    abrahamCell: users.filter(u => u.cell === "아브라함셀").length,
    completionRate: calculateCompletionRate(sessions),
    weeklyTrend: calculateWeeklyTrend(missions)
  };
}
```

---

## 5. Admin Fruit Management Page (/admin/fruits)

### 기능 요구사항
- 과일 템플릿 CRUD
- 미션 템플릿 CRUD
- 이미지 업로드 및 관리
- 템플릿 활성화/비활성화

### UI 컴포넌트
```
AdminFruitPage
├── TemplateManagement
│   ├── FruitTemplates
│   │   ├── TemplateList
│   │   │   └── TemplateCard[]
│   │   │       ├── PreviewImages
│   │   │       ├── TemplateName
│   │   │       ├── TemplateType
│   │   │       ├── EditButton
│   │   │       └── DeleteButton
│   │   └── AddTemplateButton
│   └── MissionTemplates
│       ├── MissionList
│       │   └── MissionCard[]
│       │       ├── MissionName
│       │       ├── MissionContent
│       │       ├── MissionType
│       │       ├── EditButton
│       │       └── DeleteButton
│       └── AddMissionButton
├── TemplateForm (Modal)
│   ├── BasicInfo
│   │   ├── NameInput
│   │   └── TypeSelector
│   ├── ImageUpload (과일 템플릿용)
│   │   ├── SeedImageUpload
│   │   ├── GerminationImageUpload
│   │   ├── SeedlingImageUpload
│   │   ├── JuvenileImageUpload
│   │   ├── VegetativeImageUpload
│   │   ├── ReproductiveImageUpload
│   │   └── FruitingImageUpload
│   ├── ContentEditor (미션 템플릿용)
│   └── ActionButtons
│       ├── SaveButton
│       └── CancelButton
└── DeleteConfirmModal
```

### API 호출
```javascript
// 과일 템플릿 관리
POST /api/fruit-templates
PUT /api/fruit-templates/{id}
DELETE /api/fruit-templates/{id}
GET /api/fruit-templates

// 미션 템플릿 관리
POST /api/mission-templates
PUT /api/mission-templates/{id}
DELETE /api/mission-templates/{id}
GET /api/mission-templates
```

---

## 6. 공통 컴포넌트

### Layout
```
AppLayout
├── Header
│   ├── Logo
│   ├── Navigation
│   │   ├── HomeLink
│   │   ├── FruitsLink
│   │   └── AdminLink (role === 'admin')
│   └── UserMenu
│       ├── UserName
│       └── LogoutButton
└── Main
    └── {children}
```

### Auth Guard
```javascript
// 인증이 필요한 페이지 보호
function AuthGuard({ children, requiredRole }) {
  const token = localStorage.getItem('token');
  const user = decodeToken(token);

  if (!token || !user) {
    return <Redirect to="/login" />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Redirect to="/" />;
  }

  return children;
}
```

### Error Handling
```javascript
// API 에러 처리
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 토큰 만료
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    if (error.response?.status === 403) {
      // 권한 없음
      showError('권한이 없습니다');
    }
    return Promise.reject(error);
  }
);
```

---

## 7. 상태 관리 (Context/Redux)

### Global State
```javascript
{
  auth: {
    isAuthenticated: boolean,
    user: {
      id: number,
      name: string,
      cell: string,
      role: string
    },
    token: string
  },
  session: {
    current: {
      id: number,
      fruit_id: number,
      mission_ids: array,
      status: string
    },
    loading: boolean,
    error: string
  },
  fruits: {
    templates: array,
    completed: array,
    loading: boolean,
    error: string
  },
  missions: {
    templates: array,
    today: object,
    history: array,
    loading: boolean,
    error: string
  }
}
```

---

## 8. 라우팅 구조

```javascript
const routes = [
  { path: "/login", component: LoginPage, public: true },
  { path: "/", component: HomePage, requiredAuth: true },
  { path: "/fruits", component: FruitPage, requiredAuth: true },
  { path: "/admin", component: AdminDashboard, requiredRole: "admin" },
  { path: "/admin/fruits", component: AdminFruitPage, requiredRole: "admin" }
];
```

---

## 9. 환경 설정

### 환경 변수
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_IMAGE_BASE_URL=http://localhost:8000/images
```

### 빌드 설정
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```