#!/usr/bin/env python3
"""
panlink.py — tidy up Baidu Pan / Quark Pan share links pasted from forums and chats.

Chinese share posts rarely contain a clean URL. They look like:

    链接: https://pan.baidu.com/s/1AbCdEfGhIjKlMnOpQrStUv 提取码: ab12
    --来自百度网盘超级会员v5的分享

This script finds the share link in any pasted text, pulls out the extraction code
(提取码 / 密码 / ?pwd=) and prints one canonical link per share, so you can copy it
cleanly into a download tool or a message. It does not talk to Baidu or Quark at all.

Usage:
    python panlink.py "链接: https://pan.baidu.com/s/1AbC… 提取码: ab12"
    echo "<pasted text>" | python panlink.py
    python panlink.py --json < links.txt
"""
import json
import re
import sys

BAIDU_HOSTS = r"(?:pan|yun|eyun)\.baidu\.com"

# share id: starts with 1, 22-23 chars; older short ids exist too
_BAIDU_S = re.compile(r"https?://" + BAIDU_HOSTS + r"/s/(1?[0-9A-Za-z_-]{5,30})", re.I)
_BAIDU_INIT = re.compile(r"https?://" + BAIDU_HOSTS + r"/share/init\?surl=([0-9A-Za-z_-]{5,30})", re.I)
_BAIDU_WAP = re.compile(r"https?://" + BAIDU_HOSTS + r"/wap/init\?surl=([0-9A-Za-z_-]{5,30})", re.I)
_QUARK = re.compile(r"https?://pan\.quark\.cn/s/([0-9a-f]{12,32})", re.I)

_PWD_IN_URL = re.compile(r"[?&#](?:pwd|password|code)=([0-9A-Za-z]{4})\b")
# "提取码: ab12", "密码：ab12", "pwd ab12", "code: AB12" — 4 chars, letters/digits
_PWD_IN_TEXT = re.compile(r"(?:提取码|访问码|密码|提取密码|pwd|password|code)\s*[:：=]?\s*([0-9A-Za-z]{4})(?![0-9A-Za-z])", re.I)
_PATH = re.compile(r"#list/path=([^\s&]+)")


def parse(text: str) -> list[dict]:
    """Return one dict per share found in `text`: {cloud, id, pwd, path, url}."""
    out, seen = [], set()
    matches = []
    for cloud, rx in (("baidu", _BAIDU_S), ("baidu", _BAIDU_INIT), ("baidu", _BAIDU_WAP), ("quark", _QUARK)):
        for m in rx.finditer(text):
            matches.append((m.start(), m.end(), cloud, m.group(1)))
    matches.sort()
    for i, (start, end, cloud, sid) in enumerate(matches):
        # Baidu's "/s/1xxxx" and "surl=xxxx" are the same share: surl omits the leading "1"
        if cloud == "baidu" and not sid.startswith("1") and len(sid) >= 22:
            sid = "1" + sid
        key = (cloud, sid)
        if key in seen:
            continue
        seen.add(key)
        # the code is looked for right after this link, before the next one
        window_end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        tail = text[end:window_end]
        pwd = None
        m = _PWD_IN_URL.match(tail) or _PWD_IN_URL.search(text[end:end + 40])
        if m:
            pwd = m.group(1)
        else:
            m = _PWD_IN_TEXT.search(tail)
            if m:
                pwd = m.group(1)
        path = None
        m = _PATH.search(tail[:200])
        if m:
            path = m.group(1)
        if cloud == "baidu":
            url = f"https://pan.baidu.com/s/{sid}" + (f"?pwd={pwd}" if pwd else "")
        else:
            url = f"https://pan.quark.cn/s/{sid}" + (f"?pwd={pwd}" if pwd else "")
        out.append({"cloud": cloud, "id": sid, "pwd": pwd, "path": path, "url": url})
    return out


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    text = " ".join(args) if args else sys.stdin.read()
    found = parse(text)
    if not found:
        print("no Baidu / Quark share link found", file=sys.stderr)
        return 1
    if as_json:
        print(json.dumps(found, ensure_ascii=False, indent=2))
    else:
        for f in found:
            line = f["url"]
            if f["path"]:
                line += f"   (folder: {f['path']})"
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
