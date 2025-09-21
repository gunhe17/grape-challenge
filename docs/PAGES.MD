# PAGES.MD - Mobile-First Frontend Page Design Specification

## Technology Stack
- **Backend**: FastAPI
- **Template Engine**: Jinja2
- **Frontend**: HTML
- **Styling**: Tailwind CSS (Mobile-First Responsive)
- **Data**: JSON Database
- **Primary Target**: Mobile Devices (iOS/Android)

---

## Page Structure Overview

```
webapp/
├── templates/
│   ├── base.html           # Base template with Tailwind CDN
│   ├── login.html          # Login page
│   ├── home.html           # Main home page
│   ├── fruits.html         # Fruit gallery page
│   └── admin.html          # Admin dashboard
├── static/
│   └── images/
│       ├── fruits/         # Fruit status images
│       └── icons/          # UI icons
└── server.py               # FastAPI app with template routes
```

---

## 1. Login Page (`/login`) - Mobile-First

### Template: `templates/login.html`
```html
<!-- extends base.html -->
<div class="min-h-screen flex flex-col justify-center bg-green-50 px-4 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <!-- Logo/Title Section -->
    <div class="text-center mb-8">
      <div class="text-4xl mb-4">🌳</div>
      <h2 class="text-3xl font-bold text-green-700 mb-2">
        말씀 Tree
      </h2>
      <p class="text-green-600 text-sm">성광교회 청년부</p>
    </div>

    <!-- Login Form -->
    <div class="bg-white py-8 px-6 shadow-lg rounded-2xl border border-green-100">
      <form action="/login" method="POST" class="space-y-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">이름</label>
          <input type="text" name="name" required
                 class="block w-full px-4 py-4 text-lg border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500"
                 placeholder="홍길동">
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">소속</label>
          <input type="text" name="cell" required
                 class="block w-full px-4 py-4 text-lg border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500"
                 placeholder="1청년부">
        </div>

        <!-- Large touch-friendly button -->
        <button type="submit"
                class="w-full bg-green-600 text-white py-4 px-6 text-lg font-semibold rounded-xl hover:bg-green-700 active:bg-green-800 transition-colors shadow-md">
          로그인
        </button>
      </form>
    </div>

    <!-- Help text -->
    <p class="mt-6 text-center text-xs text-gray-500">
      소속은 "1청년부" 또는 "2청년부"로 입력해주세요
    </p>
  </div>
</div>
```

### FastAPI Route:
```python
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, name: str = Form(...), cell: str = Form(...)):
    # Login logic using usecases.user.login_user()
    # Set JWT token in cookie, redirect to /home
```

---

## 2. Home Page (`/home`) - Mobile-Optimized

