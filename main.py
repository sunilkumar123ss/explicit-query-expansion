"""Inspectable one-hop query expansion with exact token-sequence rules."""
import argparse
import json
from pathlib import Path
import re


def tokens(text):return re.findall(r"\w+",text.casefold())


def expand(query,rules,limit=8):
    if not isinstance(query,str):raise ValueError("query must be a string")
    if isinstance(limit,bool) or not isinstance(limit,int) or not 0 <= limit <= 100:raise ValueError("limit must be an integer in [0,100]")
    if not isinstance(rules,dict):raise ValueError("rules must map phrases to alias lists")
    normalized=[];seen_rules=set()
    for phrase,aliases in rules.items():
        if not isinstance(phrase,str) or not tokens(phrase) or not isinstance(aliases,list) or any(not isinstance(x,str) or not tokens(x) for x in aliases):
            raise ValueError("rules require nonempty tokenizable phrases and string aliases")
        key=tuple(tokens(phrase))
        if key in seen_rules:raise ValueError("rules normalize to duplicate phrases")
        seen_rules.add(key);normalized.append((key,aliases))
    query_tokens=tokens(query)
    original=list(dict.fromkeys(query_tokens))
    additions=[];seen=set(original)
    for key,aliases in sorted(normalized,key=lambda row:(-len(row[0]),row[0])):
        if not any(tuple(query_tokens[i:i+len(key)]) == key for i in range(len(query_tokens)-len(key)+1)):
            continue
        for alias in aliases:
            normalized_alias=" ".join(tokens(alias))
            if normalized_alias in seen or len(additions) >= limit:continue
            seen.add(normalized_alias)
            additions.append({"term":normalized_alias,"weight":0.5,"rule":" ".join(key)})
    return {"query":query,"original":[{"term":term,"weight":1.0} for term in original],
            "expansions":additions,"strategy":"reviewed lexical rules; one hop"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query",nargs="?",default="voice RAG latency")
    parser.add_argument("--rules",type=Path,default=Path(__file__).with_name("rules.json"))
    parser.add_argument("--limit",type=int,default=8)
    args=parser.parse_args()
    try:result=expand(args.query,json.loads(args.rules.read_text()),args.limit)
    except (ValueError,OSError,TypeError) as exc:parser.error(str(exc))
    print(json.dumps(result,indent=2))

if __name__ == "__main__":main()
