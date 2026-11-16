=== BNR Lead Handler ===
Contributors: pugetsoundbnr
Requires at least: 5.8
Tested up to: 6.6
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later

Receives the lead form of the static PPC landing pages and emails each lead.

== Description ==
Route: POST /wp-json/bnr/v1/lead (JSON). Fields: name, phone, zip, email, service, origin_city, origin_page, optional attribution fields, honeypot "website", and "elapsed" (milliseconds the form was open).

Checks: 5 digit zip, valid email, phone of 10 to 15 digits, size limits, honeypot, minimum fill time (3 seconds), 5 requests per IP per 10 minutes. No cookies, no external services.

Each valid lead is sent as one plain text email with wp_mail to the address set at the top of bnr-lead-handler.php (BNR_LEAD_TO, default Leads@pugetsoundbnr.com). Reply to is the visitor.

Tools > BNR leads shows the last 200 attempts (time, result, page, masked email).

== Install ==
Plugins > Add New > Upload Plugin > choose bnr-lead-handler.zip > Install > Activate.

== Change the email address ==
Open bnr-lead-handler.php and change the one line that defines BNR_LEAD_TO.

== Remove ==
Deactivate and delete the plugin. The log is stored in the option bnr_lead_log.
