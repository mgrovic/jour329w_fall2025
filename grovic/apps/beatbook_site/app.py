import os, csv, re, json
from pathlib import Path
from collections import defaultdict, Counter
from flask import Flask, render_template, request, abort, jsonify
import requests  # add for Groq API

BASE = Path("/workspaces/jour329w_fall2025")
CSV_PATH = BASE / "grovic" / "stardem_nearly_final" / "people_md_de_va.csv"
MD_INPUT = BASE / "beatbook_revised.md"

EMAIL_RE = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b')
PHONE_RE = re.compile(r'''
    (?<!\w)
    (?:\+?\d{1,3}[\s.\-]?)?
    (?:\(?\d{3}\)?[\s.\-]?)
    \d{3}[\s.\-]?\d{4}
    (?:\s*(?:ext|x|\#)\s*\d{1,6})?
    (?!\w)
''', re.VERBOSE)
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\((?:https?:\/\/|mailto:)[^\)]+\)')
URL_RE = re.compile(r'\bhttps?:\/\/\S+\b')

def clean_ws(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()

def strip_contacts(text: str) -> str:
    text = MD_LINK_RE.sub(r'\1', text)
    text = URL_RE.sub('', text)
    text = EMAIL_RE.sub('', text)
    text = PHONE_RE.sub('', text)
    text = re.sub(r'\(\s*\)', '', text)
    return clean_ws(text)

def normalize_name(name: str) -> str:
    return re.sub(r'\s+', ' ', name.strip().lower())

def letter_signature(name: str) -> str:
    # Collapse scrambled inputs like "son ColdenAlli" to same bucket as "Allison Colden"
    letters = re.findall(r'[a-z]', name.lower())
    return ''.join(sorted(letters))

def to_sentence_case(s: str) -> str:
    if not s: return s
    s = s.strip()
    s = s.replace('—', '-')
    s = re.sub(r'\s+', ' ', s)
    acronyms = {'cbf','dnr','md','us','epa','noaa','asmfc'}
    words = s.split(' ')
    fixed = []
    for w in words:
        wl = w.lower().strip(".,'")
        if wl in acronyms:
            fixed.append(w.upper())
        else:
            fixed.append(w.capitalize())
    out = ' '.join(fixed)
    out = out.replace("Foundation's", "Foundation")
    out = out.replace(" Md ", " MD ")
    out = out.replace(" Md.", " MD")
    return out.strip()

def load_people(csv_path: Path):
    by_sig = defaultdict(list)
    if not csv_path.exists():
        return {}, {}
    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_raw = (row.get('name') or row.get('Name') or row.get('ame') or '').strip()
            if not name_raw:
                continue
            title_raw = (row.get('title') or row.get('Title') or '').strip()
            cat = (row.get('category') or row.get('Category') or '').strip()
            disp = clean_ws(name_raw)
            norm = normalize_name(disp)
            sig = letter_signature(disp)
            by_sig[sig].append({'disp': disp, 'norm': norm, 'title': clean_ws(title_raw), 'cat': cat})
    sig_to_canon = {}
    for sig, items in by_sig.items():
        counts = Counter(i['norm'] for i in items)
        best_norm = max(counts.items(), key=lambda x: (x[1], len(x[0])))[0]
        candidates = [i['disp'] for i in items if i['norm'] == best_norm]
        best_disp = max(candidates, key=len) if candidates else max([i['disp'] for i in items], key=len)
        best_disp_clean = ' '.join(w.capitalize() for w in best_disp.split())
        sig_to_canon[sig] = {'display_name': best_disp_clean, 'norm': best_norm}
    people = {}
    categories = defaultdict(list)
    cat_seen = defaultdict(set)
    for sig, items in by_sig.items():
        canon = sig_to_canon[sig]
        disp = canon['display_name']
        norm = canon['norm']
        titles = [i['title'] for i in items if i['title']]
        best_title = to_sentence_case(max(titles, key=len)) if titles else ''
        first_cat = next((i['cat'] for i in items if i['cat']), '')
        people[norm] = {'display_name': disp, 'title': best_title, 'category': first_cat}
        if first_cat and disp not in cat_seen[first_cat]:
            categories[first_cat].append((disp, best_title))
            cat_seen[first_cat].add(disp)
    for c in categories:
        categories[c].sort(key=lambda x: x[0].split()[-1].lower())
    return people, categories

def load_markdown(md_path: Path):
    if not md_path.exists():
        return ""
    text = md_path.read_text(encoding='utf-8')
    lines = [strip_contacts(ln) for ln in text.splitlines()]
    return "\n".join(lines)

def extract_entities(people_map, text):
    orgs = Counter()
    places = Counter()
    org_patterns = [
        r'\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z&\-]+){1,5}\b',
        r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})*\b',
    ]
    place_patterns = [
        r'\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\s+(County|River|Bay|City|Town|Park|State|Creek|Harbor)\b'
    ]
    for ln in text.splitlines():
        for pat in org_patterns:
            for m in re.findall(pat, ln):
                if len(m.split()) >= 2:
                    orgs[m] += 1
        for pat in place_patterns:
            for m in re.findall(pat, ln):
                places[m] += 1
    people_index = {p['display_name']: p for p in people_map.values()}
    org_index = {name: {'name': name, 'count': cnt} for name, cnt in orgs.items()}
    place_index = {name: {'name': name, 'count': cnt} for name, cnt in places.items()}
    return people_index, org_index, place_index

