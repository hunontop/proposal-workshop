# 실습 자료 배포 페이지 생성 (GitHub Pages용 index.html)
# 전례 = _검정제출/배포/_build.py · 색은 덱 skin.json에서 읽어 톤을 자동 일치시킨다.
import pathlib, html as H, json, re

HERE = pathlib.Path(__file__).parent
# 색은 저장소 안 skin.json에서 읽는다 — 강의 덱 스킨의 사본이고, 갱신은 강의 저장소의
# 동기화 스크립트가 한다. 여기서 바깥 경로를 참조하면 ⑴이 저장소만 clone한 사람은
# 빌드가 안 되고 ⑵경로에 든 현장 정보가 공개된다(연장통 규약 "현장 한정 정보 금지").
C = json.loads((HERE / "skin.json").read_text(encoding="utf-8"))["colors"]


def hx(k):
    return "#" + C[k]


SITE = "https://hunontop.github.io/proposal-workshop/"

# ── 프롬프트 복사 블록 ────────────────────────────────────────────────────
# 연장통 정책(공유뇌 ref/교안/연장통): 담는 것 = "프롬프트 원문(복붙)".
# 짧은 프롬프트를 내려받게 하면 붙여넣기까지 손이 하나 더 든다 →
# **복사 버튼이 1순위, 내려받기는 원문 보관용**(2026-08-27 결정).
# 라벨은 md에서 블록 바로 앞의 ##/### 제목을 주워 쓴다 — 파일을 고치면 따라온다.

# 표준 복사(클립보드) 아이콘 + 성공 체크. 인라인 SVG — 외부 의존 0(연장통 규약).
IC_COPY = ('<svg class="ic ic-c" viewBox="0 0 24 24" width="14" height="14" fill="none" '
           'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/>'
           '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>')
IC_DONE = ('<svg class="ic ic-d" viewBox="0 0 24 24" width="14" height="14" fill="none" '
           'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>')

_FENCE = re.compile(r"\n```[^\n]*\n(.*?)\n```", re.S)
_HEAD = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.M)


def _label(raw, fallback):
    if not raw:
        return fallback
    s = re.sub(r"[`*]", "", raw).strip()
    s = re.sub(r"^\d+\.\s*", "", s)          # "1. 잘 깔렸는지" → "잘 깔렸는지"
    s = re.split(r"\s+—\s+", s)[0].strip()    # "빈 양식 — 복사해서" → "빈 양식"
    return s or fallback


def copy_blocks(rel):
    """md 파일에서 (라벨, 본문) 코드블록을 뽑는다. 없으면 []."""
    f = HERE / rel
    if not f.is_file():
        return []
    md = f.read_text(encoding="utf-8")
    out = []
    for m in _FENCE.finditer(md):
        heads = _HEAD.findall(md[:m.start()])
        out.append((_label(heads[-1] if heads else None, "프롬프트 전체"), m.group(1)))
    return out