### Template: `templates/home.html`
```html
<!-- extends base.html -->
<div class="min-h-screen bg-gray-50 pb-20">
  <!-- Mobile Header -->
  <header class="bg-white shadow-sm border-b sticky top-0 z-10">
    <div class="px-4 py-3 flex justify-between items-center">
      <div class="flex items-center space-x-3">
        <div class="text-2xl">🌳</div>
        <h1 class="text-lg font-bold text-green-700">말씀 Tree</h1>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-600">{{ user.name }}님</span>
        <button class="text-gray-400 p-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
        </button>
      </div>
    </div>
  </header>

  <div class="px-4 py-4 space-y-4">

    <!-- Current Fruit Progress - Mobile Card -->
    <div class="bg-white rounded-2xl shadow-sm p-5 border border-gray-100">
      <h2 class="text-base font-semibold mb-4 text-gray-800">🌱 현재 과일 성장</h2>

      {% if current_fruit %}
      <div class="text-center mb-4">
        <!-- Large fruit image for mobile with emoji fallback -->
        <div class="w-28 h-28 mx-auto mb-3 fruit-grow flex items-center justify-center">
          <img src="/static/images/fruits/{{ current_fruit.template.name }}_{{ current_fruit.status }}.png"
               alt="{{ current_fruit.template.name }}"
               class="w-full h-full object-contain"
               onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
          <div class="text-6xl hidden items-center justify-center w-full h-full">
            {% if current_fruit.template.name == '사과' %}🍎
            {% elif current_fruit.template.name == '바나나' %}🍌
            {% elif current_fruit.template.name == '포도' %}🍇
            {% elif current_fruit.template.name == '오렌지' %}🍊
            {% elif current_fruit.template.name == '딸기' %}🍓
            {% elif current_fruit.template.name == '복숭아' %}🍑
            {% elif current_fruit.template.name == '수박' %}🍉
            {% elif current_fruit.template.name == '파인애플' %}🍍
            {% elif current_fruit.template.name == '키위' %}🥝
            {% elif current_fruit.template.name == '망고' %}🥭
            {% elif current_fruit.template.name == '레몬' %}🍋
            {% elif current_fruit.template.name == '체리' %}🍒
            {% elif current_fruit.template.name == '자두' %}🫐
            {% elif current_fruit.template.name == '블루베리' %}🫐
            {% else %}🍎{% endif %}
          </div>
        </div>

        <h3 class="font-semibold text-lg text-gray-800">{{ current_fruit.template.name }}</h3>
      </div>

      <!-- Progress bar -->
      <div class="mb-3">
        <div class="flex justify-between text-xs text-gray-500 mb-1">
          <span>진행도</span>
          <span>{{ mission_count }}/7</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div class="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all duration-500"
               style="width: {{ (mission_count / 7 * 100) }}%"></div>
        </div>
      </div>

      <!-- Progress dots -->
      <div class="flex justify-center space-x-2">
        {% for i in range(1, 8) %}
        <div class="w-2 h-2 rounded-full {% if i <= mission_count %}bg-green-500{% else %}bg-gray-300{% endif %}"></div>
        {% endfor %}
      </div>
      {% else %}
      <div class="text-center py-6">
        <div class="text-4xl mb-3">🌱</div>
        <p class="text-gray-500 text-sm">미션을 완료하면 과일이 시작됩니다</p>
      </div>
      {% endif %}
    </div>

    <!-- Today's Mission - Mobile Card -->
    <div class="bg-white rounded-2xl shadow-sm p-5 border border-gray-100">
      <h2 class="text-base font-semibold mb-4 text-gray-800 flex items-center">
        <span class="mr-2">📖</span>
        오늘의 미션
      </h2>

      {% if daily_completed %}
      <div class="text-center py-6">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <div class="text-green-500 text-2xl">✓</div>
        </div>
        <p class="text-gray-600 font-medium">오늘 미션을 완료했습니다!</p>
        <p class="text-gray-400 text-sm mt-1">내일 새로운 미션을 만나보세요</p>
      </div>
      {% else %}
      <div class="space-y-4">
        <!-- Mission content -->
        <div class="bg-gradient-to-br from-green-50 to-blue-50 p-4 rounded-xl border border-green-100">
          <h3 class="font-semibold text-green-800 mb-2">{{ today_mission.name }}</h3>
          <p class="text-green-700 text-sm leading-relaxed">{{ today_mission.content }}</p>
        </div>

        <!-- Complete button -->
        <form action="/mission/complete" method="POST">
          <input type="hidden" name="mission_template_id" value="{{ today_mission.id }}">
          <button type="submit"
                  class="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-4 px-6 text-base font-semibold rounded-xl hover:from-green-600 hover:to-green-700 active:scale-95 transition-all shadow-lg">
            ✓ 미션 완료하기
          </button>
        </form>
      </div>
      {% endif %}
    </div>

    <!-- Quick Actions - Mobile Grid -->
    <div class="grid grid-cols-2 gap-3">
      <a href="/fruits"
         class="bg-gradient-to-br from-orange-100 to-red-100 p-4 rounded-xl text-center active:scale-95 transition-transform border border-orange-200">
        <div class="text-orange-600 text-2xl mb-2">🍎</div>
        <span class="text-orange-800 font-semibold text-sm">내 과일들</span>
      </a>

      {% if user.role == 'admin' %}
      <a href="/admin"
         class="bg-gradient-to-br from-blue-100 to-indigo-100 p-4 rounded-xl text-center active:scale-95 transition-transform border border-blue-200">
        <div class="text-blue-600 text-2xl mb-2">⚙️</div>
        <span class="text-blue-800 font-semibold text-sm">관리자</span>
      </a>
      {% else %}
      <a href="/history"
         class="bg-gradient-to-br from-purple-100 to-pink-100 p-4 rounded-xl text-center active:scale-95 transition-transform border border-purple-200">
        <div class="text-purple-600 text-2xl mb-2">📊</div>
        <span class="text-purple-800 font-semibold text-sm">내 기록</span>
      </a>
      {% endif %}
    </div>
  </div>
</div>
```

