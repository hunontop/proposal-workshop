# 실습 자료 배포 페이지 생성 (GitHub Pages용 index.html)
# 전례 = _검정제출/배포/_build.py · 색은 덱 skin.json에서 읽어 톤을 자동 일치시킨다.
import pathlib, html as H, json

HERE = pathlib.Path(__file__).parent
SKIN = HERE.parent.parent / "projects" / "제안자동화" / "decks" / "venue-AI인터시스" / "skin.json"
C = json.loads(SKIN.read_text(encoding="utf-8"))["colors"]


def hx(k):
    return "#" + C[k]


SITE = "https://hunontop.github.io/proposal-workshop/"

# ── 세션별 자료 ────────────────────────────────────────────────────────────
# state: ready = 지금 내려받을 수 있음 / soon = 개설 전 준비 중
SESSIONS = [
    ("사전", "수강 전에", [
        ("프로필 카드 — 창업 준비자 김하늘", "files/프로필카드_창업준비자_김하늘.md",
         "과정 내내 이 사람의 담당자로 실습합니다. 빈칸 5종이 그대로 실습 재료입니다.", "ready"),
        ("에이전트 설치 안내 (화면 그대로 따라 하기)", "설치안내.html",
         "이것 하나만 미리 준비하면 됩니다. Claude Code(유료) / Antigravity IDE(무료) 두 갈래 · 스크린샷 안내.", "page"),
    ]),
    ("S1~S3", "이해·질문 / 문서·조사 / 덱·첫걸음", [
        ("프롬프트 4요소 카드", None, "맥락·역할·예시·제약 한 장 요약.", "soon"),
    ]),
    ("S4", "설치·시운전", [
        ("내 업무 진단 시트", None, "AI 인터뷰로 내 업무 하나를 5단계로 분해하는 템플릿.", "soon"),
    ]),
    ("S5", "선택·브리프", [
        ("브리프 예시 — 말벗ON", "files/브리프_예시_말벗ON.md",
         "공정에 넣는 요구사항 문서가 실제로 어떻게 생겼는지. 없는 값은 비워 둔 형태 그대로입니다.", "ready"),
    ]),
    ("S6", "관문·도식", [
        ("도식 5항목 판정표", None, "생성된 도식 후보를 다섯 기준으로 판정하는 표.", "soon"),
    ]),
    ("S7", "디자인·이미지", [
        ("배포 프롬프트 ① 기본 — 3병렬 카드", "files/프롬프트_기본_3병렬카드.md",
         "실습 '같은 프롬프트, 스무 개의 그림'에 쓰는 프롬프트. 실제로 채택된 장의 것입니다.", "ready"),
        ("배포 프롬프트 ② 정직 문법 — 검토요망", "files/프롬프트_정직문법_검토요망.md",
         "근거가 없는 자리를 어떻게 비워 두는지가 프롬프트까지 흘러온 예. 여유가 있을 때 해 보세요.", "ready"),
    ]),
    ("S8", "승인·마무리", [
        ("스킬 3줄 양식", None, "반복 작업 하나를 스킬로 굳히는 최소 양식.", "soon"),
    ]),
]

blocks = ""
for tag, name, items in SESSIONS:
    rows = ""
    for title, href, desc, state in items:
        if state == "page" and href:
            rows += (f'<a class="item" href="{href}">'
                     f'<b>{H.escape(title)}</b><span>{H.escape(desc)}</span>'
                     f'<em class="get">열기</em></a>')
        elif state == "ready" and href:
            rows += (f'<a class="item" href="{href}" download>'
                     f'<b>{H.escape(title)}</b><span>{H.escape(desc)}</span>'
                     f'<em class="get">내려받기</em></a>')
        else:
            rows += (f'<div class="item soon">'
                     f'<b>{H.escape(title)}</b><span>{H.escape(desc)}</span>'
                     f'<em class="wait">준비 중</em></div>')
    blocks += f"""
<section class="ses">
  <div class="shead"><span class="stag">{H.escape(tag)}</span><h2>{H.escape(name)}</h2></div>
  <div class="items">{rows}</div>
</section>"""

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
.item em{{grid-column:2;grid-row:1/3;font-style:normal;font-size:12.5px;font-weight:700;
 padding:6px 14px;border-radius:6px;white-space:nowrap}}
.get{{background:var(--accent);color:#fff}}
.wait{{background:var(--bg);color:var(--gray);border:1px dashed var(--line)}}
.item.soon{{opacity:.72}}
h3{{font-size:18px;margin:38px 0 10px}}
footer{{margin-top:52px;padding-top:22px;border-top:1px solid var(--line);color:var(--gray);font-size:13px}}
</style></head><body><div class="wrap">
<header>
  <div class="eyebrow">AI EDUCATION PROGRAM</div>
  <h1>실습 자료 — AI 기초부터 업무 자동화까지</h1>
  <p class="lead">반복업무 1/10로 줄이기 · 2시간 × 8강 · 실습에 쓰는 양식과 프롬프트</p>
</header>

<div class="note">
  <b>쓰는 법</b><br>
  세션마다 필요한 자료를 그때 내려받으면 됩니다. 미리 다 받아 둘 필요는 없습니다.<br>
  <b>사전 자료 하나는 예외입니다</b> — 프로필 카드는 첫 시간 전에 열어 보고 오세요. 과정 내내 그 사람의 담당자로 실습합니다.
</div>
{blocks}

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
</div></body></html>"""

(HERE / "index.html").write_text(doc, encoding="utf-8")
ready = sum(1 for _, _, items in SESSIONS for *_, s in items if s == "ready")
soon = sum(1 for _, _, items in SESSIONS for *_, s in items if s == "soon")
print(f"OK index.html {len(doc)} bytes · 내려받기 {ready}건 · 준비 중 {soon}건 · {SITE}")
