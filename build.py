"""Copies Sammy's live Command Center (read-only) and adds the new design.
Run by GitHub Actions every hour. Sammy's site is never changed."""
import urllib.request, pathlib, sys
SRC = "https://adexpert-command-center.netlify.app/"
out = pathlib.Path("_site"); out.mkdir(exist_ok=True)
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "adexpert-skin"}), timeout=60).read()
html = get(SRC).decode("utf-8")
tag = "<script>window.__dashStart();</script>"
if "const RAW = " not in html or tag not in html:
    sys.exit("Live dashboard layout changed; keeping the last good version.")
html = html.replace('src="d3.min.js"', 'src="https://adexpert-command-center.netlify.app/d3.min.js"')
html = html.replace("</head>", '<meta name="robots" content="noindex, nofollow"><link rel="stylesheet" href="adexpert-skin.css"></head>', 1)
html = html.replace(tag, tag + '<script src="adexpert-skin.js"></script>', 1)
(out / "index.html").write_text(html, encoding="utf-8")
for f in ("adexpert-skin.css", "adexpert-skin.js"):
    (out / f).write_bytes(pathlib.Path(f).read_bytes())
(out / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
print("Built from live data:", len(html), "bytes")
