import os
import random
from urllib.parse import quote

# 1. 타겟 지역 데이터 축소 (강서구, 양천구, 영등포구 / 구별 동 3개)
seoul_data = {
    'gangseo': {'name': '강서구', 'dongs': ['등촌1동', '화곡본동', '가양1동']},
    'yangcheon': {'name': '양천구', 'dongs': ['목1동', '신월1동', '신정1동']},
    'yeongdeungpo': {'name': '영등포구', 'dongs': ['여의동', '당산1동', '문래동']}
}

site_name = "로얄테라피"
base_url = "https://royal-therapy.netlify.app"
base_dir = "output"
os.makedirs(base_dir, exist_ok=True)

# 업체 리스트
companies_data = [
    {"name": "퀸즈홈테라피", "tel": "0507-1280-3296"},
    {"name": "한국미인테라피", "tel": "0507-1280-3140"},
    {"name": "오늘밤테라피", "tel": "0507-1280-3199"},
    {"name": "주주테라피", "tel": "0507-1280-3197"},
    {"name": "기쁨테라피", "tel": "0507-1280-3183"},
    {"name": "미인클럽테라피", "tel": "0507-1280-3180"}
]

# 텍스트 스피닝용 데이터 풀 (출장마사지 키워드는 본문 문장 내 자연스러운 단어로만 포함)
leads_sub = [
    "씻을 기운조차 없는 날이 있죠. 제휴 업체가 편안함을 안고 {dong} 출장마사지로 찾아갑니다.",
    "끝나고 캐모마일 차 한 잔이면 밤이 짧아지는 날. {dong} 출장마사지 고객님을 위한 케어입니다.",
    "복잡한 일상에서 벗어나고 싶은 저녁, {dong} 지역에서 출장마사지 프리미엄 스웨디시를 경험해보세요.",
    "조용히 위로받고 싶은 날, 전문 테라피스트가 {dong} 출장마사지 예약에 맞춰 방문합니다."
]

intro_phrases = ["집게핀으로 대충 올린 날.", "발바닥이 뜨거운 날.", "어제 요가를 했는데 어깨가 더 뭉친 날.", "머리가 복잡한 날.", "오른손만 저리고 뻐근한 날."]
chat_pool = [
    ("아로마 오일 테라피는 향이 세지 않나요?", "향이 먼저 들어오고 손이 뒤따르는 정도입니다."),
    ("머리를 수건으로 감싼 채인데 괜찮나요?", "네. 그 상태 그대로 문만 열어 주시면 됩니다."),
    ("스페셜 테라피도 오일로 하나요?", "세 코스 모두 프리미엄 오일을 씁니다."),
    ("받기 전에 꼭 씻어야 하나요?", "꼭 하지 않으셔도 됩니다. 편한 대로 하세요."),
    ("끝나고 미지근한 물을 마셔도 되나요?", "네, 따뜻한 것 한 잔을 드셔도 좋고 그대로 주무셔도 됩니다.")
]
review_pool = [
    ("H님", "스페셜 테라피 120분", "손목을 조심히 다뤄 주는 점이 좋았어요. 제가 불편해하는 곳이라 더 기억에 남죠."),
    ("진OO", "아로마 오일 테라피 120분", "아이와 하루 종일 놀아 준 뒤였어요. 이번엔 제가 쉬는 순서라 반가웠죠."),
    ("곽OO", "아로마 오일 테라피 60분", "쓰던 베개로 받으니 마음이 편했어요. 높이가 익숙해서 더 그랬겠죠."),
    ("손OO", "순환 테라피 60분", "식탁 위에 휴대폰을 뒤집어 놨어요. 생각보다 힐링에 집중하기 좋았습니다.")
]
faq_pool = [
    ("오일 냄새 오래 가나요", "세 코스 모두 오일을 씁니다. 걱정되면 문자에 적어 주세요."),
    ("숙소도 되나요", "네, 호텔이나 숙소로도 방문 가능합니다."),
    ("휴일도 되나요", "네, 주말 및 공휴일에도 방문합니다."),
    ("처음인데 뭘 준비하나요", "없습니다. 편안한 마음이면 충분합니다.")
]
rules_pool = [
    "약속한 시간에 맞춰 갑니다. 늦으면 먼저 문자로 알립니다.",
    "문자를 보내면 상담 담당자가 10분 안에 답합니다.",
    "도착 전에 문자로 한 번 더 알립니다.",
    "향이 부담스러우면 무향 오일로 진행합니다."
]

