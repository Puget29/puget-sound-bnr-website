#!/usr/bin/env python3
"""Inject the "Leave Us A Review" widget into the testimonials section of every staged page,
except the location pages under /service-areas/.

Used by scripts/stage.mjs for the Netlify production build, the same post-build pattern as
tools/inject-tracking.py.

    python tools/inject-review-widget.py [stage-dir=build/stage]

What it does, per page that has a testimonials section (id="sv-reviews" or id="reviews"):
  * inserts a trigger button as the last child of that section's .wrap. The button uses the
    site's own button classes (btn btn--primary, with the shared arrow) so it matches every
    other button on the site, not the widget's purple default.
  * appends the popup overlay + its scoped styles + its script once, before </body>.

Skipped:
  * anything under /service-areas/ (the city/location pages) per the request.
  * pages without a testimonials section (nothing to attach the button to).

Idempotent: a page that already contains the widget (id="rlgPopup") is left untouched, so
running the build twice never adds a second copy.
"""
import re
import sys
from pathlib import Path

# The shared button arrow, copied from tools/v4-gen.py BTN_ARROW so the trigger matches the
# site's primary buttons exactly (same markup, same hover animation).
ARROW = ('<svg class="btn__arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 74 74" '
         'height="34" width="34" aria-hidden="true"><circle stroke-width="3" stroke="currentColor" r="35.5" '
         'cy="37" cx="37"/><path fill="currentColor" d="M25 35.5C24.1716 35.5 23.5 36.1716 23.5 37C23.5 '
         '37.8284 24.1716 38.5 25 38.5V35.5ZM49.0607 38.0607C49.6464 37.4749 49.6464 36.5251 49.0607 '
         '35.9393L39.5147 26.3934C38.9289 25.8076 37.9792 25.8076 37.3934 26.3934C36.8076 26.9792 36.8076 '
         '27.9289 37.3934 28.5147L45.8787 37L37.3934 45.4853C36.8076 46.0711 36.8076 47.0208 37.3934 '
         '47.6066C37.9792 48.1924 38.9289 48.1924 39.5147 47.6066L49.0607 38.0607ZM25 38.5L48 38.5V35.5L25 '
         '35.5V38.5Z"/></svg>')

# The trigger button, styled with the site's button classes. Sits centered at the end of the
# testimonials section.
TRIGGER = ('<div class="rlg-review-cta" style="text-align:center;margin-top:36px">'
           '<button type="button" id="rlgOpenPopup" class="btn btn--primary">Leave Us A Review' + ARROW +
           '</button></div>')

