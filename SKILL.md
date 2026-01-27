---
name: threads-post
description: |
  Meta Threads API를 사용하여 포스트를 작성하고 게시.
  "쓰레드 작성", "쓰레드 포스트", "threads 작성", "threads 게시", "쓰레드에 올려",
  "쓰레드로 공유", "기술 공유 쓰레드", "홍보 쓰레드", "세션 정리 쓰레드", "교육 콘텐츠 쓰레드",
  "쓰레드 댓글", "쓰레드 답글", "threads reply", "threads comment",
  "threads post", "SNS 게시" 요청 시 사용.
---

# Threads Post Writer

Meta Threads API를 통해 텍스트/이미지/캐러셀 포스트를 작성하고 게시합니다. 댓글/대댓글(최대 3단계)도 지원합니다.

## 워크플로우

```
1. 환경 확인 → 2. 콘텐츠 유형 결정 → 3. 포스트 작성 → 4. 검토 → 5. 게시
```

## 1. 환경 설정 확인

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export THREADS_ACCESS_TOKEN="your-long-lived-access-token"
export THREADS_USER_ID="your-threads-user-id"  # 선택: 미설정 시 API로 자동 조회
```

**Access Token 발급 방법:**
1. [Meta Developer Portal](https://developers.facebook.com/)에서 Business 앱 생성
2. Threads 제품 추가, `threads_basic` + `threads_content_publish` 스코프 설정
3. OAuth 인증 후 단기 토큰 → 장기 토큰으로 교환

## 2. 콘텐츠 유형 결정

| 유형 | 조건 | 비고 |
|------|------|------|
| TEXT | 텍스트만 | 가장 단순 |
| IMAGE | 텍스트 + 이미지 1개 | 공개 URL 필요, 최대 8MB |
| CAROUSEL | 텍스트 + 이미지 2-20개 | 각각 공개 URL 필요 |

링크는 텍스트 본문에 직접 포함하면 자동 프리뷰가 생성됩니다.

## 3. 포스트 작성

### 제약 사항

- **500자** 제한
- 해시태그 **1개**만 허용
- 24시간 내 최대 **250개** 게시 가능
- 이미지는 **공개 URL**이어야 함
- 댓글 깊이 **최대 3단계** (포스트 → 댓글 → 대댓글 → 대대댓글)

### 용도별 포스트 작성

포스트 템플릿은 [references/post-templates.md](references/post-templates.md) 참조.

**기술 콘텐츠**: TIL, 기술 팁, 도구 추천 등. 핵심 발견을 1-2문장으로 전달.

**작업 세션 정리**: 오늘 한 일, 주요 변경, 해결한 문제를 bullet으로 정리.

**기업/브랜드 홍보**: 제품 소개, 업데이트 발표, 이벤트 안내, 고객 사례 공유. CTA 포함.

**교육 콘텐츠 소개**: 강의/코스 소개, 워크숍/세미나 안내, 학습 자료 추천, 로드맵 공유, 수강생 후기.

**일반 포스트**: 의견 공유, 링크 공유 등 자유 형식.

### 작성 원칙

1. 500자 내에서 핵심만 전달
2. 첫 줄에 주제/키워드를 명확히
3. 줄바꿈으로 가독성 확보
4. 마지막에 해시태그 1개 배치
5. 홍보 포스트에는 CTA(행동 유도) 포함

## 4. 게시

### 스크립트 사용

```bash
# 텍스트 포스트
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "포스트 내용"

# 이미지 포스트
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "포스트 내용" \
  --image-url "https://example.com/image.jpg"

# 캐러셀 포스트 (이미지 2-20개)
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "포스트 내용" \
  --carousel-images "https://example.com/1.jpg,https://example.com/2.jpg"

# 댓글 (포스트에 답글)
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "댓글 내용" \
  --reply-to "대상_포스트_미디어_ID"

# 대댓글 (댓글에 답글, 최대 3단계)
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "대댓글 내용" \
  --reply-to "대상_댓글_미디어_ID"

# 이미지 포함 댓글
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "이미지와 함께 답글" \
  --image-url "https://example.com/image.jpg" \
  --reply-to "대상_미디어_ID"

# 드라이런 (게시 없이 페이로드 확인)
python3 ~/.claude/skills/threads-post/scripts/publish_thread.py \
  --text "테스트" --dry-run
```

### 옵션

| 옵션 | 설명 | 필수 |
|------|------|------|
| `--text` | 포스트 텍스트 (max 500자) | O |
| `--image-url` | 이미지 공개 URL | X |
| `--carousel-images` | 캐러셀 이미지 URL (쉼표 구분) | X |
| `--reply-to` | 답글 대상 미디어 ID (최대 3단계) | X |
| `--dry-run` | 게시하지 않고 페이로드만 출력 | X |

## 5. 실행 절차

1. 환경변수 `THREADS_ACCESS_TOKEN` 확인
2. 사용자 요청 분석: 용도(기술/홍보/일반), 콘텐츠 유형(TEXT/IMAGE/CAROUSEL)
3. [references/post-templates.md](references/post-templates.md) 참조하여 포스트 초안 작성
4. 500자 이내인지, 해시태그 1개인지 검증
5. 사용자에게 초안 확인 요청
6. 확인 후 `publish_thread.py` 스크립트로 게시
7. 결과(post_id) 전달