# 공통 CSS 
COMMON_CSS = """
:root{--mint:#48c8c0;--mint-d:#2aa9a1;--mint-l:#f3fbfa;--ink:#202020;--sub:#7d8387;--soft:#a0a4a4;--line:#e6e8ea;--gray:#f9f9f9;--fill:#f1f2f3}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;overflow-x:hidden}
body{background:#fff;color:var(--ink);font-family:"Pretendard Variable",system-ui,sans-serif;font-size:15.5px;line-height:1.75;word-break:keep-all;-webkit-font-smoothing:antialiased;}
a{color:inherit;text-decoration:none}
.wrap{width:min(90vw,640px);margin-inline:auto}
.serif{font-family:"Noto Serif KR",serif}
header.bar{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.bar .wrap{display:flex;align-items:center;justify-content:space-between;height:58px}
.logo{font-weight:800;font-size:17px;display:flex;align-items:center;gap:8px}
.logo b{width:9px;height:9px;border-radius:50%;background:var(--mint)}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 20px;border-radius:999px;font-weight:700;font-size:14.5px;background:var(--mint);color:#fff;transition:transform .15s}
.pill.lg{min-height:54px;padding:0 30px;font-size:16.5px}
.hero{text-align:center;padding:56px 0 30px}
.hero h1{font-size:clamp(27px,7.4vw,40px);line-height:1.3;font-weight:500;letter-spacing:-.03em}
.hero .lead{margin:16px auto 0;color:var(--sub);font-size:15px}
.hero .cta{display:flex;gap:10px;justify-content:center;margin-top:26px}
.sec{padding:50px 0 72px;text-align:center}
.sec.gray{background:var(--gray)}
h2{font-size:clamp(22px,6vw,30px);line-height:1.35;font-weight:500;letter-spacing:-.03em}
h2 em{font-style:normal;color:var(--mint-d)}
.sub{color:var(--sub);font-size:14.5px;margin-top:10px}
.companies-grid { display:grid; gap:12px; margin:26px auto 0; max-width:560px; text-align:left; grid-template-columns:1fr 1fr; }
.companies-grid a { background:#fff; border:1px solid var(--line); border-radius:14px; padding:20px 18px; display:block; transition:border-color .15s; }
.companies-grid a:hover { border-color:var(--mint); box-shadow:0 10px 22px -12px rgba(72,200,192,.4); }
.companies-grid h3 { font-size:16px; color:var(--ink); margin-bottom:4px; font-weight:800; }
.companies-grid p { font-size:15px; color:var(--mint-d); font-weight:700; }
.chat{list-style:none;margin:26px auto 0;max-width:520px;display:grid;gap:10px;text-align:left}
.chat li{max-width:86%;padding:12px 16px;border-radius:18px;font-size:14.5px;line-height:1.6;color:#3a3f43;background:var(--fill);border-bottom-left-radius:6px;justify-self:start}
.chat li.me{background:var(--mint-l);border:1px solid #cdeeeb;border-bottom-left-radius:18px;border-bottom-right-radius:6px;justify-self:end;color:var(--ink)}
.check{list-style:none;margin:26px auto 0;max-width:560px;text-align:left;display:grid;gap:10px}
.check li{position:relative;padding:14px 16px 14px 44px;background:#fff;border:1px solid var(--line);border-radius:12px;font-size:15px;font-weight:600}
.check li::before{content:"";position:absolute;left:16px;top:19px;width:7px;height:12px;border:solid var(--mint);border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.strip{display:grid;gap:12px;margin:26px auto 0;max-width:560px;text-align:left;grid-template-columns:1fr 1fr}
.strip figure{background:#fff;border-radius:16px;padding:20px 18px;border:1px solid var(--line);display:grid;gap:14px;align-content:space-between}
.strip blockquote{font-size:15px;line-height:1.7;color:#3a3f43}
.faq{display:grid;gap:12px;margin:26px auto 0;max-width:560px;text-align:left;grid-template-columns:1fr 1fr}
.faq div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 18px}
.faq .q{font-weight:800;font-size:15.5px;margin-bottom:8px}
.faq .a{color:var(--sub);font-size:14.5px}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:26px auto 0;max-width:560px}
.chips a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;background:#fff;border:1px solid var(--line);border-radius:999px;font-size:13.5px;font-weight:600;padding:4px 16px;transition:background .15s}
footer{background:#2b2f33;color:#fff;padding:40px 0 48px;text-align:center}
.fab{position:fixed;right:16px;bottom:18px;z-index:30;width:66px;height:66px;border-radius:50%;background:var(--mint);color:#fff;display:grid;place-items:center;text-align:center;font-size:12px;font-weight:800;line-height:1.2}
@media(max-width:480px) { .companies-grid, .strip, .faq { grid-template-columns:1fr; } }
"""

