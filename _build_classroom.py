# -*- coding: utf-8 -*-
"""강의실 페이지 생성 (강의실.html) — 좌 플레이어 / 우 커리큘럼 사이드바.

계획 정본 = 강의 저장소 `촬영준비_문제파악.md` §H · 인계 §2-12(레퍼런스 실측).
색은 `_build.py`와 같은 자리(`skin.json`)에서 읽는다 — 이 저장소 밖을 참조하지 않는다.

## 이 페이지가 하는 일

- 편 12개를 **사이드바**에 세우고, 고른 편을 왼쪽에서 재생한다
- 편마다 **차례(레슨 예정 단위)**와 **그 편에서 쓰는 실습 자료**를 함께 보인다
- **본 표시는 localStorage**다 — 그 브라우저에만 남는다. 화면에도 그렇게 적었다(서버가 없다)

## 고칠 때

촬영이 끝난 편은 `E`의 `vid` 자리에 유튜브 ID를 넣으면 그 편이 열린다.
⚠ **재생시간과 차례의 시작 초는 편집본에서 실측해서 넣는다.** 발표노트의 ⏱는 추정치라
화면에 박으면 실제 영상과 어긋난다 — 정직 표기 위반이다(§H 선행 조건 2).
**비워 두면 화면에 안 나온다** — 차례 오른쪽 끝은 시작 초가 들어올 때까지 장 번호를 대신 보인다.
빌드할 때 미기입 항목을 알려 준다.

⚠ 유튜브는 **일부공개(unlisted)**로 올린다. 비공개(private)는 임베드가 깨진다.
"""
import pathlib, html as H, json, re

HERE = pathlib.Path(__file__).parent
C = json.loads((HERE / "skin.json").read_text(encoding="utf-8"))["colors"]


def hx(k):
    return "#" + C[k]


# ── 복사 버튼 ─────────────────────────────────────────────────────────────
# 실습 자료 페이지(`_build.py`)와 **같은 규약**이다 — md의 펜스 코드블록을 수확하고
# 라벨은 바로 앞의 ##/### 제목에서 가져온다. 연장통 정책: 복사가 1순위, 내려받기는 보관용.
# ⚠ 지금은 **COPY_EPISODES에 든 편만** 버튼을 단다(2026-09-02 사용자 지시: 1·2편만).
COPY_EPISODES = {1, 2}

# ── 공개 범위 ─────────────────────────────────────────────────────────────
# 이 페이지도 **홍보용**이다(2026-09-02 결정). 1·2편만 열고 나머지는 **자물쇠**다 —
# 사이드바에서 누르면 편이 열리는 대신 **신청 페이지**로 간다.
# ⚠ UI 표시일 뿐이다. 진짜 잠금은 로그인 사이트로 옮길 때 성립한다.
OPEN_EPISODES = {1, 2}
SIGNUP = "https://event-us.kr/aiintersyslec/event/134312"

IC_COPY = ('<svg class="ic ic-c" viewBox="0 0 24 24" width="13" height="13" fill="none" '
           'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/>'
           '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>')
IC_DONE = ('<svg class="ic ic-d" viewBox="0 0 24 24" width="13" height="13" fill="none" '
           'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>')

_FENCE = re.compile(r"\n```[^\n]*\n(.*?)\n```", re.S)
_HEAD = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.M)


def _label(raw, fallback):
    if not raw:
        return fallback
    t = re.sub(r"[`*]", "", raw).strip()
    t = re.sub(r"^\d+\.\s*", "", t)
    return re.split(r"\s+—\s+", t)[0].strip() or fallback


def copy_blocks(rel):
    f = HERE / rel
    if not f.is_file() or not rel.endswith(".md"):
        return []
    md = f.read_text(encoding="utf-8")
    out = []
    for m in _FENCE.finditer(md):
        heads = _HEAD.findall(md[:m.start()])
        out.append((_label(heads[-1] if heads else None, "프롬프트 전체"), m.group(1)))
    return out


TITLE = "AI 기초부터 업무 자동화까지"
LEAD = "일반 사무직을 위한 에이전트 사용법 · 영상 12편"