# The popup, its scoped styles and its script (the supplied widget, minus its own trigger button,
# which we replace with the site styled TRIGGER above). Kept verbatim so the widget behaves exactly
# as provided.
WIDGET = r"""<!-- Begin Review Link Generator Widget -->
<!-- Popup Overlay -->
<div id="rlgPopup" class="rlg-popup-overlay">
    <div class="rlg-popup-content">
        <span id="rlgClosePopup" class="rlg-close">&times;</span>
        <div class="rlg-review-container">
            <h3>Puget Sound Builders &amp; Renovation - Kitchen &amp; Bathroom</h3>
            <p>We value your feedback! Please rate our service.</p>
            <div class="rlg-star-rating-wrapper">
                <div class="rlg-star-rating">
                    <input type="radio" id="rlgStar5" name="rlgRating" value="5"/>
                    <label for="rlgStar5" title="5 stars">&#9733;</label>
                    <input type="radio" id="rlgStar4" name="rlgRating" value="4"/>
                    <label for="rlgStar4" title="4 stars">&#9733;</label>
                    <input type="radio" id="rlgStar3" name="rlgRating" value="3"/>
                    <label for="rlgStar3" title="3 stars">&#9733;</label>
                    <input type="radio" id="rlgStar2" name="rlgRating" value="2"/>
                    <label for="rlgStar2" title="2 stars">&#9733;</label>
                    <input type="radio" id="rlgStar1" name="rlgRating" value="1"/>
                    <label for="rlgStar1" title="1 star">&#9733;</label>
                </div>
                <button class="rlg-submit-btn" onclick="rlgSubmitReview()">Submit Review</button>
            </div>
            <div class="rlg-feedback-form" id="rlgFeedbackForm">
                <h3>Your Feedback</h3>
                <textarea id="rlgFeedbackText" placeholder="Please let us know how we can improve our service..."></textarea>
                <button class="rlg-submit-btn" onclick="rlgSubmitFeedback()">Submit Feedback</button>
            </div>
            <div class="rlg-thank-you" id="rlgThankYou">
                <p>&#10003;</p>
                <p>Thank you for your feedback!</p>
            </div>

            <div class="rlg-positive-reviews">
                <h3>Our most recent online review:</h3>
                <div class="rlg-review">

      <div class="rlg-review-avatar rlg-review-avatar-fallback">
        <span>A</span>
        <img
          class="rlg-review-avatar-img"
          src="https://cdn.jsdelivr.net/gh/yamos28/ReviewWidget26@main/public/reviewer-images/reviewer1.jpg"
          alt="Avery Morgan"
          loading="lazy"
          referrerpolicy="no-referrer"
          onerror="this.style.display='none'; this.parentNode.classList.add('rlg-avatar-fallback');"
        />
      </div>

                    <div class="rlg-review-content">
                        <strong>Avery Morgan</strong>
                        <div class="rlg-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                        <span class="rlg-time">2 days ago</span>
                        <p>Professional, friendly, and on time. Othe service businesses should learn from Puget Sound Builders &amp; Renovation - Kitchen &amp; Bathroom!</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* Review Link Generator Styles - Scoped with rlg- prefix */
.rlg-popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px);
    z-index: 999999;
    display: none;
    animation: rlgFadeIn 0.2s ease;
}
@keyframes rlgFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.rlg-popup-content {
    background: #fff;
    margin: 5% auto;
    padding: 32px;
    width: 90%;
    max-width: 480px;
    border-radius: 16px;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    animation: rlgSlideUp 0.3s ease;
}
@keyframes rlgSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.rlg-close {
    position: absolute;
    top: 16px;
    right: 20px;
    font-size: 28px;
    color: #9ca3af;
    cursor: pointer;
    line-height: 1;
    transition: color 0.2s;
}
.rlg-close:hover { color: #374151; }
.rlg-review-container { text-align: center; }
.rlg-review-container > h3 { color: #000; }
.rlg-review-container h1 {
    font-size: 24px;
    font-weight: 600;
    color: #111827;
    margin: 0 0 12px 0;
}
.rlg-review-container > p {
    font-size: 15px;
    color: #6b7280;
    margin: 0 0 24px 0;
}
.rlg-star-rating-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}
.rlg-star-rating {
    display: inline-flex;
    flex-direction: row-reverse;
    font-size: 36px;
}
.rlg-star-rating input { display: none; }
.rlg-star-rating label {
    color: #e5e7eb;
    cursor: pointer;
    margin: 0 2px;
    transition: color 0.15s, transform 0.15s;
}
.rlg-star-rating label:hover { transform: scale(1.1); }
.rlg-star-rating input:checked ~ label,
.rlg-star-rating label:hover,
.rlg-star-rating label:hover ~ label {
    color: #fbbf24;
}
.rlg-review-button, .rlg-submit-btn {
    background: #7366f1;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
}
.rlg-review-button:hover, .rlg-submit-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.rlg-feedback-form {
    display: none;
    margin-top: 24px;
    animation: rlgFadeIn 0.3s ease;
}
.rlg-feedback-form h2 {
    font-size: 18px;
    color: #111827;
    margin: 0 0 12px 0;
}
.rlg-feedback-form textarea {
    width: 100%;
    height: 100px;
    padding: 12px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    font-size: 14px;
    resize: vertical;
    margin-bottom: 12px;
}
.rlg-feedback-form textarea:focus {
    outline: none;
    border-color: #7366f1;
    box-shadow: 0 0 0 3px #7366f120;
}
.rlg-thank-you {
    display: none;
    text-align: center;
    padding: 24px;
}
.rlg-thank-you h2 {
    font-size: 48px;
    color: #10b981;
    margin: 0 0 8px 0;
}
.rlg-thank-you p {
    font-size: 16px;
    color: #374151;
    margin: 0;
}
.rlg-positive-reviews {
    margin-top: 32px;
    text-align: left;
    border-top: 1px solid #f3f4f6;
    padding-top: 24px;
}
.rlg-positive-reviews h3 {
    font-size: 14px;
    color: #000;
    margin: 0 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.rlg-review {
    display: flex;
    gap: 12px;
    padding: 16px;
    background: #f9fafb;
    border-radius: 12px;
}
.rlg-review-avatar {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #7366f1, #7366f1cc);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
    flex-shrink: 0;
    position: relative;
}
.rlg-review-avatar-img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
    border-radius: 50%;
}
.rlg-review-avatar-fallback span {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
    color: #fff;
}
.rlg-review-avatar-fallback.rlg-avatar-fallback {
    background: linear-gradient(135deg, #7366f1, #7366f1cc);
}
.rlg-review-content { flex: 1; }
.rlg-review-content strong {
    display: block;
    font-size: 14px;
    color: #111827;
    margin-bottom: 4px;
}
.rlg-review-content .rlg-stars {
    color: #fbbf24;
    font-size: 14px;
    margin-bottom: 4px;
}
.rlg-review-content .rlg-time {
    font-size: 12px;
    color: #9ca3af;
    display: block;
    margin-bottom: 8px;
}
.rlg-review-content p {
    font-size: 13px;
    color: #4b5563;
    margin: 0;
    line-height: 1.5;
}
</style>

<script>
(function() {
    var rlgReviewLink = "https://search.google.com/local/writereview?placeid=ChIJdW-rLktdkFQRVyJh3IBFrQI";
    var rlgEmail = "office@pugetsoundbnr.com";
    var rlgBusinessName = "Puget Sound Builders & Renovation - Kitchen & Bathroom";
    var rlgPlatform = "google";
    var rlgMinRating = 4;
    var platformHash = '';
    var rlgFeedbackEndpoint = "https://reviewtool.gsmarketingroup.com/api/send-feedback";
    var rlgTrackEndpoint = "https://reviewtool.gsmarketingroup.com/api/track-event";
    var rlgLastRating = 0;

    function rlgResolveEndpoint(url) {
        if (!url) return '';
        try {
            return new URL(url, window.location.origin).toString();
        } catch {
            return url;
        }
    }

    var rlgFeedbackEndpointResolved = rlgResolveEndpoint(rlgFeedbackEndpoint);
    var rlgTrackEndpointResolved = rlgResolveEndpoint(rlgTrackEndpoint);

    function rlgNormalizeHash(hash) {
        if (!hash) return '';
        return hash.toLowerCase().split('?')[0];
    }

    function rlgMaybeOpenFromHash() {
        var currentHash = rlgNormalizeHash(window.location.hash);
        if (currentHash === platformHash) {
            rlgOpenPopup('hash');
        }
    }

    function rlgGetWidgetUrl() {
        var hash = platformHash || rlgNormalizeHash(window.location.hash);
        if (!hash) return window.location.href;
        return window.location.origin + window.location.pathname + hash;
    }

    function rlgTrackEvent(eventType, extra) {
        if (!rlgTrackEndpointResolved) return;
        var payload = {
            businessEmail: rlgEmail,
            businessName: rlgBusinessName,
            platform: rlgPlatform,
            eventType: eventType,
            timestamp: new Date().toISOString(),
            pageUrl: window.location.href,
            referrer: document.referrer || '',
            reviewLink: rlgReviewLink,
            widgetUrl: rlgGetWidgetUrl()
        };
        if (extra) {
            for (var key in extra) {
                payload[key] = extra[key];
            }
        }
        try {
            var body = JSON.stringify(payload);
            if (navigator.sendBeacon) {
                var blob = new Blob([body], { type: 'application/json' });
                navigator.sendBeacon(rlgTrackEndpointResolved, blob);
                return;
            }
            fetch(rlgTrackEndpointResolved, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: body,
                keepalive: true
            }).catch(function() {});
        } catch (err) {
            // ignore tracking errors
        }
    }

    function rlgOpenPopup(source) {
        document.getElementById('rlgPopup').style.display = 'block';
        document.body.style.overflow = 'hidden';
        rlgTrackEvent('widget_open', { source: source || 'button' });
    }
    function rlgClosePopup() {
        document.getElementById('rlgPopup').style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    window.rlgSubmitReview = function() {
        var rating = document.querySelector('#rlgPopup input[name="rlgRating"]:checked');
        if (!rating) {
            alert('Please select a rating before submitting.');
            return;
        }
        rlgLastRating = parseInt(rating.value);
        if (rlgLastRating >= rlgMinRating) {
            rlgTrackEvent('review_redirect', { rating: rlgLastRating });
            window.location.href = rlgReviewLink;
        } else {
            document.getElementById('rlgFeedbackForm').style.display = 'block';
            document.querySelector('.rlg-star-rating-wrapper').style.display = 'none';
            if (document.querySelector('.rlg-positive-reviews')) {
                document.querySelector('.rlg-positive-reviews').style.display = 'none';
            }
        }
    };
    window.rlgSubmitFeedback = function() {
        var feedback = document.getElementById('rlgFeedbackText').value;
        if (feedback.trim() === '') {
            alert('Please enter your feedback before submitting.');
            return;
        }
        var payload = {
            businessName: rlgBusinessName,
            businessEmail: rlgEmail,
            customerRating: rlgLastRating || 0,
            customerFeedback: feedback,
            platform: rlgPlatform,
            timestamp: new Date().toISOString()
        };
        if (!rlgFeedbackEndpointResolved) {
            alert('Feedback service is not configured. Please try again later.');
            return;
        }
        fetch(rlgFeedbackEndpointResolved, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true
        })
        .then(function(res) {
            if (!res.ok) throw new Error('Failed to send feedback');
            return res.json().catch(function() { return {}; });
        })
        .then(function() {
            rlgTrackEvent('feedback_submit', { rating: rlgLastRating || 0 });
            document.getElementById('rlgFeedbackForm').style.display = 'none';
            document.getElementById('rlgThankYou').style.display = 'block';
        })
        .catch(function() {
            alert('Sorry, there was a problem sending your feedback. Please try again.');
        });
    };
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('rlgOpenPopup').addEventListener('click', function() {
            rlgOpenPopup('button');
        });
        document.getElementById('rlgClosePopup').addEventListener('click', rlgClosePopup);
        document.getElementById('rlgPopup').addEventListener('click', function(e) {
            if (e.target === this) rlgClosePopup();
        });
        // Support #review for Google, platform-specific hashes for others
        platformHash = '#review';
        platformHash = platformHash.toLowerCase();
        rlgMaybeOpenFromHash();
        window.addEventListener('hashchange', rlgMaybeOpenFromHash);
    });
})();
</script>
<!-- End Review Link Generator Widget -->"""