### FastAPI Route:
```python
@app.get("/home")
async def home_page(request: Request):
    # Get user from JWT token
    # Load current session, today's mission, fruit status
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "current_fruit": fruit,
        "mission_count": len(session.mission_ids),
        "today_mission": mission_template,
        "daily_completed": is_daily_completed
    })

@app.post("/mission/complete")
async def complete_mission(request: Request, mission_template_id: int = Form(...)):
    # Use usecases.mission_workflow.complete_mission_workflow()
    # Redirect to /home with success message
```

---

## 3. Fruits Page (`/fruits`) - Green Nature Theme

### Template: `templates/fruits.html`
```html
<!-- extends base.html -->
<div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
  <!-- Mobile Header -->
  <header class="bg-white/90 backdrop-blur-sm shadow-sm border-b border-green-100 sticky top-0 z-10">
    <div class="px-4 py-3 flex justify-between items-center">
      <a href="/home" class="flex items-center text-green-600 hover:text-green-700 active:scale-95 transition-all">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        <span class="font-medium">홈으로</span>
      </a>
      <h1 class="text-lg font-bold text-green-700 flex items-center">
        <span class="mr-2">🍎</span>
        내 과일들
      </h1>
      <div class="w-16"></div>
    </div>
  </header>

  <div class="px-4 py-4">
    {% if completed_fruits %}
    <!-- Fruit Count Header -->
    <div class="mb-6 text-center">
      <div class="inline-flex items-center bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-green-200">
        <span class="text-2xl mr-2">🌳</span>
        <span class="text-green-700 font-semibold">{{ completed_fruits|length }}개의 열매를 수확했어요!</span>
      </div>
    </div>

    <!-- Fruits Grid -->
    <div class="grid grid-cols-2 gap-4 mb-6">
      {% for fruit in completed_fruits %}
      <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-sm p-4 text-center border border-green-100 hover:shadow-md transition-all active:scale-95">
        <!-- Fruit Image with emoji fallback and glow effect -->
        <div class="relative mb-3">
          <div class="w-20 h-20 mx-auto fruit-grow flex items-center justify-center">
            <img src="/static/images/fruits/{{ fruit.template.name }}_seventh.png"
                 alt="{{ fruit.template.name }}"
                 class="w-full h-full object-contain"
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <div class="text-4xl hidden items-center justify-center w-full h-full">
              {% if fruit.template.name == '사과' %}🍎
              {% elif fruit.template.name == '바나나' %}🍌
              {% elif fruit.template.name == '포도' %}🍇
              {% elif fruit.template.name == '오렌지' %}🍊
              {% elif fruit.template.name == '딸기' %}🍓
              {% elif fruit.template.name == '복숭아' %}🍑
              {% elif fruit.template.name == '수박' %}🍉
              {% elif fruit.template.name == '파인애플' %}🍍
              {% elif fruit.template.name == '키위' %}🥝
              {% elif fruit.template.name == '망고' %}🥭
              {% elif fruit.template.name == '레몬' %}🍋
              {% elif fruit.template.name == '체리' %}🍒
              {% elif fruit.template.name == '자두' %}🫐
              {% elif fruit.template.name == '블루베리' %}🫐
              {% else %}🍎{% endif %}
            </div>
          </div>
          {% if fruit.template.type == 'special' %}
          <div class="absolute -top-1 -right-1 w-6 h-6 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center">
            <span class="text-white text-xs">✨</span>
          </div>
          {% endif %}
        </div>

        <!-- Fruit Info -->
        <h3 class="font-semibold text-green-800 mb-1">{{ fruit.template.name }}</h3>
        <p class="text-xs text-green-600 mb-2">{{ fruit.completed_date }}</p>

        {% if fruit.template.type == 'special' %}
        <span class="inline-block bg-gradient-to-r from-yellow-100 to-orange-100 text-orange-700 text-xs px-2 py-1 rounded-full border border-orange-200">
          ✨ 특별한 과일
        </span>
        {% else %}
        <span class="inline-block bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full border border-green-200">
          🌱 일반 과일
        </span>
        {% endif %}
      </div>
      {% endfor %}
    </div>

    <!-- Growth Stats -->
    <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-5 border border-green-100 mb-4">
      <h3 class="font-semibold text-green-800 mb-3 flex items-center">
        <span class="mr-2">📊</span>
        나의 성장 기록
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">{{ completed_fruits|length }}</div>
          <div class="text-xs text-green-500">완성된 과일</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">{{ (completed_fruits|length * 7) }}</div>
          <div class="text-xs text-green-500">완료한 미션</div>
        </div>
      </div>
    </div>

    {% else %}
    <!-- Empty State -->
    <div class="text-center py-16">
      <div class="mb-6">
        <div class="w-24 h-24 bg-gradient-to-br from-green-100 to-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4 border-4 border-green-200">
          <span class="text-4xl">🌱</span>
        </div>
      </div>

      <h3 class="text-lg font-semibold text-green-700 mb-2">첫 번째 과일을 키워보세요!</h3>
      <p class="text-green-600 text-sm mb-6 leading-relaxed">
        매일 미션을 완료하면<br>
        아름다운 과일을 수확할 수 있어요
      </p>

      <a href="/home"
         class="inline-flex items-center bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-green-600 hover:to-emerald-600 active:scale-95 transition-all shadow-lg">
        <span class="mr-2">🌱</span>
        미션 시작하기
      </a>
    </div>
    {% endif %}
  </div>
</div>
```