# ── 커리큘럼 ──────────────────────────────────────────────────────────────
# (편, 제목, 장 범위, 유튜브ID, 재생시간, [차례], [자료])
#   차례 = (번호, 제목, 장 범위, 시작 초 or None)
#   자료 = (제목, 경로) — 실습 자료 페이지(index.html)와 같은 파일을 가리킨다
E = [
 (1, "왜 이 과정인가", "1~13장", "hzRFqWST0rM", None, [
    ("1-1", "여는 말 · 강사 소개", "1~2장", None),
    ("1-2", "왜 업무는 그대로일까", "3~6장", None),
    ("1-3", "이 과정의 목표", "7~10장", None),
    ("1-4", "준비물과 주인공", "11~13장", None)], [
    ("에이전트 설치 안내", "설치안내.html"),
    ("프로필 카드 — 창업 준비자 김하늘", "files/프로필카드_창업준비자_김하늘.md")]),
 (2, "AI는 어떻게 답하나", "14~20장", "i8eYYERmgtk", None, [
    ("2-1", "확률로 고른다", "14~15장", None),
    ("2-2", "세 줄과 대화창", "16~17장", None),
    ("2-3", "실습 · 잘 묻는 법", "18장", None),
    ("2-4", "대화 관리와 세 단계", "19~20장", None)], [
    ("프롬프트 4요소 카드 — 첫 실습", "files/프롬프트_4요소_카드.md")]),
 (3, "공고 조사와 수작업 우회", "21~24장", None, None, [
    ("3-1", "담장은 첨부 하나입니다", "21~22장", None),
    ("3-2", "실습 · 수작업으로 가져다줍니다", "23장", None),
    ("3-3", "마크다운", "24장", None)], [
    ("실습 프롬프트 — 공고 조사", "files/프롬프트_공고조사.md")]),
 (4, "스킬과 덱", "25~27장", None, None, [
    ("4-1", "스킬이란", "25장", None),
    ("4-2", "실습 · 분석을 슬라이드덱으로", "26장", None),
    ("4-3", "방금 한 것이 5단계입니다", "27장", None)], [
    ("실습 프롬프트 — 분석을 슬라이드덱으로", "files/프롬프트_분석을_덱으로.md")]),
 (5, "에이전트 첫걸음", "28~32장", None, None, [
    ("5-1", "채팅 AI와 에이전트의 차이", "28~29장", None),
    ("5-2", "실습 · 첫 한마디로 파일 만들기", "30장", None),
    ("5-3", "여기가 어디인가", "31장", None),
    ("5-4", "실패는 정상입니다", "32장", None)], [
    ("실습 프롬프트 — 에이전트 첫걸음", "files/프롬프트_에이전트_첫걸음.md"),
    ("경로 · 작업 폴더 · 터미널", "files/경로_작업폴더_터미널.md"),
    ("승인 판단 카드", "files/승인판단_카드.md")]),
 (6, "설치와 시운전", "33~38장", None, None, [
    ("6-1", "설치 ① 공고 수집 스킬", "33~34장", None),
    ("6-2", "기준은 우리 카드가 줍니다", "35장", None),
    ("6-3", "설치 ②와 시운전", "36~38장", None)], [
    ("설치 확인 한마디", "files/설치확인_한마디.md")]),
 (7, "공정 입구 · 선택과 브리프", "39~44장", None, None, [
    ("7-1", "공정으로 · 입구는 둘, 엔진은 하나", "39~41장", None),
    ("7-2", "선택 · AI가 대신하지 않습니다", "42장", None),
    ("7-3", "실습 · 브리프 한 장 만들기", "43장", None),
    ("7-4", "go, 여정 폴더가 생깁니다", "44장", None)], [
    ("실습 프롬프트 — 브리프 한 장 만들기", "files/프롬프트_브리프_한장.md"),
    ("브리프 예시 — 말벗ON", "files/브리프_예시_말벗ON.md")]),
 (8, "관문 · AI를 멈춰 세우는 자리", "45~46장", None, None, [
    ("8-1", "AI가 스스로 붉게 칠하는 자리", "45장", None),
    ("8-2", "관문 · 실패로 멈춥니다", "46장", None)], []),
 (9, "도식 · 말로 먼저 그린다", "47~50장", None, None, [
    ("9-1", "그리고 만듭니다 · napkin 시작하기", "47~48장", None),
    ("9-2", "말로 먼저 그려봅니다", "49장", None),
    ("9-3", "그림의 역할 분담", "50장", None)], [
    ("도식 5항목 판정표", "files/도식_5항목_판정표.md")]),
 (10, "디자인과 이미지 프롬프트", "51~54장", None, None, [
    ("10-1", "디자인 관문 · 실물 확인", "51장", None),
    ("10-2", "이미지를 만드는 두 가지 길", "52장", None),
    ("10-3", "프롬프트 = 결정의 압축본", "53장", None),
    ("10-4", "같은 프롬프트, 스무 개의 그림", "54장", None)], [
    ("배포 프롬프트 ① 기본 — 3병렬 카드", "files/프롬프트_기본_3병렬카드.md"),
    ("배포 프롬프트 ② 정직 문법 — 검토요망", "files/프롬프트_정직문법_검토요망.md")]),
 (11, "생산과 최종 승인", "55~57장", None, None, [
    ("11-1", "회사 기밀을 넣어도 됩니까", "55장", None),
    ("11-2", "기다림의 정체", "56장", None),
    ("11-3", "완성 덱 · 최종 승인", "57장", None)], []),
 (12, "회수와 마무리", "58~64장", None, None, [
    ("12-1", "회수합니다 · AI티가 난다는 말", "58~59장", None),
    ("12-2", "손과 공정 · 스킬로 굳히기", "60~61장", None),
    ("12-3", "과정에서 손에 든 것 · 마무리", "62~64장", None)], []),
]

