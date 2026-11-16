<?php
/**
 * Plugin Name: BNR Lead Handler
 * Description: Receives the lead form of the static PPC landing pages (POST /wp-json/bnr/v1/lead) and emails each lead. No cookies, no external services.
 * Version: 1.0.0
 * Author: Puget Sound BNR
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) {
    exit;
}

/* Where leads are emailed. Change this one line (or define BNR_LEAD_TO in wp-config.php before this plugin loads). */
if (!defined('BNR_LEAD_TO')) {
    define('BNR_LEAD_TO', 'Leads@pugetsoundbnr.com');
}

const BNR_LEAD_MIN_FILL_MS = 3000;     // a human needs at least 3 seconds to fill the form
const BNR_LEAD_RATE_MAX    = 5;        // per IP
const BNR_LEAD_RATE_WINDOW = 600;      // seconds (10 minutes)
const BNR_LEAD_LOG_KEEP    = 200;      // last attempts kept
const BNR_LEAD_LOG_OPTION  = 'bnr_lead_log';

add_action('rest_api_init', function () {
    register_rest_route('bnr/v1', '/lead', array(
        'methods'             => 'POST',
        'callback'            => 'bnr_lead_handle',
        'permission_callback' => '__return_true',
    ));
});

function bnr_lead_reply($ok, $status, $error = '')
{
    $body = $ok ? array('ok' => true) : array('ok' => false, 'error' => $error);
    $resp = new WP_REST_Response($body, $status);
    $resp->header('Cache-Control', 'no-store');
    return $resp;
}

function bnr_lead_ip()
{
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
    $private = !filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE);
    if ($private && !empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $parts = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $first = trim($parts[0]);
        if (filter_var($first, FILTER_VALIDATE_IP)) {
            $ip = $first;
        }
    }
    return $ip;
}

function bnr_lead_mask_email($email)
{
    $at = strpos($email, '@');
    if ($at === false || $at < 1) {
        return '(none)';
    }
    return substr($email, 0, 1) . '***' . substr($email, $at);
}

function bnr_lead_log($ok, $page, $email, $note = '')
{
    $log = get_option(BNR_LEAD_LOG_OPTION, array());
    if (!is_array($log)) {
        $log = array();
    }
    $log[] = array(
        'time'  => gmdate('Y-m-d H:i:s') . ' UTC',
        'ok'    => $ok ? 'ok' : 'error',
        'page'  => substr($page, 0, 120),
        'email' => bnr_lead_mask_email($email),
        'note'  => substr($note, 0, 60),
    );
    if (count($log) > BNR_LEAD_LOG_KEEP) {
        $log = array_slice($log, -BNR_LEAD_LOG_KEEP);
    }
    update_option(BNR_LEAD_LOG_OPTION, $log, false);
}

function bnr_lead_clean($value, $max)
{
    if (!is_scalar($value)) {
        return '';
    }
    $value = sanitize_text_field((string) $value);
    return function_exists('mb_substr') ? mb_substr($value, 0, $max) : substr($value, 0, $max);
}