### FastAPI Route:
```python
@app.get("/fruits")
async def fruits_page(request: Request):
    # Get user from JWT token
    # Load completed sessions with fruits
    return templates.TemplateResponse("fruits.html", {
        "request": request,
        "completed_fruits": fruits_with_dates
    })
```

---

## 4. Admin Dashboard (`/admin`)

### Template: `templates/admin.html`
```html
<!-- extends base.html -->
<div class="min-h-screen bg-gray-50">
  <header class="bg-white shadow-sm border-b">
    <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
      <a href="/home" class="text-green-600 hover:text-green-700">← 홈으로</a>
      <h1 class="text-xl font-bold text-green-700">관리자 대시보드</h1>
      <div></div>
    </div>
  </header>

  <div class="max-w-6xl mx-auto px-4 py-6 space-y-6">

    <!-- Statistics Overview -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <div class="text-3xl font-bold text-blue-600">{{ stats.total_users }}</div>
        <p class="text-gray-600">총 사용자</p>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <div class="text-3xl font-bold text-green-600">{{ stats.active_users }}</div>
        <p class="text-gray-600">활성 사용자</p>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6 text-center">
        <div class="text-3xl font-bold text-orange-600">{{ stats.completion_rate }}%</div>
        <p class="text-gray-600">완료율</p>
      </div>
    </div>

    <!-- User Statistics Table -->
    <div class="bg-white rounded-lg shadow-md">
      <div class="px-6 py-4 border-b">
        <h2 class="text-lg font-semibold">사용자 통계</h2>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">이름</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">소속</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">역할</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">총 세션</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">완료 세션</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            {% for user in stats.users %}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ user.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.cell }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="{% if user.role == 'admin' %}bg-blue-100 text-blue-800{% else %}bg-gray-100 text-gray-800{% endif %} px-2 py-1 rounded-full text-xs">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.statistics.total_sessions }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.statistics.completed_sessions }}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
```

### FastAPI Route:
```python
@app.get("/admin")
async def admin_page(request: Request):
    # Verify admin role from JWT token
    # Load admin statistics
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "stats": admin_statistics
    })
```

---