# ── 세션별 자료 ────────────────────────────────────────────────────────────
# state: ready = 지금 내려받을 수 있음 / soon = 개설 전 준비 중
# 묶음은 **덱(영상 편성 12편) 순서**를 따른다 — 2026-09-01 변경.
# 종전엔 강의실 2시간 세션(S1~S8)으로 묶었는데, 정본 편성은 이미 「내용으로 자른 12편」이라
# (발표노트 「영상 편성 — 12편」) 목록과 영상이 어긋났다. 이제 편 번호·장 범위로 묶는다.
# 자료가 없는 편은 아예 나타나지 않는다.
SESSIONS = [
    ("사전", "시작하기 전에", [
        ("에이전트 설치 안내 (화면 그대로 따라 하기)", "설치안내.html",
         "이것 하나만 미리 준비하면 됩니다. Claude Code(유료) / Antigravity IDE(무료) 두 갈래 · 스크린샷 안내.", "page"),
    ]),
    ("1편", "왜 이 과정인가 · 1~13장", [
        ("프로필 카드 — 창업 준비자 김하늘", "files/프로필카드_창업준비자_김하늘.md",
         "13장에서 만납니다. 과정 내내 이 사람의 담당자로 실습합니다. 빈칸 5종이 그대로 실습 재료입니다.", "ready"),
    ]),
    ("2편", "AI는 어떻게 답하나 · 14~20장", [
        ("프롬프트 4요소 카드 — 첫 실습", "files/프롬프트_4요소_카드.md",
         "18장. 과정에서 처음 직접 시켜 보는 실습입니다. 같은 요청을 한 줄로 한 번, 4요소로 한 번 — 두 문장을 복사해서 바로 보내고 답을 비교하세요. 맥락·역할·예시·제약 한 장 요약과 빈칸 양식도 함께 있습니다.", "ready"),
    ]),
    ("3편", "공고 조사와 수작업 우회 · 21~24장", [
        # ⚠ 5단계 지도는 2026-09-01 내렸다 — 덱·노트 어디에서도 이 자료를 안내하지 않는다.
        #   파일(files/5단계_지도.md)은 남겨 뒀다. 다시 안내할 자리가 생기면 되살린다.
        ("실습 프롬프트 — 공고 조사", "files/프롬프트_공고조사.md",
         "21·23장. 공고를 찾고 첨부를 열어 보라는 문장 둘(21장), 그리고 사람이 재료를 가져다준 뒤 분석시키는 문장(23장).", "ready"),
    ]),
    ("4편", "스킬과 덱 · 25~27장", [
        ("실습 프롬프트 — 분석을 슬라이드덱으로", "files/프롬프트_분석을_덱으로.md",
         "26장. 같은 분석을 두 번 시킵니다 — 빈칸 지시 없이 한 번, 카드를 주고 빈칸을 지시하고 한 번. 지어낸 칸과 비워 둔 칸이 갈리는 자리입니다.", "ready"),
    ]),
    ("5편", "에이전트 첫걸음 · 28~32장", [
        ("실습 프롬프트 — 에이전트 첫걸음", "files/프롬프트_에이전트_첫걸음.md",
         "30·31·32장. 첫 한마디로 파일 만들기, 작업 폴더 묻기와 자리 옮겨 보기, 일부러 실패시키고 되돌리기. 시킬 문장만 모았습니다.", "ready"),
        ("경로 · 작업 폴더 · 터미널", "files/경로_작업폴더_터미널.md",
         "31장. 무너지는 곳은 코드가 아니라 '그 파일이 어디 갔지'입니다. 개념 셋과 자리 옮기기 실습, 막혔을 때 되묻는 세 문장.", "ready"),
        ("승인 판단 카드", "files/승인판단_카드.md",
         "32장. 승인 창은 여러분의 정지 버튼입니다. 멈출 신호 셋(삭제·전부/전체·설정 변경)과 빨간 글씨를 붙여넣는 법.", "ready"),
    ]),
    ("6편", "설치와 시운전 · 33~38장", [
        ("실습 프롬프트 — 설치와 첫 분류", "files/프롬프트_설치_두도구.md",
         "34~36장. 강의에서 하는 순서 그대로입니다 — 설치 → 확인 → 1건 시운전 → 그 한 건을 카드 기준으로 판정 → 두 번째 도구. 막혔을 때 에러를 돌려주는 한 줄까지.", "ready"),
        # ⏳ 자리만 잡아 둔다 (2026-09-02) — 실습을 촬영한 뒤 그때 나온 결과를 zip으로 올린다.
        #    올릴 때: files/ 에 zip을 넣고 아래 줄의 None → 경로, "soon" → "ready".
        ("수집 결과 묶음 (zip)", None,
         "35장 수집이 오래 걸리거나 막힌 분을 위한 예비입니다. 공고 10건의 목록·상세와 분류 전 상태를 그대로 묶었습니다 — 받아서 풀면 분류부터 이어갈 수 있습니다.", "soon"),
        ("설치 확인 한마디", "files/설치확인_한마디.md",
         "37장. 설치가 끝나면 에이전트에게 '잘 깔렸는지 확인해줘' 한마디로 점검합니다. 막혔을 때 붙여넣는 문장까지 복사해서 쓰면 됩니다.", "ready"),
    ]),
    ("7편", "공정 입구 · 선택과 브리프 · 40~44장", [
        ("실습 프롬프트 — 본격 수집과 선택", "files/프롬프트_조사보고서와_선택.md",
         "42장. 이번엔 고를 만큼 모읍니다 — 10건 수집 · 카드 기준 A/B/C 분류 · 조사보고서 저장, 그리고 고르는 것은 사람이 합니다.", "ready"),
        ("실습 프롬프트 — 브리프 한 장 만들기", "files/프롬프트_브리프_한장.md",
         "43장. 재료는 전부 내 폴더 안에 있습니다 — 23장에서 내려받은 첨부와 프로필 카드.", "ready"),
        ("브리프 예시 — 말벗ON", "files/브리프_예시_말벗ON.md",
         "43장. 공정에 넣는 요구사항 문서가 실제로 어떻게 생겼는지. 없는 값은 비워 둔 형태 그대로입니다.", "ready"),
    ]),
    ("9편", "도식 · 말로 먼저 그린다 · 48~50장", [
        ("도식 5항목 판정표", "files/도식_5항목_판정표.md",
         "48~50장. 도식 후보를 순서·위계·누락·산출물 분리·밀도로 판정하는 표. 세 동사로 묻는 법과 napkin 주의 두 가지도 함께.", "ready"),
    ]),
    ("10편", "디자인과 이미지 프롬프트 · 51~54장", [
        ("배포 프롬프트 ① 기본 — 3병렬 카드", "files/프롬프트_기본_3병렬카드.md",
         "54장 실습 '같은 프롬프트, 스무 개의 그림'에 쓰는 프롬프트. 실제로 채택된 장의 것입니다.", "ready"),
        ("배포 프롬프트 ② 정직 문법 — 검토요망", "files/프롬프트_정직문법_검토요망.md",
         "54장. 근거가 없는 자리를 어떻게 비워 두는지가 프롬프트까지 흘러온 예. 여유가 있을 때 해 보세요.", "ready"),
    ]),
    ("12편", "회수와 마무리 · 59~64장", [
        ("스킬 3줄 양식", "files/스킬_3줄_양식.md",
         "61장. 이름·언제 쓰나·순서 3줄. 새 대화에서 이름만 불러 같은 결과가 나오는지까지가 완료입니다.", "ready"),
        ("산출물 자기점검", "files/산출물_자기점검.md",
         "62장. 편마다 손에 남아야 하는 것 11칸. 제출하는 곳은 없습니다 — 비어 있는 칸을 스스로 찾는 목록입니다.", "ready"),
    ]),
]