def main():
    stage = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build") / "stage"
    injected = 0
    for f in sorted(stage.rglob("*.html")):
        rel = f.relative_to(stage)
        if rel.parts and rel.parts[0] == "service-areas" and rel.parts[1:2] != ("algona",):
            continue  # location pages skip the review button, EXCEPT the optimized Algona pilot page
        html = f.read_text(encoding="utf-8")
        if 'id="rlgPopup"' in html:
            continue  # already has the widget
        m = re.search(r'id="(sv-reviews|reviews)"', html)
        if not m:
            continue  # no testimonials section on this page
        sec_id = m.group(1)
        # Insert the trigger as the last child of the testimonials section's .wrap (right before
        # the wrap-close + section-close that end the section).
        pat = re.compile(r'(<section[^>]*id="' + sec_id + r'".*?)(\s*</div>\s*</section>)', re.S)
        new, n = pat.subn(lambda mm: mm.group(1) + "\n    " + TRIGGER + mm.group(2), html, count=1)
        if n != 1:
            print(f"inject-review-widget: WARNING could not place button in {f}, skipped")
            continue
        new, n2 = re.subn(r'</body>', "\n" + WIDGET + "\n</body>", new, count=1)
        if n2 != 1:
            print(f"inject-review-widget: WARNING no </body> in {f}, skipped")
            continue
        f.write_text(new, encoding="utf-8", newline="")
        injected += 1
    print(f"inject-review-widget: injected into {injected} page(s)")


if __name__ == "__main__":
    main()