CLIP: list[str] = []


def _files(no, fs):
    out = []
    for title, href in fs:
        cps = []
        if no in COPY_EPISODES:
            for lab, body in copy_blocks(href):
                cps.append({"lab": lab, "i": len(CLIP)})
                CLIP.append(body)
        out.append({"title": title, "href": href, "copy": cps})
    return out


# ⚠ 잠긴 편은 **DATA에서 링크·자료를 지운다.** 사이드바만 가리면 페이지 소스에
#   유튜브 ID가 그대로 남아 자물쇠가 무의미해진다(홍보 페이지의 최소선).
DATA = [dict(n=n, title=t, slides=s,
             vid=(v if n in OPEN_EPISODES else None),
             dur=(d if n in OPEN_EPISODES else None),
             chapters=[dict(no=a, title=b, slides=c, t=e) for a, b, c, e in ch],
             files=(_files(n, fs) if n in OPEN_EPISODES else []))
        for n, t, s, v, d, ch, fs in E]

IC_LOCK = ('<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" '
           'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>')

side = ""
for e in DATA:
    ready = bool(e["vid"])
    if e["n"] not in OPEN_EPISODES:            # 잠금 — 누르면 신청 페이지로 나간다
        side += ('<a class="ep lock" href="%s" target="_blank" rel="noopener">'
                 '<span class="epn">%d편</span>'
                 '<span class="ept"><b>%s</b><i>수강 신청하고 보기</i></span>'
                 '<span class="epl">%s</span></a>'
                 % (SIGNUP, e["n"], H.escape(e["title"]), IC_LOCK))
        continue
    meta = e["dur"] or ("" if ready else "촬영 준비 중")
    side += ('<button class="ep%s" data-n="%d" type="button">'
             '<span class="epn">%d편</span>'
             '<span class="ept"><b>%s</b>%s</span>'
             '<span class="epd" aria-hidden="true"></span></button>'
             % ("" if ready else " soon", e["n"], e["n"], H.escape(e["title"]),
                ("<i>%s</i>" % H.escape(meta)) if meta else ""))

