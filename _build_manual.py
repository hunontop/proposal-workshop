# -*- coding: utf-8 -*-
# 설치 매뉴얼 페이지 생성 — 스크린샷 기반. 색은 덱 skin.json에서 읽어 톤을 맞춘다.
import pathlib, html as H, json

HERE = pathlib.Path(__file__).parent
SKIN = HERE.parent.parent / "projects" / "제안자동화" / "decks" / "venue-AI인터시스" / "skin.json"
C = json.loads(SKIN.read_text(encoding="utf-8"))["colors"]
ASOF = "2026-08-08"


def hx(k):
    return "#" + C[k]


def step(no, title, body, img=None, cap=None):
    # title·body는 내가 쓰는 문장이라 태그를 허용한다(이스케이프하면 <b>가 화면에 그대로 찍힌다).
    # alt·figcaption은 사용자 눈에 보이는 텍스트라 이스케이프한다.
    fig = (f'<figure><img src="img/{img}" alt="{H.escape(cap or "")}" loading="lazy">'
           f'<figcaption>{H.escape(cap or "")}</figcaption></figure>') if img else ""
    return (f'<section class="step"><div class="sh"><span class="no">{no}</span>'
            f'<h3>{title}</h3></div><div class="sb">{body}{fig}</div></section>')


def trap(text):
    return f'<div class="trap"><b>⚠ 여기서 많이 틀립니다</b><p>{text}</p></div>'


# ── 경로 A ────────────────────────────────────────────────────────────────
A = "".join([
    step(1, "VS Code를 내려받아 설치합니다",
         '<p><a href="https://code.visualstudio.com/download" target="_blank" rel="noopener">code.visualstudio.com/download</a> '
         '에서 <b>Windows</b> 버튼을 누릅니다. 설치는 기본값으로 계속 눌러 진행하면 됩니다.</p>'
         '<p class="req">필요 버전: <b>VS Code 1.98.0 이상</b> (확장이 요구하는 최소 버전)</p>',
         "a1_vscode_다운로드.png", "VS Code 내려받기 페이지"),
    step(2, "확장 탭을 엽니다",
         '<p>왼쪽 세로 막대(활동 표시줄)에서 <b>네모 네 개</b> 모양 아이콘을 누릅니다. '
         '단축키는 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd> 입니다.</p>',
         "a3_확장탭.png", "확장 탭을 연 화면"),
    step(3, "claude 를 검색해 <b>Anthropic</b> 것을 설치합니다",
         '<p>검색창에 <code>claude</code> 를 칩니다. 목록 맨 위 <b>Claude Code for VS Code</b> 를 고르고 「설치」를 누릅니다.</p>'
         + trap('검색 결과가 <b>열 개 넘게</b> 나옵니다. 이름이 비슷한 <b>비공식 확장</b>이 대부분입니다. '
                '고를 것은 <b>맨 위 하나</b>뿐이고, 구별하는 표시는 세 가지입니다 — '
                '이름이 정확히 <b>Claude Code for VS Code</b>, 게시자가 <b>Anthropic</b>, 그 옆에 <b>파란 인증 배지</b>.'),
         "a4_확장검색_claude.png", "claude 검색 결과 — 맨 위 하나만 정품입니다"),
    step(4, "로그인합니다",
         '<p>설치가 끝나면 「설치」 자리가 <b>사용 안 함 / 제거</b>로 바뀝니다. 그다음 Claude 패널을 열면 로그인 화면이 나옵니다.</p>'
         '<p>세 가지 중 <b>Claude.ai Subscription</b> 을 고르고 브라우저에서 승인하면 끝입니다.</p>'
         '<p class="req">⚠ <b>유료 구독이 필요합니다</b> — Pro · Max · Team · Enterprise 중 하나. '
         '<b>무료 Claude 계정으로는 사용할 수 없습니다.</b> 구독이 없으면 아래 <a href="#pathb">경로 B</a>로 가세요.</p>',
         "a6_확장설치_로그인선택.png", "설치 완료(제거 버튼) + 로그인 선택 화면"),
    step(5, "이 화면이 나오면 준비 끝입니다",
         '<p>아래쪽에 <b>Ask Claude to edit…</b> 입력창이 보이면 성공입니다. 여기에 말을 걸면 됩니다.</p>',
         "a7_패널_첫화면.png", "로그인 후 Claude 패널"),
])

