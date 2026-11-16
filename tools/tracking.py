"""Google Tag Manager and Google Ads snippets for the live pages, read from data/tracking.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tracking_blocks():
    t = json.loads((ROOT / "data" / "tracking.json").read_text(encoding="utf-8"))
    head, noscript = "", ""
    g = t.get("gtm", {})
    if g.get("enabled") and g.get("id"):
        i = g["id"]
        head += ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
                 "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
                 "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','" + i + "');</script>\n<!-- End Google Tag Manager -->\n")
        noscript = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + i +
                    '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')
    a = t.get("googleAds", {})
    if a.get("enabled") and a.get("id"):
        i = a["id"]
        head += ('<!-- Google Ads tag -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=' + i + '"></script>\n'
                 "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','" + i + "');</script>\n")
    return head, noscript
