import urllib.request
import json
import os

def generate_svgs():
    print("Fetching GitHub stats for Heebu...")
    
    # 1. Fetch User Data
    try:
        u_req = urllib.request.Request('https://api.github.com/users/Heebu', headers={'User-Agent': 'Mozilla/5.0'})
        user = json.loads(urllib.request.urlopen(u_req, timeout=10).read())
        public_repos = user.get('public_repos', 57)
        followers = user.get('followers', 9)
    except Exception as e:
        print("User fetch fallback:", e)
        public_repos = 57
        followers = 9

    # 2. Fetch Commits
    try:
        c_req = urllib.request.Request('https://api.github.com/search/commits?q=author:Heebu', headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.cloak-preview'
        })
        commits_data = json.loads(urllib.request.urlopen(c_req, timeout=10).read())
        total_commits = commits_data.get('total_count', 310)
    except Exception as e:
        print("Commits fetch fallback:", e)
        total_commits = 310

    # 3. Fetch Repos for Stars and Languages
    try:
        repos = []
        page = 1
        while True:
            r_req = urllib.request.Request(f'https://api.github.com/users/Heebu/repos?per_page=100&page={page}', headers={'User-Agent': 'Mozilla/5.0'})
            batch = json.loads(urllib.request.urlopen(r_req, timeout=10).read())
            if not batch: break
            repos.extend(batch)
            page += 1
            if len(batch) < 100: break

        total_stars = sum(r.get('stargazers_count', 0) for r in repos)
        lang_counts = {}
        for r in repos:
            l = r.get('language')
            if l: lang_counts[l] = lang_counts.get(l, 0) + 1
    except Exception as e:
        print("Repos fetch fallback:", e)
        total_stars = 4
        lang_counts = {'Dart': 25, 'C++': 10, 'JavaScript': 7, 'HTML': 2, 'CSS': 1}

    # Format language percentages
    total_lang_repos = sum(lang_counts.values()) or 1
    dart_pct = round((lang_counts.get('Dart', 25) / total_lang_repos) * 100, 1)
    cpp_pct = round((lang_counts.get('C++', 10) / total_lang_repos) * 100, 1)
    js_pct = round(((lang_counts.get('JavaScript', 7) + lang_counts.get('TypeScript', 0)) / total_lang_repos) * 100, 1)
    web_pct = round(((lang_counts.get('HTML', 2) + lang_counts.get('CSS', 1)) / total_lang_repos) * 100, 1)
    other_pct = round(100 - (dart_pct + cpp_pct + js_pct + web_pct), 1)
    if other_pct < 0: other_pct = 2.0

    print(f"Stats: Commits={total_commits}, Repos={public_repos}, Stars={total_stars}, Followers={followers}")
    print(f"Langs: Dart={dart_pct}%, C++={cpp_pct}%, JS/TS={js_pct}%, Web={web_pct}%, Other={other_pct}%")

    # SVG 1: Quantum Telemetry Overview Card
    stats_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 235" width="460" height="235" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="460" y2="235" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#080C1A"/>
      <stop offset="100%" stop-color="#04060D"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#7000FF"/>
    </linearGradient>
    <linearGradient id="borderGrad" x1="0" y1="0" x2="460" y2="235" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#7928CA" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#00FF9D" stop-opacity="0.7"/>
    </linearGradient>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <style>
    .title {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 700; fill: #00F0FF; letter-spacing: 2px; }}
    .subtext {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; fill: #94A3B8; font-weight: 500; }}
    .metric-val {{ font-family: 'Fira Code', monospace; font-size: 20px; font-weight: 800; fill: #FFFFFF; }}
    .metric-lbl {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 11px; fill: #64748B; text-transform: uppercase; letter-spacing: 1px; }}
    .badge-text {{ font-family: 'Fira Code', monospace; font-size: 10px; fill: #00FF9D; font-weight: 700; }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="456" height="231" rx="12" fill="url(#bgGrad)"/>
  <rect x="2" y="2" width="456" height="231" rx="12" stroke="url(#borderGrad)" stroke-width="1.5"/>

  <!-- Tech Grid Background Pattern -->
  <g opacity="0.07" stroke="#00F0FF" stroke-width="0.5">
    <line x1="20" y1="45" x2="440" y2="45"/>
    <line x1="20" y1="125" x2="440" y2="125"/>
    <line x1="230" y1="45" x2="230" y2="215"/>
  </g>

  <!-- Header Section -->
  <circle cx="22" cy="24" r="4" fill="#00FF9D" filter="url(#neonGlow)">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="35" y="28" class="title">// QUANTUM TELEMETRY</text>
  <text x="340" y="27" class="badge-text">STATUS: ACTIVE</text>

  <!-- Corner Brackets -->
  <path d="M 8 16 L 8 8 L 16 8" stroke="#00F0FF" stroke-width="2" fill="none"/>
  <path d="M 452 16 L 452 8 L 444 8" stroke="#00F0FF" stroke-width="2" fill="none"/>
  <path d="M 8 219 L 8 227 L 16 227" stroke="#00F0FF" stroke-width="2" fill="none"/>
  <path d="M 452 219 L 452 227 L 444 227" stroke="#00F0FF" stroke-width="2" fill="none"/>

  <!-- Metric 1: Total Commits -->
  <g transform="translate(25, 55)">
    <rect x="0" y="0" width="190" height="65" rx="8" fill="#0E1528" stroke="#1E293B" stroke-width="1"/>
    <circle cx="18" cy="22" r="5" fill="#00F0FF"/>
    <text x="30" y="26" class="metric-lbl">TOTAL COMMITS</text>
    <text x="18" y="52" class="metric-val" fill="#00F0FF">{total_commits}+</text>
  </g>

  <!-- Metric 2: Public Repositories -->
  <g transform="translate(240, 55)">
    <rect x="0" y="0" width="190" height="65" rx="8" fill="#0E1528" stroke="#1E293B" stroke-width="1"/>
    <circle cx="18" cy="22" r="5" fill="#A855F7"/>
    <text x="30" y="26" class="metric-lbl">PUBLIC REPOSITORIES</text>
    <text x="18" y="52" class="metric-val" fill="#A855F7">{public_repos}</text>
  </g>

  <!-- Metric 3: Stars & Recognition -->
  <g transform="translate(25, 135)">
    <rect x="0" y="0" width="190" height="65" rx="8" fill="#0E1528" stroke="#1E293B" stroke-width="1"/>
    <circle cx="18" cy="22" r="5" fill="#00FF9D"/>
    <text x="30" y="26" class="metric-lbl">TOTAL STARS EARNED</text>
    <text x="18" y="52" class="metric-val" fill="#00FF9D">{total_stars} ★</text>
  </g>

  <!-- Metric 4: Followers / Network -->
  <g transform="translate(240, 135)">
    <rect x="0" y="0" width="190" height="65" rx="8" fill="#0E1528" stroke="#1E293B" stroke-width="1"/>
    <circle cx="18" cy="22" r="5" fill="#F59E0B"/>
    <text x="30" y="26" class="metric-lbl">NETWORK FOLLOWERS</text>
    <text x="18" y="52" class="metric-val" fill="#F59E0B">{followers}</text>
  </g>

  <!-- Bottom Terminal Tag -->
  <text x="25" y="222" class="subtext">RUNTIME: FLUTTER // DART CORE // LAGOS SECTOR 01</text>
  <text x="375" y="222" class="subtext">HEEBU_PRIME</text>
</svg>'''

    # SVG 2: Quantum Core Languages Matrix
    langs_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 235" width="460" height="235" fill="none">
  <defs>
    <linearGradient id="bgGrad2" x1="0" y1="0" x2="460" y2="235" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#080C1A"/>
      <stop offset="100%" stop-color="#04060D"/>
    </linearGradient>
    <linearGradient id="borderGrad2" x1="0" y1="0" x2="460" y2="235" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7928CA" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#00F0FF" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#FF007F" stop-opacity="0.7"/>
    </linearGradient>
    <linearGradient id="dartGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#02569B"/>
    </linearGradient>
    <linearGradient id="cppGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#A855F7"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
    <linearGradient id="jsGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00FF9D"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="webGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="otherGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <filter id="neonGlow2" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <style>
    .title {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 700; fill: #A855F7; letter-spacing: 2px; }}
    .lang-lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 600; fill: #E2E8F0; }}
    .lang-pct {{ font-family: 'Fira Code', monospace; font-size: 12px; font-weight: 700; fill: #94A3B8; text-anchor: end; }}
    .bar-bg {{ fill: #0E1528; rx: 4; }}
    .bar-fill {{ rx: 4; }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="456" height="231" rx="12" fill="url(#bgGrad2)"/>
  <rect x="2" y="2" width="456" height="231" rx="12" stroke="url(#borderGrad2)" stroke-width="1.5"/>

  <!-- Corner Brackets -->
  <path d="M 8 16 L 8 8 L 16 8" stroke="#A855F7" stroke-width="2" fill="none"/>
  <path d="M 452 16 L 452 8 L 444 8" stroke="#A855F7" stroke-width="2" fill="none"/>
  <path d="M 8 219 L 8 227 L 16 227" stroke="#A855F7" stroke-width="2" fill="none"/>
  <path d="M 452 219 L 452 227 L 444 227" stroke="#A855F7" stroke-width="2" fill="none"/>

  <!-- Header Section -->
  <circle cx="22" cy="24" r="4" fill="#A855F7" filter="url(#neonGlow2)">
    <animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="35" y="28" class="title">// LANGUAGE MATRIX</text>
  <text x="430" y="27" style="font-family:'Fira Code'; font-size:10px; fill:#00F0FF; text-anchor:end; font-weight:700;">DOMINANT: DART</text>

  <!-- Language 1: Dart -->
  <g transform="translate(25, 48)">
    <circle cx="4" cy="5" r="4" fill="#00F0FF"/>
    <text x="16" y="9" class="lang-lbl">Dart (Flutter Engine)</text>
    <text x="405" y="9" class="lang-pct" fill="#00F0FF">{dart_pct}%</text>
    <rect x="0" y="16" width="410" height="8" class="bar-bg"/>
    <rect x="0" y="16" width="{int(410 * (dart_pct / 100))}" height="8" fill="url(#dartGrad)" class="bar-fill"/>
  </g>

  <!-- Language 2: C++ -->
  <g transform="translate(25, 84)">
    <circle cx="4" cy="5" r="4" fill="#A855F7"/>
    <text x="16" y="9" class="lang-lbl">C++ (Systems Core)</text>
    <text x="405" y="9" class="lang-pct" fill="#A855F7">{cpp_pct}%</text>
    <rect x="0" y="16" width="410" height="8" class="bar-bg"/>
    <rect x="0" y="16" width="{int(410 * (cpp_pct / 100))}" height="8" fill="url(#cppGrad)" class="bar-fill"/>
  </g>

  <!-- Language 3: JavaScript / TypeScript -->
  <g transform="translate(25, 120)">
    <circle cx="4" cy="5" r="4" fill="#00FF9D"/>
    <text x="16" y="9" class="lang-lbl">JavaScript / TypeScript</text>
    <text x="405" y="9" class="lang-pct" fill="#00FF9D">{js_pct}%</text>
    <rect x="0" y="16" width="410" height="8" class="bar-bg"/>
    <rect x="0" y="16" width="{int(410 * (js_pct / 100))}" height="8" fill="url(#jsGrad)" class="bar-fill"/>
  </g>

  <!-- Language 4: Modern Web (HTML/CSS) -->
  <g transform="translate(25, 156)">
    <circle cx="4" cy="5" r="4" fill="#F59E0B"/>
    <text x="16" y="9" class="lang-lbl">HTML5 / CSS3 / Web UI</text>
    <text x="405" y="9" class="lang-pct" fill="#F59E0B">{web_pct}%</text>
    <rect x="0" y="16" width="410" height="8" class="bar-bg"/>
    <rect x="0" y="16" width="{int(410 * (web_pct / 100))}" height="8" fill="url(#webGrad)" class="bar-fill"/>
  </g>

  <!-- Language 5: Tooling & Systems -->
  <g transform="translate(25, 192)">
    <circle cx="4" cy="5" r="4" fill="#38BDF8"/>
    <text x="16" y="9" class="lang-lbl">Build &amp; System Scripts (CMake / Shell)</text>
    <text x="405" y="9" class="lang-pct" fill="#38BDF8">{other_pct}%</text>
    <rect x="0" y="16" width="410" height="8" class="bar-bg"/>
    <rect x="0" y="16" width="{int(410 * (other_pct / 100))}" height="8" fill="url(#otherGrad)" class="bar-fill"/>
  </g>
</svg>'''

    # Ensure assets dir exists
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(out_dir, exist_ok=True)
    
    stats_path = os.path.join(out_dir, 'quantum_stats.svg')
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(stats_svg)
    print(f"Written: {stats_path}")

    langs_path = os.path.join(out_dir, 'quantum_languages.svg')
    with open(langs_path, 'w', encoding='utf-8') as f:
        f.write(langs_svg)
    print(f"Written: {langs_path}")

if __name__ == '__main__':
    generate_svgs()