CSS = """
:root{--ink:{ink};--accent:{accent};--accent-deep:{deep};--bg:{bg};--paper:{paper};
 --line:{line};--gray:{gray};--wash:{wash};--tab:{tab}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.65;
 font-family:Pretendard,'Malgun Gothic',-apple-system,sans-serif}
a{color:inherit}
header{border-bottom:1px solid var(--ink);padding:34px 24px 20px;position:relative}
header:after{content:"";position:absolute;left:24px;bottom:-2px;width:220px;height:3px;background:var(--accent)}
.eyebrow{color:var(--accent);font-weight:700;letter-spacing:3px;font-size:12px}
h1{font-size:25px;margin:9px 0 4px;letter-spacing:-.5px}
.lead{color:var(--gray);font-size:14px;margin:0}
.top{position:absolute;right:24px;top:34px;font-size:13px;font-weight:700;text-decoration:none;
 color:var(--accent-deep);border:1px solid var(--line);background:var(--paper);
 border-radius:999px;padding:7px 16px}
.top:hover{border-color:var(--accent)}
.room{display:grid;grid-template-columns:1fr 372px;gap:22px;max-width:1420px;margin:0 auto;
 padding:22px 24px 70px;align-items:start}
.stage{background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden;
 box-shadow:0 4px 14px rgba(0,0,0,.04)}
.frame{position:relative;width:100%;aspect-ratio:16/9;background:#161210}
.frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.blank{position:absolute;inset:0;display:flex;flex-direction:column;gap:8px;align-items:center;
 justify-content:center;color:#CFC5B8;text-align:center;padding:24px}
.blank b{font-size:17px;color:#EDE6DC}
.blank span{font-size:13.5px}
.meta{padding:20px 24px 24px}
.meta h2{font-size:20px;margin:0 0 4px}
.meta .sub{color:var(--gray);font-size:13.5px;margin:0 0 16px}
.sect{margin-top:18px;padding-top:16px;border-top:1px dashed var(--line)}
.sect h3{font-size:13px;letter-spacing:1px;color:var(--gray);margin:0 0 10px;font-weight:800}
.ch{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:baseline;padding:9px 0;
 border-bottom:1px solid var(--line);font-size:14.5px}
.ch:last-child{border-bottom:0}
.ch em{font-style:normal;font-weight:800;color:var(--accent-deep);font-size:13px}
.ch i{font-style:normal;color:var(--gray);font-size:12.5px;white-space:nowrap}
.mat{display:flex;flex-wrap:wrap;gap:8px}
.mat a{display:inline-block;font-size:13px;font-weight:700;text-decoration:none;color:var(--accent-deep);
 background:var(--wash);border:1px solid var(--line);border-radius:999px;padding:6px 14px}
.mat a:hover{border-color:var(--accent);background:#fff}
.mat p{color:var(--gray);font-size:13.5px;margin:0}
/* 복사 버튼 — 실습 자료 페이지와 같은 문법(연장통 정책: 복사가 1순위) */
.matrow{flex-basis:100%;display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:2px;
 padding-top:10px;border-top:1px dashed var(--line)}
.cp{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12.5px;font-weight:700;
 cursor:pointer;color:var(--accent-deep);background:var(--wash);border:1px solid var(--line);
 border-radius:999px;padding:5px 13px 5px 11px;transition:.13s;line-height:1.3}
.cp:hover{border-color:var(--accent);background:#fff}
.cp:active{transform:translateY(1px)}
.cp:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.cp .ic{flex:0 0 auto;display:block}
.cp .ic-d{display:none}
.cp.done{background:var(--accent);border-color:var(--accent);color:#fff}
.cp.done .ic-c{display:none}
.cp.done .ic-d{display:block}
aside{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px;
 box-shadow:0 4px 14px rgba(0,0,0,.04);position:sticky;top:22px}
aside h2{font-size:13px;letter-spacing:1px;color:var(--gray);margin:6px 8px 12px;font-weight:800}
.ep{display:grid;grid-template-columns:auto 1fr auto;gap:11px;align-items:center;width:100%;
 text-align:left;font:inherit;cursor:pointer;background:transparent;border:1px solid transparent;
 border-radius:11px;padding:10px 11px;transition:.13s}
.ep:hover{background:var(--wash)}
.ep[aria-current="true"]{background:var(--wash);border-color:var(--accent)}
.epn{min-width:42px;text-align:center;background:var(--tab);color:#fff;font-weight:800;font-size:12px;
 padding:4px 7px;border-radius:6px}
.ep.soon .epn{background:var(--bg);color:var(--gray);border:1px dashed var(--line)}
.ept{display:block;min-width:0}
.ept b{display:block;font-size:14.5px;font-weight:700;line-height:1.35}
.ept i{display:block;font-style:normal;color:var(--gray);font-size:12px}
.epd{width:9px;height:9px;border-radius:50%;border:1.5px solid var(--line)}
.ep.seen .epd{background:var(--accent);border-color:var(--accent)}
.ep.soon{opacity:.62}
a.ep.lock{text-decoration:none;opacity:.85}
a.ep.lock:hover{background:var(--wash);border-color:var(--accent)}
a.ep.lock .epn{background:var(--bg);color:var(--gray);border:1px dashed var(--line)}
a.ep.lock .ept i{color:var(--accent-deep);font-weight:700}
.epl{color:var(--gray);display:flex;align-items:center}
.foot{margin:14px 8px 4px;padding-top:12px;border-top:1px dashed var(--line);color:var(--gray);
 font-size:12px;line-height:1.6}
footer{max-width:1420px;margin:0 auto;padding:0 24px 60px;color:var(--gray);font-size:13px}
@media (max-width:1040px){
  .room{grid-template-columns:1fr}
  aside{position:static}
  header:after{width:150px}
  .top{position:static;display:inline-block;margin-top:12px}
}
""".replace("{ink}", hx("ink")).replace("{accent}", hx("accent")).replace("{deep}", hx("accent_deep")).replace("{bg}", hx("bg")).replace("{paper}", hx("paper")).replace("{line}", hx("line")).replace("{gray}", hx("gray_text")).replace("{wash}", hx("accent_wash")).replace("{tab}", hx("tab"))