function bnr_lead_handle(WP_REST_Request $request)
{
    $raw = $request->get_body();
    if (strlen($raw) > 8192) {
        return bnr_lead_reply(false, 413, 'too_large');
    }
    $in = $request->get_json_params();
    if (!is_array($in)) {
        $in = $request->get_body_params();
    }
    if (!is_array($in) || !$in) {
        return bnr_lead_reply(false, 400, 'empty');
    }
    foreach ($in as $v) {
        if (is_scalar($v) && strlen((string) $v) > 600) {
            return bnr_lead_reply(false, 400, 'too_large');
        }
    }

    $page_raw = isset($in['origin_page']) ? $in['origin_page'] : '';
    $page     = esc_url_raw(bnr_lead_clean($page_raw, 300));
    $page_path = $page ? wp_parse_url($page, PHP_URL_PATH) : '';
    $email_raw = isset($in['email']) ? sanitize_email(bnr_lead_clean($in['email'], 120)) : '';

    // Spam traps: honeypot filled or form submitted too fast. Look successful, send nothing.
    $elapsed = isset($in['elapsed']) ? (int) $in['elapsed'] : 0;
    if (!empty($in['website']) || $elapsed < BNR_LEAD_MIN_FILL_MS) {
        bnr_lead_log(false, (string) $page_path, $email_raw, 'spam trap');
        return bnr_lead_reply(true, 200);
    }

    // Per IP rate limit (transient).
    $key   = 'bnr_lead_rl_' . md5(bnr_lead_ip());
    $count = (int) get_transient($key);
    if ($count >= BNR_LEAD_RATE_MAX) {
        bnr_lead_log(false, (string) $page_path, $email_raw, 'rate limit');
        return bnr_lead_reply(false, 429, 'rate_limited');
    }
    set_transient($key, $count + 1, BNR_LEAD_RATE_WINDOW);

    $name    = bnr_lead_clean(isset($in['name']) ? $in['name'] : '', 100);
    $phone   = bnr_lead_clean(isset($in['phone']) ? $in['phone'] : '', 40);
    $zip     = bnr_lead_clean(isset($in['zip']) ? $in['zip'] : '', 10);
    $service = bnr_lead_clean(isset($in['service']) ? $in['service'] : '', 80);
    if ($service === '') {
        $service = bnr_lead_clean(isset($in['origin_service']) ? $in['origin_service'] : '', 80);
    }
    $city = bnr_lead_clean(isset($in['origin_city']) ? $in['origin_city'] : '', 80);

    $digits = preg_replace('/\D+/', '', $phone);
    $err = '';
    if (strlen($name) < 2) {
        $err = 'name';
    } elseif (strlen($digits) < 10 || strlen($digits) > 15) {
        $err = 'phone';
    } elseif (!preg_match('/^\d{5}$/', $zip)) {
        $err = 'zip';
    } elseif (!is_email($email_raw)) {
        $err = 'email';
    }
    if ($err !== '') {
        bnr_lead_log(false, (string) $page_path, $email_raw, 'invalid ' . $err);
        return bnr_lead_reply(false, 400, 'invalid_' . $err);
    }

    // Attribution fields, only these keys, short values.
    $extra_keys = array('referrer', 'landing_page', 'first_seen', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'msclkid', 'fbclid');
    $extra = '';
    foreach ($extra_keys as $k) {
        if (!empty($in[$k])) {
            $extra .= $k . ': ' . bnr_lead_clean($in[$k], 200) . "\n";
        }
    }

    $where   = ($city !== '' && strtolower($city) !== 'general') ? $city : (string) $page_path;
    $subject = 'New lead: ' . ($service !== '' ? $service : 'Free consultation') . ' from ' . $where;
    $subject = trim(preg_replace('/[\r\n]+/', ' ', $subject));

    // Main site forms send a source value, the PPC landing pages do not.
    $source = bnr_lead_clean(isset($in['source']) ? $in['source'] : '', 60);
    $body  = ($source !== '' ? "New lead from the website" : "New lead from the PPC landing page") . "\n\n";
    $body .= 'Name: ' . $name . "\n";
    $body .= 'Phone: ' . $phone . "\n";
    $body .= 'Email: ' . $email_raw . "\n";
    $body .= 'Zip code: ' . $zip . "\n";
    $body .= 'Service: ' . ($service !== '' ? $service : '(not chosen)') . "\n";
    $body .= 'City page: ' . $city . "\n";
    $body .= 'Page: ' . $page . "\n";
    if ($extra !== '') {
        $body .= "\n" . $extra;
    }
    $body .= "\nSent " . gmdate('Y-m-d H:i:s') . " UTC\n";

    $reply_name = trim(preg_replace('/[\r\n<>",]+/', ' ', $name));
    $headers = array(
        'Content-Type: text/plain; charset=UTF-8',
        'Reply-To: ' . $reply_name . ' <' . $email_raw . '>',
    );

    $sent = wp_mail(BNR_LEAD_TO, $subject, $body, $headers);
    if (!$sent) {
        bnr_lead_log(false, (string) $page_path, $email_raw, 'mail failed');
        return bnr_lead_reply(false, 500, 'send_failed');
    }
    bnr_lead_log(true, (string) $page_path, $email_raw, 'sent');
    return bnr_lead_reply(true, 200);
}

/* Tools > BNR leads: the last attempts, so delivery can be proven. No personal data except a masked email. */
add_action('admin_menu', function () {
    add_management_page('BNR leads', 'BNR leads', 'manage_options', 'bnr-lead-log', 'bnr_lead_render_log');
});

function bnr_lead_render_log()
{
    if (!current_user_can('manage_options')) {
        return;
    }
    $log = get_option(BNR_LEAD_LOG_OPTION, array());
    $log = is_array($log) ? array_reverse($log) : array();
    echo '<div class="wrap"><h1>BNR leads</h1>';
    echo '<p>Last ' . (int) BNR_LEAD_LOG_KEEP . ' attempts. Leads go to <strong>' . esc_html(BNR_LEAD_TO) . '</strong>.</p>';
    echo '<table class="widefat striped"><thead><tr><th>Time</th><th>Result</th><th>Page</th><th>Email</th><th>Note</th></tr></thead><tbody>';
    if (!$log) {
        echo '<tr><td colspan="5">No attempts yet.</td></tr>';
    }
    foreach ($log as $row) {
        echo '<tr><td>' . esc_html($row['time']) . '</td><td>' . esc_html($row['ok']) . '</td><td>' . esc_html($row['page']) . '</td><td>' . esc_html($row['email']) . '</td><td>' . esc_html($row['note']) . '</td></tr>';
    }
    echo '</tbody></table></div>';
}