# 계층형 피라미드 링크
def get_hierarchical_chips(level, gu_key=None):
    chips = []
    if level == 'main':
        for g_key, g_info in seoul_data.items():
            chips.append(f'<a href="{base_url}/{quote(g_info["name"])}/">{g_info["name"]}</a>')
    elif level == 'gu' and gu_key:
        dongs = seoul_data[gu_key]['dongs']
        for dong in dongs:
            chips.append(f'<a href="{base_url}/{quote(dong)}/">{dong}</a>')
    elif level == 'dong' and gu_key:
        dongs = seoul_data[gu_key]['dongs']
        sample_size = min(3, len(dongs)) 
        sampled_dongs = random.sample(dongs, sample_size)
        for dong in sampled_dongs:
            chips.append(f'<a href="{base_url}/{quote(dong)}/">{dong}</a>')
    return "\n".join(chips)

# HTML 템플릿 엔진
def generate_html(location_name, url_path, level, gu_key=None):
    intro = random.choice(intro_phrases)
    chats = random.sample(chat_pool, min(2, len(chat_pool)))
    chat_html = "".join([f'<li><small>손님</small>{q}</li><li class="me"><small>{site_name}</small>{a}</li>' for q, a in chats])
    reviews = random.sample(review_pool, min(2, len(review_pool)))
    reviews_html = "".join([f'<figure><blockquote>{txt}</blockquote><figcaption><span><b>{name}</b><br>{course}</span></figcaption></figure>' for name, course, txt in reviews])
    faqs = random.sample(faq_pool, min(2, len(faq_pool)))
    faq_html = "".join([f'<div><p class="q">{q}</p><p class="a">{a}</p></div>' for q, a in faqs])
    rules = random.sample(rules_pool, min(2, len(rules_pool)))
    rules_html = "".join([f'<li>{r}</li>' for r in rules])
    
    sample_count = random.randint(3, 4)
    final_companies = random.sample(companies_data, sample_count)
    
    companies_html = ""
    json_ld_items = []
    for idx, comp in enumerate(final_companies, 1):
        companies_html += f'<a href="tel:{comp["tel"]}"><h3>{comp["name"]}</h3><p>{comp["tel"]}</p></a>\n'
        json_ld_items.append(f'{{"@type": "LocalBusiness", "position": {idx}, "name": "{comp["name"]}", "telephone": "{comp["tel"]}"}}')
    json_ld_str = ",\n        ".join(json_ld_items)

    # SEO 타이틀, 헤딩, 설명에서 '출장마사지' 키워드 완전히 제거
    if level == 'main':
        title = f"{site_name} | 프리미엄 스웨디시 홈테라피"
        desc = f"{site_name}에서 검증된 프리미엄 홈테라피 업체를 만나보세요."
        h1_text = "프리미엄 테라피<br>스웨디시 홈테라피"
        lead_text = f"씻을 기운조차 없는 날이 있죠. {site_name} 제휴 업체가 찾아갑니다."
        section_title = f"{site_name} 제휴 업체"
        chat_intro = f"{site_name} 고객님들이 주로 남기시는 문의입니다."
        chips_title = "지역 안내"
    else:
        title = f"{location_name} 프리미엄 테라피 | {site_name}"
        desc = f"{location_name} 지역에서 활동하는 {site_name}의 검증된 홈테라피 업체를 만나보세요."
        h1_text = f"{location_name} 프리미엄 테라피<br>스웨디시 홈케어"
        # 키워드(출장마사지)는 문장 내부(lead_text, chat_intro)에 자연스럽게 포함
        lead_text = random.choice(leads_sub).format(dong=location_name)
        section_title = f"{location_name} 제휴 업체"
        chat_intro = f"{intro} {location_name} 출장마사지를 찾는 분들이 주로 남기시는 문의입니다."
        chips_title = "주변 지역" if level == 'dong' else f"{location_name} 상세 지역"

    chips_html = get_hierarchical_chips(level, gu_key)

    section_blocks = [
        f'<section id="companies" class="sec gray"><div class="wrap"><h2 class="serif"><em>{section_title}</em></h2><div class="companies-grid">{companies_html}</div></div></section>',
        f'<section class="sec"><div class="wrap"><h2 class="serif"><em>이런 날</em> 이런 몸</h2><p class="sub">{chat_intro}</p><ul class="chat">{chat_html}</ul></div></section>',
        f'<section class="sec gray"><div class="wrap"><h2 class="serif"><em>받아 본 분들의</em> 리뷰</h2><div class="strip">{reviews_html}</div></div></section>',
        f'<section class="sec"><div class="wrap"><h2 class="serif"><em>지키는 것,</em> 하지 않는 것</h2><ul class="check">{rules_html}</ul></div></section>',
        f'<section class="sec gray"><div class="wrap"><h2 class="serif"><em>궁금한</em> 것부터</h2><div class="faq">{faq_html}</div></div></section>'
    ]
    random.shuffle(section_blocks)
    dynamic_dom_content = "\n".join(section_blocks)

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url_path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<script>
  document.addEventListener("DOMContentLoaded", function() {{
    const jsonLd = {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "url": "{url_path}",
      "name": document.title,
      "itemListElement": [
        {json_ld_str}
      ]
    }};
    const script = document.createElement('script');
    script.type = "application/ld+json";
    script.text = JSON.stringify(jsonLd);
    document.head.appendChild(script);
  }});