CLIP = []          # 페이지에 심는 복사 대상 원문 (자기완결 — 외부 의존 0)
blocks = ""
for tag, name, items in SESSIONS:
    rows = ""
    for title, href, desc, state in items:
        cps = copy_blocks(href) if (state == "ready" and href) else []
        btns = ""
        for lab, body in cps:
            btns += (f'<button class="cp" type="button" data-i="{len(CLIP)}" '
                     f'title="복사: {H.escape(lab)}" aria-label="복사: {H.escape(lab)}">'
                     f'{IC_COPY}{IC_DONE}<span class="lb">{H.escape(lab)}</span></button>')
            CLIP.append(body)
        crow = f'<div class="copyrow">{btns}</div>' if btns else ""

        if state == "page" and href:
            act = f'<a class="get" href="{href}">열기</a>'
        elif state == "ready" and href:
            # 복사 블록이 있으면 내려받기는 원문 보관용으로 물러난다
            cls = "sub" if btns else "get"
            act = f'<a class="{cls}" href="{href}" download>원문</a>' if btns else                   f'<a class="get" href="{href}" download>내려받기</a>'
        else:
            act = '<em class="wait">준비 중</em>'

        soon = " soon" if not (state in ("ready", "page") and href) else ""
        rows += (f'<div class="item{soon}">'
                 f'<b>{H.escape(title)}</b><span>{H.escape(desc)}</span>'
                 f'<div class="acts">{act}</div>{crow}</div>')
    blocks += f"""
<section class="ses">
  <div class="shead"><span class="stag">{H.escape(tag)}</span><h2>{H.escape(name)}</h2></div>
  <div class="items">{rows}</div>
</section>"""

