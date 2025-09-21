# 🚀 Scripts 사용법

## 서버 실행 스크립트

### 1. 통합 애플리케이션 시작 (API + Web, 포트 8000)
```bash
./scripts/start.sh
```

### 2. 데이터 설정
```bash
./scripts/setup_data.sh
```

### 3. 데이터베이스 초기화 (선택사항)
```bash
./scripts/reset_db.sh
```

## 사용 순서

1. **데이터 설정**: `./scripts/setup_data.sh`
2. **애플리케이션 시작**: `./scripts/start.sh`
3. **브라우저에서 접속**: `http://localhost:8000`

## 데이터베이스 관리

### 초기화 (데이터 삭제)
```bash
./scripts/reset_db.sh
```
- 기존 데이터를 백업하고 완전히 초기화
- 백업 파일은 `database/db_backup_YYYYMMDD_HHMMSS.json` 형식으로 저장

## 데이터베이스

- **프로덕션**: `database/db.json` (일반 사용)
- **테스트**: `database/test_db.json` (자동 테스트용)

애플리케이션은 기본적으로 프로덕션 모드로 실행되며, 테스트는 별도의 test_db.json을 사용합니다.

## 설정된 데이터

- **관리자**: 관리자 / 관리자
- **과일 템플릿**: 포도 (7단계 성장)
- **미션 템플릿**: 성경 1장 읽기

## API 엔드포인트

모든 API 엔드포인트는 `/api` 접두사를 사용합니다:
- API 문서: `http://localhost:8000/docs`
- 웹 인터페이스: `http://localhost:8000`

## 성광교회 청년부 말씀 Tree 시스템

매일 성경을 읽고 포도나무가 자라는 과정을 시각화하여 동기부여를 제공하는 시스템입니다.