## 5. Base Template (`templates/base.html`) - Green Nature Theme

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="theme-color" content="#10b981">
    <title>{% block title %}성광교회 말씀 Tree{% endblock %}</title>

    <!-- Tailwind CSS with custom green theme -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'nature': {
                            50: '#f0fdf4',
                            100: '#dcfce7',
                            200: '#bbf7d0',
                            300: '#86efac',
                            400: '#4ade80',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                            800: '#166534',
                            900: '#14532d',
                        },
                        'leaf': {
                            50: '#ecfdf5',
                            100: '#d1fae5',
                            200: '#a7f3d0',
                            300: '#6ee7b7',
                            400: '#34d399',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                            800: '#065f46',
                            900: '#064e3b',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        /* Custom green nature theme styles */
        .fruit-grow {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .fruit-grow:hover {
            transform: scale(1.08);
            filter: brightness(1.1);
        }

        /* Green gradient backgrounds */
        .bg-nature-gradient {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 50%, #a7f3d0 100%);
        }

        /* Custom scrollbar for mobile */
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: #f0fdf4;
        }
        ::-webkit-scrollbar-thumb {
            background: #22c55e;
            border-radius: 2px;
        }

        /* Prevent text selection on mobile */
        .no-select {
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        /* Loading animation for buttons */
        .btn-loading {
            position: relative;
            color: transparent;
        }
        .btn-loading::after {
            content: "";
            position: absolute;
            width: 16px;
            height: 16px;
            top: 50%;
            left: 50%;
            margin-left: -8px;
            margin-top: -8px;
            border: 2px solid #ffffff;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Pulse animation for new features */
        @keyframes pulse-green {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .pulse-green {
            animation: pulse-green 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
    </style>
</head>
<body class="bg-nature-gradient min-h-screen">
    {% block content %}{% endblock %}

    <!-- Toast Notifications with Green Theme -->
    {% if messages %}
    <div class="fixed top-4 left-4 right-4 space-y-2 z-50">
        {% for message in messages %}
        <div class="{% if message.type == 'success' %}bg-green-50 border-l-4 border-green-400 text-green-700{% else %}bg-red-50 border-l-4 border-red-400 text-red-700{% endif %} p-4 rounded-r-lg shadow-lg backdrop-blur-sm animate-slide-down">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    {% if message.type == 'success' %}
                    <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                    {% else %}
                    <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                    </svg>
                    {% endif %}
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium">{{ message.text }}</p>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- JavaScript for Mobile Interactions -->
    <script>
        // Add loading states to form submissions
        document.addEventListener('DOMContentLoaded', function() {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        submitBtn.classList.add('btn-loading');
                        submitBtn.disabled = true;
                    }
                });
            });

            // Auto-hide toast messages
            const messages = document.querySelectorAll('[class*="animate-slide-down"]');
            messages.forEach(message => {
                setTimeout(() => {
                    message.style.opacity = '0';
                    message.style.transform = 'translateY(-20px)';
                    setTimeout(() => message.remove(), 300);
                }, 3000);
            });

            // Add touch feedback for interactive elements
            const interactiveElements = document.querySelectorAll('button, a, [role="button"]');
            interactiveElements.forEach(element => {
                element.addEventListener('touchstart', function() {
                    this.style.transform = 'scale(0.95)';
                });
                element.addEventListener('touchend', function() {
                    this.style.transform = '';
                });
            });
        });
    </script>
</body>
</html>
```

---

## 6. FastAPI Integration with Emoji Fallback

### Helper Function for Fruit Images:
```python
def get_fruit_emoji(fruit_name: str) -> str:
    """Get emoji representation for fruit names"""
    fruit_emojis = {
        '사과': '🍎',
        '바나나': '🍌',
        '포도': '🍇',
        '오렌지': '🍊',
        '딸기': '🍓',
        '복숭아': '🍑',
        '수박': '🍉',
        '파인애플': '🍍',
        '키위': '🥝',
        '망고': '🥭',
        '레몬': '🍋',
        '체리': '🍒',
        '자두': '🫐',
        '블루베리': '🫐'
    }
    return fruit_emojis.get(fruit_name, '🍎')  # Default to apple

