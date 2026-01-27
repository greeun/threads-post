# threads-post

Meta Threads API를 활용한 Claude Code 스킬. 자연어 명령으로 Threads 포스트 작성, 이미지/캐러셀 게시, 댓글/대댓글을 처리합니다.

## 기능

- **TEXT** — 텍스트 포스트
- **IMAGE** — 텍스트 + 이미지 1개 (공개 URL, max 8MB)
- **CAROUSEL** — 텍스트 + 이미지 2~20개
- **댓글/대댓글** — `reply_to_id`로 최대 3단계 깊이

## 구조

```
threads-post/
├── SKILL.md                    # 스킬 정의 (워크플로우, 제약사항)
├── scripts/
│   └── publish_thread.py       # Threads API 게시 스크립트
└── references/
    └── post-templates.md       # 용도별 포스트 템플릿
```

## 사전 준비

### 1. Meta Developer Portal 설정

1. [Meta Developer Portal](https://developers.facebook.com/)에서 Business 앱 생성
2. Threads 제품 추가
3. 스코프: `threads_basic`, `threads_content_publish`
4. OAuth 인증 → 단기 토큰 → 장기 토큰 교환

### 2. 환경변수

```bash
export THREADS_ACCESS_TOKEN="your-long-lived-access-token"
export THREADS_USER_ID="your-threads-user-id"  # 선택
```

### 3. Claude Code에 스킬 등록

```bash
ln -s /path/to/threads-post ~/.claude/skills/threads-post
```

## 사용법

### Claude Code에서 자연어로 사용

```
# 기술 콘텐츠
오늘 Python match 문 배운 거 쓰레드에 올려줘

# 브랜드 홍보
WithWiz v2.0 업데이트 발표 쓰레드 써줘

# 교육 콘텐츠
FastAPI 강의 소개 쓰레드 포스트 써줘

# 댓글
포스트 18050206876707110에 댓글 달아줘

# 대댓글
댓글 18099887766554433에 대댓글 달아줘
```

### 스크립트 직접 실행

```bash
# 텍스트 포스트
python3 scripts/publish_thread.py --text "포스트 내용"

# 이미지 포스트
python3 scripts/publish_thread.py --text "내용" --image-url "https://example.com/img.jpg"

# 캐러셀 포스트
python3 scripts/publish_thread.py --text "내용" \
  --carousel-images "https://example.com/1.jpg,https://example.com/2.jpg"

# 댓글
python3 scripts/publish_thread.py --text "댓글" --reply-to "미디어ID"

# 드라이런
python3 scripts/publish_thread.py --text "테스트" --dry-run
```

### 옵션

| 옵션 | 설명 | 필수 |
|------|------|------|
| `--text` | 포스트 텍스트 (max 500자) | O |
| `--image-url` | 이미지 공개 URL | X |
| `--carousel-images` | 캐러셀 이미지 URL (쉼표 구분) | X |
| `--reply-to` | 답글 대상 미디어 ID | X |
| `--dry-run` | 게시 없이 페이로드 확인 | X |

## 용도별 템플릿

| 용도 | 템플릿 |
|------|--------|
| 기술 콘텐츠 | TIL, 기술 팁, 도구 추천 |
| 작업 세션 정리 | 개발 로그, 문제 해결 기록 |
| 기업/브랜드 홍보 | 제품 소개, 업데이트 발표, 이벤트, 고객 사례 |
| 교육 콘텐츠 | 강의 소개, 워크숍 안내, 로드맵, 수강생 후기 |
| 일반 | 의견 공유, 링크 공유 |

상세 템플릿은 `references/post-templates.md` 참조.

## API 제약사항

- 500자 제한
- 해시태그 1개
- 24시간 내 250개 게시
- 이미지 공개 URL 필요 (max 8MB)
- 캐러셀 2~20개 이미지
- 댓글 깊이 최대 3단계
- 링크 5개 초과 시 게시 실패

## 의존성

Python 3 표준 라이브러리만 사용. 별도 패키지 설치 불필요.

## 라이선스

MIT