clip_json = json.dumps(CLIP, ensure_ascii=False)
doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>실습 자료 — AI 기초부터 업무 자동화까지</title>
<style>
:root{{--ink:{hx('ink')};--accent:{hx('accent')};--accent-deep:{hx('accent_deep')};
 --bg:{hx('bg')};--paper:{hx('paper')};--line:{hx('line')};--gray:{hx('gray_text')};
 --wash:{hx('accent_wash')};--tab:{hx('tab')}}}
*{{box-sizing:border-box}}
body{{margin:0;padding:0;background:var(--bg);color:var(--ink);line-height:1.65;
 font-family:Pretendard,'Malgun Gothic',-apple-system,sans-serif}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 20px 80px}}
header{{border-bottom:1px solid var(--ink);padding:52px 0 26px;margin-bottom:12px;position:relative}}
header:after{{content:"";position:absolute;left:0;bottom:-2px;width:260px;height:3px;background:var(--accent)}}
.eyebrow{{color:var(--accent);font-weight:700;letter-spacing:3px;font-size:13px}}
h1{{font-size:32px;margin:12px 0 6px;letter-spacing:-.5px}}
.lead{{color:var(--gray);font-size:15px;margin:0}}
.note{{background:var(--paper);border:1px solid var(--line);border-left:10px solid var(--accent);
 border-radius:12px;padding:18px 22px;margin:26px 0;font-size:14.5px}}
.ses{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:18px 0;
 box-shadow:0 4px 14px rgba(0,0,0,.04)}}
.shead{{display:flex;gap:14px;align-items:center;margin-bottom:14px}}
.stag{{flex:0 0 auto;min-width:64px;text-align:center;background:var(--tab);color:#fff;
 font-weight:800;font-size:13px;padding:5px 10px;border-radius:6px;letter-spacing:.5px}}
h2{{font-size:19px;margin:0;font-weight:700}}
.items{{display:grid;gap:10px}}
.item{{display:grid;grid-template-columns:1fr auto;align-items:center;gap:4px 16px;
 border:1px solid var(--line);border-radius:12px;padding:14px 18px;text-decoration:none;color:var(--ink)}}
a.item{{transition:.15s}}
a.item:hover{{border-color:var(--accent);background:var(--wash);transform:translateY(-1px)}}
.item b{{font-size:15.5px;grid-column:1}}
.item span{{grid-column:1;color:var(--gray);font-size:13.5px}}
.acts{{grid-column:2;grid-row:1/3;display:flex;align-items:center}}
.item em,.acts a{{font-style:normal;font-size:12.5px;font-weight:700;text-decoration:none;
 padding:6px 14px;border-radius:6px;white-space:nowrap;display:inline-block}}