def get_fruit_display_data(fruit_template, status='seventh'):
    """Prepare fruit data for template rendering with image fallback"""
    return {
        'name': fruit_template['name'],
        'emoji': get_fruit_emoji(fruit_template['name']),
        'image_path': f"/static/images/fruits/{fruit_template['name']}_{status}.png",
        'type': fruit_template.get('type', 'normal')
    }
```

### Main Server Routes:
```python
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import jwt
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Custom template filter for emoji fallback
@app.on_event("startup")
async def setup_template_filters():
    templates.env.globals["get_fruit_emoji"] = get_fruit_emoji
    templates.env.globals["file_exists"] = lambda path: os.path.exists(f"static{path}")

# Authentication middleware for protected routes
async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Verify JWT and return user info

# Enhanced route handlers with emoji fallback support
@app.get("/home")
async def home_page(request: Request, user = Depends(get_current_user)):
    # Get current fruit with emoji fallback
    current_fruit = None
    if session and session.get('fruit_id'):
        fruit_data = get_fruit_with_template(session['fruit_id'])
        if fruit_data:
            current_fruit = {
                'template': get_fruit_display_data(fruit_data['template'], fruit_data['status']),
                'status': fruit_data['status']
            }

    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "current_fruit": current_fruit,
        "mission_count": len(session.mission_ids) if session else 0,
        "today_mission": mission_template,
        "daily_completed": is_daily_completed
    })

@app.get("/fruits")
async def fruits_page(request: Request, user = Depends(get_current_user)):
    completed_fruits = []
    for fruit in get_completed_fruits(user['id']):
        completed_fruits.append({
            'template': get_fruit_display_data(fruit['template']),
            'completed_date': fruit['completed_date'],
            'type': fruit['template']['type']
        })

    return templates.TemplateResponse("fruits.html", {
        "request": request,
        "completed_fruits": completed_fruits
    })
```

---

## Key Mobile-First Features Implementation

### 1. **Green Nature Theme Design**
- 🌿 **Color Palette**: Nature-inspired green gradients (emerald, leaf, teal)
- 🎨 **Visual Elements**: Plant emojis, gradient backgrounds, soft shadows
- ✨ **Animations**: Fruit growth effects, button touch feedback, pulse animations
- 🌱 **Typography**: Clean, readable fonts with green color scheme

### 2. **Mobile-Optimized UX**
- 📱 **Touch-Friendly**: Large buttons (py-4), proper spacing, 44px+ touch targets
- 🔄 **Responsive Grid**: 2-column mobile grid, adapts to screen size
- 📏 **Safe Areas**: Proper padding (px-4), sticky headers, bottom spacing (pb-20)
- 🎯 **Active States**: `active:scale-95` for immediate touch feedback

### 3. **Green-Themed Mission Flow**
- 🌱 **Progress Visualization**: Green gradient progress bars, dot indicators
- 🍎 **Fruit Growth**: Large centered images (w-28 h-28), growth animations
- ✅ **Completion States**: Green success icons, nature-themed messaging
- 📊 **Statistics**: Green-colored metrics with plant icons

### 4. **Mobile Performance & Accessibility**
- ⚡ **Loading States**: Button loading animations with spinners
- 🎨 **Backdrop Blur**: Modern glass-morphism effect (`backdrop-blur-sm`)
- 📳 **Touch Optimization**: Prevents text selection, proper tap highlights
- 🔔 **Toast Notifications**: Auto-hide messages with green theme

### 5. **Progressive Web App Features**
- 📱 **Mobile Meta Tags**: `apple-mobile-web-app-capable`, proper viewport
- 🎨 **Theme Color**: Green theme color for status bar (`#10b981`)
- 📏 **No Zoom**: `user-scalable=no` for app-like experience
- 🌟 **Smooth Animations**: CSS transitions with cubic-bezier easing

### 6. **Green Nature Branding Elements**
- 🌳 **Logo**: Tree emoji as brand icon throughout app
- 🍎 **Section Icons**: Fruit, plant, and nature emojis for navigation
- 🌿 **Gradient Backgrounds**: Subtle green gradients create depth
- ✨ **Special Effects**: Glow effects for special fruits, pulse animations

This mobile-first design creates an **immersive green nature experience** that feels like a native mobile app while implementing **only the essential features** from DOCS.MD using **clean, simple code**.