# ── 경로 B ────────────────────────────────────────────────────────────────
B = "".join([
    step(1, "Antigravity <b>IDE</b>를 내려받습니다",
         '<p><a href="https://antigravity.google/download" target="_blank" rel="noopener">antigravity.google/download</a> 에서 '
         '<b>Antigravity IDE</b> 라고 적힌 칸을 찾아, <b>Windows</b> 열의 <b>Download for x64</b> 를 누릅니다.</p>'
         + trap('이 페이지에는 <b>제품이 네 개</b> 있습니다 — Antigravity 2.0 · CLI · <b>IDE</b> · SDK. '
                '페이지를 열면 <b>2.0이 먼저</b> 보이는데 그건 우리가 쓸 것이 아닙니다. '
                '제목이 <b>Antigravity IDE</b> 인지, 옆의 버전 배지가 <code>v2.1.1</code> 계열인지 확인하고 누르세요.')
         + '<p class="req">Windows 10 (64bit) 이상</p>',
         "b1_antigravity_IDE_다운로드.png", "Antigravity IDE 칸 — 이것이 맞습니다"),
    step(2, "설치하고 <b>구글 계정</b>으로 로그인합니다",
         '<p>받은 파일을 실행하면 설치가 진행됩니다. 처음 열면 환영 화면이 뜹니다 — '
         '<b>Continue with Google</b> 을 누르고 평소 쓰는 구글 계정으로 로그인하면 됩니다.</p>'
         '<p class="req">별도 결제가 없습니다. 공식 안내는 <b>“Available at no charge”</b> 입니다. '
         f'(무료 한도는 바뀔 수 있습니다 · 기준일 {ASOF})</p>',
         "b2_첫실행_로그인.png", "첫 실행 — 구글 계정으로 로그인"),
    step(3, "이 화면이 나오면 준비 끝입니다",
         '<p>왼쪽에 파일 목록, 오른쪽에 <b>Agent</b> 패널이 보이면 성공입니다. 오른쪽 입력창에 말을 걸면 됩니다.</p>'
         '<p>메뉴 구성이 VS Code와 <b>거의 같습니다</b> — 수업에서 “왼쪽 탐색기”, “터미널을 여세요” 같은 안내가 그대로 통합니다. '
         '가운데 <b>Clone Repository</b> 버튼은 수업 중에 쓰게 됩니다.</p>',
         "b3_에디터_본화면.png", "Antigravity IDE 본화면 — 오른쪽이 에이전트 패널"),
])

doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>사전 준비 — 에이전트 설치 안내</title>
<style>
:root{{--ink:{hx('ink')};--accent:{hx('accent')};--accent-deep:{hx('accent_deep')};
 --bg:{hx('bg')};--paper:{hx('paper')};--line:{hx('line')};--gray:{hx('gray_text')};
 --wash:{hx('accent_wash')};--tab:{hx('tab')}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);line-height:1.65;
 font-family:Pretendard,'Malgun Gothic',-apple-system,sans-serif}}
.wrap{{max-width:920px;margin:0 auto;padding:0 20px 90px}}
header{{border-bottom:1px solid var(--ink);padding:48px 0 24px;margin-bottom:10px;position:relative}}
header:after{{content:"";position:absolute;left:0;bottom:-2px;width:240px;height:3px;background:var(--accent)}}
.eyebrow{{color:var(--accent);font-weight:700;letter-spacing:3px;font-size:13px}}
h1{{font-size:30px;margin:12px 0 6px;letter-spacing:-.5px}}
.lead{{color:var(--gray);font-size:15px;margin:0}}
.note{{background:var(--paper);border:1px solid var(--line);border-left:10px solid var(--accent);
 border-radius:12px;padding:18px 22px;margin:24px 0;font-size:14.5px}}
.pick{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0}}
@media(max-width:720px){{.pick{{grid-template-columns:1fr}}}}
.pick a{{display:block;background:var(--paper);border:1px solid var(--line);border-radius:14px;
 padding:20px 22px;text-decoration:none;color:var(--ink);transition:.15s}}
