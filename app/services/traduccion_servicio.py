import re, os
import deepl
from dotenv import load_dotenv

load_dotenv()
AUTH_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(AUTH_KEY)

def find_dnt_spans(text):
    dnt = re.findall(r'(["\'])(.+?)\1', text)
    spans = [m[1] for m in dnt]
    whitelist = [
        "Call of Duty", "Black Ops II", "Tom Clancy's Rainbow Six Siege", "Skyscraper",
        "The Big Bang Theory", "World of Warcraft", "Pokémon", "Overwatch League",
        "Hobo with a Shotgun", "Panic! At the Disco", "The Beatles", "Frank Ocean",
        "RuneScape", "Harry Potter", "South Park", "Golden Master", "Super Mario Bros.",
        "Neil Hamburger", "The Walking Dead", "Zelda", "Ernő Rubik", "Super Smash Bros.",
        "San Diego Comic-Con", "Dead Rising", "Falcon Heavy", "Overlord",
        "Mario & Sonic at the Olympic Games", "Slipknot", "Muse",
        "Donkey Kong Country", "Homestuck", "M1911", "Commando", "Pompeii"
    ]
    for w in whitelist:
        if w in text:
            spans.append(w)
    for m in re.finditer(r'\b(?:[A-Z][\w\.'+"'"+r"]+\s+){1,}[A-Z][\w\.'"+r"]+\b", text):
        spans.append(m.group(0))
    seen, result = set(), []
    for s in spans:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result

def mask(text, spans):
    for i, s in enumerate(spans, start=1):
        text = text.replace(s, f"[[DNT_{i:03d}]]")
    return text

def translate_with_deepl(text):
    spans = find_dnt_spans(text)
    masked = mask(text, spans)
    html = masked
    for i, s in enumerate(spans, start=1):
        html = html.replace(f"[[DNT_{i:03d}]]", f"<keep>{s}</keep>")
    result = translator.translate_text(
        html, target_lang="ES",
        tag_handling="html", ignore_tags=["keep"],
        preserve_formatting=True
    )
    out = re.sub(r'</?keep>', '', result.text)
    return out