</script>
<style>{COMMON_CSS}</style>
</head>
<body class="root">
<header class="bar"><div class="wrap"><a class="logo" href="{base_url}/"><b></b>{site_name}</a><a class="pill" href="#companies">제휴 업체</a></div></header>

<section class="hero">
<div class="wrap">
<h1 class="serif">{h1_text}</h1>
<p class="lead">{lead_text}</p>
<div class="cta"><a class="pill lg" href="#companies">업체 바로보기</a></div>
</div>
</section>

{dynamic_dom_content}

<section class="sec"><div class="wrap"><h2 class="serif"><em>{chips_title}</em></h2>
<div class="chips">
{chips_html}
</div></div></section>

<footer>
<div class="wrap"><div class="logo" style="justify-content:center;color:#fff;font-size:19px;"><b></b>{site_name}</div><p style="color:#b8bcc0;font-size:14px;margin-top:10px;">프리미엄 테라피 안내</p></div>
</footer>
<a class="fab" href="#companies">업체<br>보기</a>
</body>
</html>
"""

sitemap_urls = [f"{base_url}/"]

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(generate_html("전지역", f"{base_url}/", level='main'))

for gu_key, gu_info in seoul_data.items():
    gu_name = gu_info['name']
    
    gu_folder = os.path.join(base_dir, gu_name)
    os.makedirs(gu_folder, exist_ok=True)
    gu_url = f"{base_url}/{quote(gu_name)}/"
    sitemap_urls.append(gu_url)
    
    with open(os.path.join(gu_folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_html(gu_name, gu_url, level='gu', gu_key=gu_key))
    
    for dong in gu_info['dongs']:
        dong_folder = os.path.join(base_dir, dong)
        os.makedirs(dong_folder, exist_ok=True)
        dong_url = f"{base_url}/{quote(dong)}/"
        sitemap_urls.append(dong_url)
        
        with open(os.path.join(dong_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_html(dong, dong_url, level='dong', gu_key=gu_key))

sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n"
sitemap_content += '</urlset>'

with open(os.path.join(base_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_content)

with open(os.path.join(base_dir, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n")