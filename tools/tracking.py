"""Google Tag Manager and Google Ads snippets for the live pages, read from data/tracking.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tracking_blocks(defer=False):
    t = json.loads((ROOT / "data" / "tracking.json").read_text(encoding="utf-8"))
    g = t.get("gtm", {})
    a = t.get("googleAds", {})
    gtm_id = g["id"] if (g.get("enabled") and g.get("id")) else None
    ads_id = a["id"] if (a.get("enabled") and a.get("id")) else None
    noscript = ""
    if gtm_id:
        noscript = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + gtm_id +
                    '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')
    if defer:
        # Netlify production build. The dataLayer queue + gtag('config')/pageview + gtm.start are set up
        # immediately for EVERY visitor, so events queue and are sent as soon as the scripts load. Only the
        # SCRIPT LOADING is device-aware at runtime (the same static HTML is served to all visitors): desktop
        # (the hero's own criteria - wide viewport, not save-data, not 2g/3g) loads GTM + Google Ads
        # immediately, exactly as before; mobile/constrained connections defer the load off the critical path
        # (first user interaction OR a bounded idle/timeout, whichever comes first, once) to free Slow-4G
        # bandwidth for the LCP hero/CSS. No container/ID/conversion change; nothing is disabled.
        srcs = []
        if gtm_id: srcs.append("https://www.googletagmanager.com/gtm.js?id=" + gtm_id)
        if ads_id: srcs.append("https://www.googletagmanager.com/gtag/js?id=" + ads_id)
        if not srcs:
            return "", noscript
        queue = "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        if gtm_id: queue += "dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
        if ads_id: queue += "gtag('js',new Date());gtag('config','" + ads_id + "');"
        head = ("<!-- Google Tag Manager -->\n<script>" + queue +
                "(function(d){var L=0,E=['scroll','pointerdown','keydown','touchstart'];"
                "function go(){if(L)return;L=1;E.forEach(function(e){removeEventListener(e,go);});" +
                json.dumps(srcs) + ".forEach(function(u){var j=d.createElement('script');j.async=1;j.src=u;d.head.appendChild(j);});}"
                "var c=navigator.connection||{},dsk=innerWidth>900&&!c.saveData&&!/(^|-)(2g|3g)$/.test(c.effectiveType||'');"
                "if(dsk){go();}else{E.forEach(function(e){addEventListener(e,go,{once:true,passive:true});});"
                "('requestIdleCallback'in window)?requestIdleCallback(go,{timeout:3500}):setTimeout(go,3500);}"
                "})(document);</script>\n<!-- End Google Tag Manager -->\n")
        return head, noscript
    # WordPress live pipeline (home-live.py): original immediate loading - unchanged.
    head = ""
    if gtm_id:
        i = gtm_id
        head += ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
                 "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
                 "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','" + i + "');</script>\n<!-- End Google Tag Manager -->\n")
    if ads_id:
        i = ads_id
        head += ('<!-- Google Ads tag -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=' + i + '"></script>\n'
                 "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','" + i + "');</script>\n")
    return head, noscript
