"""
make_real_samples.py
────────────────────
Create data/real_samples_9000.csv containing 9 000 legitimate job
postings from fake_job_postings.csv with the `company_profile` column
reduced to a concise company name so it matches your fake‑jobs dataset.

Run (inside your venv):
    python make_real_samples.py
"""

import re
from pathlib import Path
import pandas as pd

# ─── Config ──────────────────────────────────────────────────────────
RAW_PATH  = Path("data/raw/fake_job_postings.csv")   # source EMSCAD CSV
OUT_PATH  = Path("data/real_samples.csv")       # output file
N_SAMPLES = 9_000                                    # desired sample size
SEED      = 42
# ─────────────────────────────────────────────────────────────────────

# 1) Load and normalise headers
df = pd.read_csv(RAW_PATH, low_memory=False)
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(' ', '_')
)

# 2) Keep only legitimate postings
df_real = df[df["fraudulent"] == 0].copy()

# ─── Regex helpers & extractor ───────────────────────────────────────
STOP_VERBS   = r'\b(is|are|was|were|has|have|helps|offers|makes|' \
               r'provides|creates|supplies)\b'
LEGAL_SUFFIX = r'\b(inc|inc\.|llc|ltd|ltd\.?|corp|corporation|' \
               r'group|solutions|systems|company)\b'
URL_TOKEN    = re.compile(r'#URL_[^#]+#', re.I)
PUNCT_SPLIT  = re.compile(r'[\r\n.;]')
CAP_WORD     = re.compile(r'\b[A-Z][a-zA-Z]{1,}\b')

LEADING_STOP = re.compile(
    r'^(we|our|the|a|an|established|welcome|thanks|only|as|'
    r'provide|provides|providing|growing|founded|at|based)\b',
    re.I
)

VERB_PHRASE = re.compile(
    r'\b(enable|enables|want|provide|provides|help|helps)\b',
    re.I
)

BAD_START = re.compile(              # final sweep for leftovers
    r'^(we|our|provide|provides|providing|growing|based|at|thanks|welcome)\b',
    re.I
)

def extract_company_name(profile: str, title: str) -> str:
    """Return a concise company name; fallback to '<3 title words> Inc.'."""
    txt = str(profile) if pd.notna(profile) else ""
    txt = (
        URL_TOKEN.sub(" ", txt)            # remove #URL_…#
        .replace('â€™', '’')               # fix mojibake
        .replace('â€“', '-')               # fix dashes
        .strip(' "\'')
    )

    # First chunk before punctuation / newline
    txt = PUNCT_SPLIT.split(txt, maxsplit=1)[0]

    # Drop leading filler words
    txt = LEADING_STOP.sub("", txt, count=1).strip()

    # Cut at first common verb ("is", "provides", …)
    txt = re.split(STOP_VERBS, txt, maxsplit=1, flags=re.I)[0].strip()

    # Collapse multiple spaces
    txt = re.sub(r'\s{2,}', ' ', txt)

    # ── Guards ──────────────────────────────────────────────────────
    if txt and txt[0].islower():
        txt = ""                               # sentence fragment
    else:
        if txt and not CAP_WORD.search(" ".join(txt.split()[:3])):
            txt = ""                           # no capitalised word
        first5 = " ".join(txt.split()[:5])
        if VERB_PHRASE.search(first5):
            txt = ""                           # still looks like a sentence

    # Trim overly long names lacking legal suffix
    words = txt.split()
    if len(words) > 5 and not re.search(LEGAL_SUFFIX, txt, re.I):
        txt = " ".join(words[:4])

    # Fallback
    if not txt:
        stub = " ".join(str(title).split()[:3]).strip()
        txt = f"{stub} Inc." if stub else "Unknown Inc."

    return txt

# 3) Extract / clean company names
df_real["company_profile"] = df_real.apply(
    lambda row: extract_company_name(row.get("company_profile", ""),
                                     row.get("title", "")),
    axis=1
)

# 4) Final sweep: replace any residual bad‑start strings with fallback
mask_bad = df_real["company_profile"].str.match(BAD_START, na=False)
df_real.loc[mask_bad, "company_profile"] = df_real.loc[mask_bad, "title"] \
    .apply(lambda t: f"{' '.join(str(t).split()[:3]).strip()} Inc." or "Unknown Inc.")

# 5) Remove duplicate company names to increase diversity
df_real = df_real.drop_duplicates(subset="company_profile")

# 6) Sample N_SAMPLES rows (or keep all if fewer)
df_sampled = (
    df_real if len(df_real) <= N_SAMPLES
    else df_real.sample(n=N_SAMPLES, random_state=SEED)
)

# 7) Ensure required column order / padding
wanted_cols = [
    "title", "description", "requirements", "company_profile",
    "location", "salary_range", "employment_type",
    "industry", "benefits", "fraudulent"
]
for col in wanted_cols:
    if col not in df_sampled.columns:
        df_sampled[col] = ""
df_sampled = df_sampled[wanted_cols]

# 8) Save
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df_sampled.to_csv(OUT_PATH, index=False)
print(f"✔  Saved {len(df_sampled)} clean real postings → {OUT_PATH}")