def find_context_for_name(name, text, max_lines=6):
    name_norm = normalize_name(name)
    matched = []
    for ln in text.splitlines():
        if normalize_name(ln).find(name_norm) != -1:
            if ln.strip():
                matched.append(ln.strip())
    return "\n".join(matched[:max_lines])

def groq_expand(name: str, title: str, context: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Additional details unavailable: set GROQ_API_KEY."
    try:
        url = "https://api.groq.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        prompt = f"""Provide concise factual bullets (4-6) about this person.
Use only public, widely cited info; avoid speculation and contact details.
Focus: role, notable work, affiliations, Bay/Eastern Shore relevance.

Name: {name}
Title: {title}

Local context snippets:
{context}
"""
        body = {
            "model": "maverick",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 400,
        }
        resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=15)
        if resp.status_code != 200:
            return f"GROQ error {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return text or "No additional details returned."
    except Exception as e:
        return f"GROQ request failed: {e}"

app = Flask(__name__)
PEOPLE_MAP, PEOPLE_BY_CAT = load_people(CSV_PATH)
TEXT = load_markdown(MD_INPUT)
PEOPLE_IDX, ORG_IDX, PLACE_IDX = extract_entities(PEOPLE_MAP, TEXT)
ALL_DISPLAY_NAMES = [p['display_name'] for p in PEOPLE_MAP.values()]
ALL_DISPLAY_NAMES.sort()

@app.route("/")
def index():
    return render_template(
        "index.html",
        people_by_cat=PEOPLE_BY_CAT,
        orgs=sorted(ORG_IDX.items(), key=lambda x: -x[1]['count'])[:50],
        places=sorted(PLACE_IDX.items(), key=lambda x: -x[1]['count'])[:50],
        all_names=ALL_DISPLAY_NAMES,
    )

@app.route("/entity")
def entity():
    name = request.args.get("name", "").strip()
    kind = request.args.get("kind", "Person")
    if not name:
        abort(400)
    person_data = PEOPLE_MAP.get(normalize_name(name)) if kind == "Person" else None
    disp = person_data["display_name"] if person_data else name
    ctx = find_context_for_name(disp, TEXT, max_lines=8)
    title = person_data["title"] if person_data else ""
    more = groq_expand(disp, title, ctx)
    return render_template("entity.html", name=disp, kind=kind, title=title, context=ctx, more_info=more)

@app.route("/entity.json")
def entity_json():
    name = request.args.get("name", "").strip()
    if not name:
        abort(400)
    person_data = PEOPLE_MAP.get(normalize_name(name))
    if not person_data:
        title = ""
        ctx = find_context_for_name(name, TEXT, max_lines=6)
        more = groq_expand(name, title, ctx)
        return jsonify({"name": name, "title": title, "context": ctx, "more_info": more})
    disp = person_data["display_name"]
    title = person_data["title"]
    ctx = find_context_for_name(disp, TEXT, max_lines=6)
    more = groq_expand(disp, title, ctx)
    return jsonify({"name": disp, "title": title, "context": ctx, "more_info": more})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=True)