.pick a:hover{{border-color:var(--accent);background:var(--wash)}}
.pick b{{display:block;font-size:18px;margin-bottom:4px}}
.pick .tagline{{color:var(--gray);font-size:13.5px}}
.pick .badge{{display:inline-block;font-size:11.5px;font-weight:700;padding:3px 10px;border-radius:999px;
 background:var(--accent);color:#fff;margin-bottom:10px}}
.pick .badge.free{{background:var(--tab)}}
h2{{font-size:23px;margin:52px 0 4px;padding-top:10px}}
h2 .sub{{display:block;font-size:14px;color:var(--gray);font-weight:400;margin-top:4px}}
.step{{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin:14px 0}}
.sh{{display:flex;gap:14px;align-items:center;margin-bottom:10px}}
.no{{flex:0 0 auto;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;
 font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center}}
h3{{font-size:18px;margin:0;font-weight:700}}
.sb p{{margin:6px 0}}
.req{{font-size:13.5px;color:var(--gray);background:var(--bg);border-radius:8px;padding:10px 14px;margin-top:10px}}
code{{background:var(--bg);border-radius:5px;padding:1px 7px;font-size:13.5px}}
kbd{{background:var(--ink);color:#fff;border-radius:5px;padding:2px 8px;font-size:12.5px;font-weight:600}}
figure{{margin:16px 0 0}}
figure img{{width:100%;border:1px solid var(--line);border-radius:10px;display:block}}
figcaption{{color:var(--gray);font-size:12.5px;margin-top:8px;text-align:center}}
.trap{{background:var(--wash);border:1px solid var(--accent);border-radius:10px;padding:14px 18px;margin:12px 0}}
.trap b{{color:var(--accent-deep);font-size:14px}}
.trap p{{margin:6px 0 0;font-size:14px}}
footer{{margin-top:56px;padding-top:22px;border-top:1px solid var(--line);color:var(--gray);font-size:13px}}
a{{color:var(--accent-deep)}}
</style></head><body><div class="wrap">
<header>
  <div class="eyebrow">수강 전 준비</div>
  <h1>에이전트 하나만 설치해 오세요</h1>
  <p class="lead">AI 기초부터 업무 자동화까지 · 2시간 × 8강</p>
</header>

<div class="note">
  <b>준비물은 이것 하나뿐입니다.</b><br>
  나머지 도구는 <b>수업 중에 함께 설치</b>합니다. 직접 설치해 보는 것이 수업 내용의 일부라서, 미리 하지 않으셔도 됩니다.<br>
  다만 <b>에이전트만은 미리</b> 준비해 주세요. 온라인 과정이라 당일에 한 분씩 도와드리기가 어렵습니다.
</div>

<div class="pick">
  <a href="#patha"><span class="badge">권장</span>
    <b>경로 A · Claude Code</b>
    <span class="tagline">VS Code에 확장을 얹습니다. <b>유료 구독이 있는 분.</b></span></a>
  <a href="#pathb"><span class="badge free">무료</span>
    <b>경로 B · Antigravity IDE</b>
    <span class="tagline">별도 프로그램을 내려받습니다. <b>구독이 없는 분.</b></span></a>
</div>

<div class="note">
  둘 중 <b>어느 쪽이든 수업을 따라오는 데 문제없습니다.</b>
  다만 무료 쪽은 응답 품질과 사용량 한도가 낮아 실습 중 기다림이 생길 수 있습니다. 감추지 않고 미리 말씀드립니다.
</div>

<h2 id="patha">경로 A · Claude Code<span class="sub">VS Code + 확장 · 유료 구독 필요</span></h2>
{A}

<h2 id="pathb">경로 B · Antigravity IDE<span class="sub">단독 프로그램 · 무료 · 구글 계정</span></h2>
{B}

<h2>준비되면 여기까지입니다<span class="sub">나머지는 수업에서</span></h2>
<div class="note">
  Python·Git·공고 수집 도구·자동화 공정은 <b>전부 수업 중에 함께 설치</b>합니다.
  설치하다 막히는 경험 자체가 수업의 한 대목이라, 미리 해 오시면 오히려 그 시간을 놓칩니다.<br><br>
  <b>막히면 이렇게 하세요</b> — 화면의 오류 메시지를 <b>그대로 복사해 에이전트에게 붙여넣으세요.</b>
  이 과정에서 계속 쓰게 될 방법이고, 준비 단계에서 미리 한 번 해 보시는 것도 좋습니다.
</div>

<footer>
  화면은 {ASOF} 기준입니다. 프로그램이 업데이트되면 버튼 위치나 문구가 달라질 수 있습니다.<br>
  일부 화면은 웹 버전 VS Code에서 촬영했습니다 — 설치한 VS Code와 구성이 같습니다.<br>
  최상훈 · AI Educator &amp; AX Consultant
</footer>
</div></body></html>"""

out = HERE / "설치안내.html"
out.write_text(doc, encoding="utf-8")
print("OK", out.name, len(doc), "chars")
