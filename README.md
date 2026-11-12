# Baidu Pan (pan.baidu.com) link reference — formats, extraction codes, and downloading outside China

A small reference for people who keep running into `pan.baidu.com` links on Chinese forums, Bilibili, Zhihu, mod sites and course pages, and cannot get the file out. Covers how the links are built, what the Chinese text around them means, and the realistic way to download in 2026 if you have no Baidu account. Quark Pan (`pan.quark.cn`), the second most common host, is covered in the same way.

Includes `panlink.py`, a tiny dependency-free script that cleans up pasted share text into a canonical link with the extraction code attached. It does not contact Baidu or Quark.

> Disclosure: I run [BaiduFast](https://baidufast.com/?utm_source=github-repo), a paid link-to-download service that is mentioned at the end. The reference part is plain public information about Baidu and Quark.

## Anatomy of a Baidu Pan share

```
链接：https://pan.baidu.com/s/1AbCdEfGhIjKlMnOpQrStUv?pwd=ab12
提取码：ab12
--来自百度网盘超级会员V5的分享
```

| Piece | Meaning |
|---|---|
| `链接` | "link" |
| `/s/1AbCd…` | the share ID. Case matters: `1AbCd` and `1abcd` are different shares |
| `?pwd=ab12` | the extraction code embedded in the URL (newer shares) |
| `提取码：ab12` | the same code written out (older shares, or both) |
| `--来自百度网盘超级会员V5的分享` | "shared from a Baidu Netdisk SVIP v5 member", decoration only |
| `#list/path=/Mods` | optional: opens a sub-folder of the share |

Other spellings of the same link you will meet:

| Form | Note |
|---|---|
| `https://pan.baidu.com/share/init?surl=AbCdEfGhIjKlMnOpQrStUv` | `surl` is the share ID without the leading `1` |
| `https://pan.baidu.com/wap/init?surl=…` | mobile page |
| `https://yun.baidu.com/s/…`, `https://eyun.baidu.com/…` | old domains, still redirect |
| `https://pan.baidu.com/share/link?shareid=…&uk=…` | very old; usually dead by now |

The extraction code (提取码, sometimes 密码 or 访问码) is 4 characters, letters and digits, case-sensitive. Without it the share page shows `请输入提取码`; with a wrong one, `提取码错误`.

## Anatomy of a Quark Pan share

```
https://pan.quark.cn/s/0123456789ab?pwd=abcd
「文件夹名」链接：https://pan.quark.cn/s/0123456789ab  提取码：abcd
```

Quark IDs are lowercase hex (12–32 characters). The code works the same way as Baidu's. Quark folders show **0 bytes** on the share page even when they hold gigabytes, so do not trust the size shown there.

## What the share page is telling you

| Chinese | English |
|---|---|
| 请输入提取码 | enter the extraction code |
| 提取码错误 | wrong code |
| 啊哦，你来晚了，分享的文件已经被取消了 | too late, the share was cancelled |
| 分享的文件已经被删除了 | the file was deleted |
| 此链接分享内容可能因为涉及侵权…无法访问 | blocked by Baidu, nobody can open it |
| 请登录后下载 | log in to download |
| 请下载客户端 | use the desktop client |
| 下载速度慢？开通超级会员 | "slow? buy SVIP" — the free-account throttle |

The last three are the ones foreigners actually hit, and they are not errors: Baidu requires a logged-in account for every download, the account needs a mainland (+86) phone number, and a free account is capped at a few dozen KB/s.

## `panlink.py` — clean up pasted links

```
$ python panlink.py "链接: https://pan.baidu.com/s/1AbCdEfGhIjKlMnOpQrStUv 提取码: ab12 --来自百度网盘超级会员v5的分享"
https://pan.baidu.com/s/1AbCdEfGhIjKlMnOpQrStUv?pwd=ab12

$ cat forum-post.txt | python panlink.py --json
[
  {"cloud": "baidu", "id": "1AbCdEfGhIjKlMnOpQrStUv", "pwd": "ab12", "path": null, "url": "https://pan.baidu.com/s/1AbCdEfGhIjKlMnOpQrStUv?pwd=ab12"},
  {"cloud": "quark", "id": "0123456789ab", "pwd": "abcd", "path": null, "url": "https://pan.quark.cn/s/0123456789ab?pwd=abcd"}
]
```

It handles the `/s/`, `share/init?surl=` and `wap/init` forms, picks the code from `?pwd=`, `提取码`, `密码` or `code:` text following each link, keeps `#list/path=` folders, and de-duplicates. Python 3.9+, no packages. Useful before pasting a link into a download tool, a ticket, or a message to a friend.

## Downloading when you have no Baidu account

Everything that worked 2018–2020 (PanDownload, direct-link bookmarklets, user-agent spoofing) is dead or now needs your own logged-in SVIP account, which brings you back to the +86 phone problem.

What works in 2026 is having the file fetched for you: paste the cleaned link on [baidufast.com](https://baidufast.com/?utm_source=github-repo), see the real size and the price, and get a normal HTTPS download link. Shares up to 150 MB are free; larger ones are priced by size with a cap, shown before you pay. Quark links go in the same box.

A longer write-up with step-by-step instructions, prices and FAQ is in this gist: [How to download from pan.baidu.com outside China (2026)](https://gist.github.com/markdrew156/a0a2d48dd2842ae85e264ffd99d24984). Questions and link requests go in its comments.

## Contributing

Found a link form or error message not listed here? Open an issue or a pull request with the example. Please do not post extraction codes for copyrighted material.

## License

MIT for `panlink.py`. The text is CC BY 4.0.