JS = """
(function(){
  var D = JSON.parse(document.getElementById("d").textContent),
      T = JSON.parse(document.getElementById("clip").textContent),
      IC = document.getElementById("ic").textContent,
      K = "pw-seen", cur = null, seen = {};
  function put(s){
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(s);
    var a = document.createElement("textarea");          // file:// · 구형 폴백
    a.value = s; a.setAttribute("readonly", "");
    a.style.cssText = "position:fixed;top:-9999px";
    document.body.appendChild(a); a.select();
    try { document.execCommand("copy"); } finally { document.body.removeChild(a); }
  }
  document.addEventListener("click", function(ev){
    var b = ev.target.closest && ev.target.closest(".cp");
    if (!b) return;
    put(T[+b.dataset.i]);
    b.classList.add("done");
    setTimeout(function(){ b.classList.remove("done"); }, 1200);
  });
  try { seen = JSON.parse(localStorage.getItem(K) || "{}") || {}; } catch(e) {}
  function save(){ try { localStorage.setItem(K, JSON.stringify(seen)); } catch(e) {} }
  function mmss(n){
    var h = Math.floor(n / 3600), m = Math.floor(n % 3600 / 60), s = n % 60,
        p = function(x){ return (x < 10 ? "0" : "") + x; };
    return (h ? h + ":" + p(m) : m) + ":" + p(s);
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function paint(){
    [].forEach.call(document.querySelectorAll(".ep"), function(b){
      b.setAttribute("aria-current", String(cur === b.dataset.n));
      b.classList.toggle("seen", !!seen[b.dataset.n]);
    });
  }
  function show(n){
    var e = D.filter(function(x){ return String(x.n) === String(n); })[0];
    if (!e) return;
    cur = String(n);
    var f = document.getElementById("frame");
    if (e.vid) {
      f.innerHTML = '<iframe src="https://www.youtube.com/embed/' + e.vid +
        '?rel=0&modestbranding=1" title="' + esc(e.n) + '\\uD3B8" allowfullscreen ' +
        'allow="accelerometer;clipboard-write;encrypted-media;picture-in-picture"></iframe>';
      seen[cur] = 1; save();
    } else {
      f.innerHTML = '<div class="blank"><b>\\uCD2C\\uC601 \\uC900\\uBE44 \\uC911\\uC785\\uB2C8\\uB2E4</b>' +
        '<span>\\uC774 \\uD3B8\\uC758 \\uCC28\\uB840\\uC640 \\uC790\\uB8CC\\uB294 ' +
        '\\uC544\\uB798\\uC5D0\\uC11C \\uBBF8\\uB9AC \\uBCF4\\uC2E4 \\uC218 \\uC788\\uC2B5\\uB2C8\\uB2E4.</span></div>';
    }
    document.getElementById("mt").textContent = e.n + "\\uD3B8 \\u00B7 " + e.title;
    document.getElementById("ms").textContent = e.dur || "";
    document.getElementById("mc").innerHTML = e.chapters.map(function(c){
      var jump = (e.vid && c.t != null)
        ? '<a href="https://www.youtube.com/watch?v=' + e.vid + '&t=' + c.t + 's" target="_blank" rel="noopener">' + esc(c.title) + '</a>'
        : esc(c.title);
      var mark = (c.t != null) ? mmss(c.t) : c.slides;   // 시간이 들어오면 장 번호를 밀어낸다
      return '<div class="ch"><em>' + esc(c.no) + '</em><span>' + jump + '</span><i>' + esc(mark) + '</i></div>';
    }).join("");
    document.getElementById("mf").innerHTML = e.files.length
      ? e.files.map(function(x){
          var a = '<a href="' + x.href + '">' + esc(x.title) + '</a>';
          if (!x.copy || !x.copy.length) return a;
          var b = x.copy.map(function(c){
            return '<button class="cp" type="button" data-i="' + c.i + '" title="\\uBCF5\\uC0AC: ' +
                   esc(c.lab) + '">' + IC + '<span>' + esc(c.lab) + '</span></button>';
          }).join("");
          return a + '<div class="matrow">' + b + '</div>';
        }).join("")
      : '<p>\\uC774 \\uD3B8\\uC5D0\\uB294 \\uB530\\uB85C \\uB0B4\\uB824\\uBC1B\\uC744 \\uC790\\uB8CC\\uAC00 \\uC5C6\\uC2B5\\uB2C8\\uB2E4.</p>';
    paint();
    if (location.hash !== "#" + n) history.replaceState(null, "", "#" + n);
  }
  [].forEach.call(document.querySelectorAll(".ep"), function(b){
    b.addEventListener("click", function(){ show(b.dataset.n); });
  });
  var first = D.filter(function(x){ return x.vid; })[0];
  show((location.hash || "").replace("#", "") || (first ? first.n : 1));
})();
"""