.get{{background:var(--accent);color:#fff}}
a.get:hover{{filter:brightness(1.08)}}
.sub{{background:transparent;color:var(--gray);border:1px solid var(--line)}}
a.sub:hover{{border-color:var(--accent);color:var(--accent)}}
.wait{{background:var(--bg);color:var(--gray);border:1px dashed var(--line)}}
.item.soon{{opacity:.72}}
/* 복사 버튼 — 짧은 프롬프트의 1순위 동선 */
.copyrow{{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;align-items:center;
 margin-top:12px;padding-top:12px;border-top:1px dashed var(--line)}}
.cp{{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:13px;font-weight:700;
 cursor:pointer;color:var(--accent-deep);background:var(--wash);border:1px solid var(--line);
 border-radius:999px;padding:6px 14px 6px 12px;transition:.13s;line-height:1.3}}
.cp:hover{{border-color:var(--accent);background:#fff}}
.cp:active{{transform:translateY(1px)}}
.cp:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.cp .ic{{flex:0 0 auto;display:block}}
.cp .ic-d{{display:none}}
.cp.done{{background:var(--accent);border-color:var(--accent);color:#fff}}
.cp.done .ic-c{{display:none}}
.cp.done .ic-d{{display:block}}
a.room{{position:absolute;right:0;top:52px;font-size:13px;font-weight:700;text-decoration:none;
 color:#fff;background:var(--accent);border-radius:999px;padding:8px 18px}}
a.room:hover{{filter:brightness(1.08)}}
@media (max-width:720px){{a.room{{position:static;display:inline-block;margin-top:12px}}}}
h3{{font-size:18px;margin:38px 0 10px}}
footer{{margin-top:52px;padding-top:22px;border-top:1px solid var(--line);color:var(--gray);font-size:13px}}
</style></head><body><div class="wrap">
<header>
  <div class="eyebrow">AI EDUCATION PROGRAM</div>
  <h1>실습 자료 — AI 기초부터 업무 자동화까지</h1>
  <p class="lead">일반 사무직을 위한 에이전트 사용법 · 실습에 쓰는 양식과 프롬프트</p>
  <a class="room" href="강의실.html">강의실 열기 (영상 보기)</a>
</header>

<div class="note">
  <b>쓰는 법</b><br>
  세션마다 필요한 것만 그때 쓰면 됩니다. 미리 다 받아 둘 필요는 없습니다.<br>
  <b>프롬프트는 「복사」 버튼</b>으로 바로 가져가 붙여 넣으세요 — 내려받지 않아도 됩니다. 「원문」은 나중에 다시 볼 때 쓰는 보관용입니다.<br>
  <b>사전 자료 하나는 예외입니다</b> — 프로필 카드는 <b>시작하기 전에</b> 열어 보세요. 과정 내내 그 사람의 담당자로 실습합니다.
</div>
{blocks}
<script type="application/json" id="clip">{clip_json}</script>

<h3>레퍼런스 이미지는 각자 준비하세요</h3>
<div class="note">
  디자인 실습에서 <b>레퍼런스 이미지 2장</b>을 함께 첨부합니다. 하나는 <b>디자인 언어</b>(카드·아이콘·구성),
  하나는 <b>색 계열</b>입니다. 저작권 때문에 여기서 배포하지 않습니다 —
  <b>여러분 조직에서 잘 만든 자료 2장</b>을 골라 쓰시면 됩니다. 그게 오히려 더 좋은 결과를 냅니다.
</div>

<footer>
  최상훈 · AI Educator &amp; AX Consultant<br>
  이 페이지의 양식·프롬프트는 작성자 본인이 제작했습니다. 실습대상 프로필은 가상 인물입니다.
</footer>
</div>
<script>
(function(){{
  var T = JSON.parse(document.getElementById("clip").textContent);
  function put(s){{
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(s);
    var a = document.createElement("textarea");            // file:// · 구형 폴백
    a.value = s; a.setAttribute("readonly", "");
    a.style.cssText = "position:fixed;top:-9999px";
    document.body.appendChild(a); a.select();
    try {{ document.execCommand("copy"); }} finally {{ document.body.removeChild(a); }}
    return Promise.resolve();
  }}
  document.addEventListener("click", function(e){{
    var b = e.target.closest(".cp"); if (!b) return;
    var lb = b.querySelector(".lb");
    if (b.classList.contains("done")) return;          // 연타 중 라벨이 굳는 것을 막는다
    put(T[+b.dataset.i]).then(function(){{
      var was = lb.textContent;
      lb.textContent = "복사됨"; b.classList.add("done");
      setTimeout(function(){{ lb.textContent = was; b.classList.remove("done"); }}, 1400);
    }});
  }});
}})();
</script>
</body></html>"""

(HERE / "index.html").write_text(doc, encoding="utf-8")
ready = sum(1 for _, _, items in SESSIONS for *_, s in items if s == "ready")
soon = sum(1 for _, _, items in SESSIONS for *_, s in items if s == "soon")
print(f"OK index.html {len(doc.encode()):,} bytes · 자료 {ready}건 · 복사 버튼 {len(CLIP)}개 · 준비 중 {soon}건")
