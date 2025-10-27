# Fonts for Mission Report

## 포함된 폰트

### BMHANNAPro (배민 한나Pro)
- **파일**: `BMHANNAProOTF.otf`
- **특징**: 깔끔하고 모던한 스타일, 가독성 우수
- **용도**: 감사일기 본문 텍스트
- **라이선스**: 무료 (개인 및 기업 사용 가능)
- **출처**: https://www.woowahan.com/fonts

## 사용 방법

이 폰트는 프로젝트에 포함되어 있어 별도 설치 없이 사용 가능합니다.

코드는 다음 순서로 폰트를 찾습니다:
1. `BMHANNAProOTF.otf` (프로젝트 폰트)
2. 시스템 폰트 (fallback)

## 다른 폰트 사용하기

다른 폰트를 사용하려면:
1. `.ttf` 또는 `.otf` 파일을 이 디렉토리에 추가
2. `write_daily_mission_report.py`의 `_get_font_paths()` 함수에서 폰트 경로 수정