doc = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>강의실 — ' + H.escape(TITLE) + '</title>'
       '<style>' + CSS + '</style></head><body>'
       '<header><div class="eyebrow">AI EDUCATION PROGRAM</div>'
       '<h1>' + H.escape(TITLE) + '</h1>'
       '<p class="lead">' + H.escape(LEAD) + '</p>'
       '<a class="top" href="index.html">실습 자료 전체 보기</a></header>'
       '<div class="room"><main class="stage"><div class="frame" id="frame"></div>'
       '<div class="meta"><h2 id="mt"></h2><p class="sub" id="ms"></p>'
       '<div class="sect"><h3>이 편의 차례</h3><div id="mc"></div></div>'
       '<div class="sect"><h3>이 편에서 쓰는 자료</h3><div class="mat" id="mf"></div></div>'
       '</div></main>'
       '<aside><h2>커리큘럼 · 12편</h2>' + side +
       '<p class="foot">본 표시(●)는 <b>이 브라우저에만</b> 남습니다. 기기를 바꾸면 사라집니다 — '
       '서버에 진도를 저장하지 않습니다.<br>재생시간과 차례의 시간 표시는 '
       '<b>편집이 끝난 편부터</b> 채웁니다.</p></aside></div>'
       '<footer>최상훈 · AI Educator &amp; AX Consultant</footer>'
       '<script type="application/json" id="d">' +
       json.dumps(DATA, ensure_ascii=False) + '</script>'
       '<script type="application/json" id="clip">' +
       json.dumps(CLIP, ensure_ascii=False) + '</script>'
       '<script type="text/plain" id="ic">' + IC_COPY + IC_DONE + '</script>'
       '<script>' + JS + '</script></body></html>')

out = HERE / "강의실.html"
out.write_text(doc, encoding="utf-8")
try:
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ready = [e for e in DATA if e["vid"]]
print("OK %s  %d chars · 편 %d개 · 영상 %d편" % (out.name, len(doc), len(DATA), len(ready)))
for e in ready:
    if not e["dur"]:
        print("  대기 · %d편 재생시간 미기입 (편집본에서 실측해 E에 넣을 것)" % e["n"])
    if any(c["t"] is None for c in e["chapters"]):
        print("  대기 · %d편 차례 시작 초 미기입 (넣으면 차례가 그 지점으로 뛴다)" % e["n"])
