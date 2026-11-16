<?php
/**
 * Plugin Name: BNR Home Loader
 * Description: Serves the finished static BNR pages from the plugin folder. Every built page has a hidden preview at /home-new/ with nested routes for service pages (noindex). A page takes over its real WordPress address only when it is named in BNR_LIVE_PAGES (home also when BNR_HOME_LIVE is true). Everything else on the site is untouched.
 * Version: 2.2.0
 * Author: BNR
 * License: GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/*
 * THE SWITCHES. Change only what is after the comma, save, then clear WP Rocket.
 *
 * BNR_HOME_LIVE:  false = the old Elementor home stays at /.   true = the new home page is served at / (same as adding 'home' to the list below).
 * BNR_LIVE_PAGES: pages that take over their real WordPress address. Empty = none, only the hidden previews work.
 *                 Names: 'home', 'about', 'contact', 'services', 'projects', 'kitchen', 'bathroom', 'roofing', 'deck', 'adu', 'siding', 'flooring', 'painting', 'blog', and one 'blog-<post-slug>' per imported post. Example: array( 'about', 'contact' )
 *                 ('privacy' only has a preview, it never takes over an address.)
 * Preview addresses always work: /home-new/  /home-new/about/  /home-new/contact/  /home-new/privacy/  /home-new/our-services/  /home-new/remodeling-projects/  /home-new/blog/  /home-new/blog/<post-slug>/ and the service routes.
 * Projects: 'projects' = /remodeling-projects/ (exact address only, the old project sub pages such as /shower-replacement/ or /composite-deck/ stay WordPress).
 * Service pages: 'services' = /our-services/, 'kitchen' = /kitchen-remodel-seattle/, 'bathroom' = /bathroom-remodel-seattle/, 'roofing' = /roof-repair-company-in-seattle/, 'deck' = /our-services/deck-building/, 'adu' = /our-services/adu-garage-conversion/, 'siding' = /siding-replacement/, 'flooring' = /flooring-replacement-in-seattle/, 'painting' = /our-services/painting/. Exact address only: child pages such as /kitchen-remodel-seattle/<city>/ stay WordPress.
 */
define( 'BNR_HOME_LIVE', false );
define( 'BNR_LIVE_PAGES', array() );

/** The page table, written by the build (pages/pages.json): slug => preview path, live path. */
function bnr_home_loader_pages() {
	static $pages = null;
	if ( null === $pages ) {
		$pages = array();
		$f     = __DIR__ . '/pages/pages.json';
		if ( is_file( $f ) && is_readable( $f ) ) {
			$j = json_decode( (string) file_get_contents( $f ), true );
			if ( is_array( $j ) ) {
				$pages = $j;
			}
		}
	}
	return $pages;
}

/** Normalise a path for comparing: lower case, one trailing slash. */
function bnr_home_loader_norm( $p ) {
	$p = strtolower( (string) $p );
	return rtrim( $p, '/' ) . '/';
}

/**
 * Serve a page file when the request is a preview address or the real address of a page named in BNR_LIVE_PAGES.
 * Runs on template_redirect at priority 0, before WP Rocket's cache buffer and before any theme or Elementor output.
 */
function bnr_home_loader_serve() {
	// never touch admin, ajax, REST, feeds, previews, the customizer, cron or command line
	if ( is_admin() || wp_doing_ajax() || wp_doing_cron() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) || ( defined( 'WP_CLI' ) && WP_CLI ) ) {
		return;
	}
	if ( is_feed() || is_preview() || is_customize_preview() || is_robots() || is_trackback() ) {
		return;
	}
	$method = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( $_SERVER['REQUEST_METHOD'] ) : 'GET';
	if ( 'GET' !== $method && 'HEAD' !== $method ) {
		return;
	}
	$pages = bnr_home_loader_pages();
	if ( ! $pages ) {
		return;
	}

	$uri  = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '/';
	$path = (string) wp_parse_url( $uri, PHP_URL_PATH );
	$base = rtrim( (string) wp_parse_url( home_url(), PHP_URL_PATH ), '/' ); // empty unless WordPress sits in a subfolder
	if ( '' !== $base && 0 === strpos( $path, $base ) ) {
		$path = substr( $path, strlen( $base ) );
	}
	$np = bnr_home_loader_norm( '' === $path ? '/' : $path );

	$live_list = is_array( BNR_LIVE_PAGES ) ? BNR_LIVE_PAGES : array();
	if ( BNR_HOME_LIVE ) {
		$live_list[] = 'home';
	}

	$slug = null;
	$kind = null;
	foreach ( $pages as $s => $p ) {
		if ( isset( $p['preview'] ) && bnr_home_loader_norm( $p['preview'] ) === $np ) {
			$slug = $s;
			$kind = 'preview';
			break;
		}
	}
	if ( null === $slug ) {
		foreach ( $pages as $s => $p ) {
			if ( ! empty( $p['live'] ) && in_array( $s, $live_list, true ) && bnr_home_loader_norm( $p['live'] ) === $np ) {
				// only the plain address: tracking parameters and the form prefill are fine, any other query (?s=, ?p=, ?preview=, ?elementor-preview, ?bnr-old=1 ...) goes to WordPress
				$ok = array( 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid', 'gad_source', 'gad_campaignid', 'service' );
				foreach ( array_keys( $_GET ) as $key ) {
					if ( ! in_array( strtolower( (string) $key ), $ok, true ) ) {
						return;
					}
				}
				$slug = $s;
				$kind = 'live';
				break;
			}
		}
	}
	if ( null === $slug ) {
		return;
	}

	$safe = preg_replace( '/[^a-z0-9-]/', '', strtolower( (string) $slug ) );
	$file = __DIR__ . '/pages/' . $safe . '.' . $kind . '.html';
	if ( '' === $safe || ! is_file( $file ) || ! is_readable( $file ) ) {
		return; // missing or unreadable: do nothing, WordPress continues
	}
	$size  = filesize( $file );
	$mtime = filemtime( $file );
	if ( false === $size || false === $mtime ) {
		return;
	}
	$etag = '"' . md5( $kind . $mtime . '-' . $size ) . '"';

	if ( ! defined( 'DONOTCACHEPAGE' ) ) {
		define( 'DONOTCACHEPAGE', true ); // keeps cache plugins from storing a copy under the wrong status
	}
	if ( ! headers_sent() ) {
		// WordPress may have prepared a 404 and no-cache headers for a preview address: replace them
		status_header( 200 );
		header_remove( 'Expires' );
		header_remove( 'Pragma' );
		header_remove( 'Last-Modified' );
		header( 'Content-Type: text/html; charset=UTF-8', true );
		header( 'Cache-Control: public, max-age=300', true );
		header( 'ETag: ' . $etag, true );
		header( 'Last-Modified: ' . gmdate( 'D, d M Y H:i:s', $mtime ) . ' GMT', true );
		header( 'Vary: Accept-Encoding', false );
		if ( 'preview' === $kind ) {
			header( 'X-Robots-Tag: noindex, nofollow', true );
		}
		$inm = isset( $_SERVER['HTTP_IF_NONE_MATCH'] ) ? trim( (string) $_SERVER['HTTP_IF_NONE_MATCH'] ) : '';
		if ( '' !== $inm && $inm === $etag ) {
			status_header( 304 );
			exit;
		}
		header( 'Content-Length: ' . $size, true );
	}
	if ( 'HEAD' !== $method ) {
		readfile( $file );
	}
	exit;
}
add_action( 'template_redirect', 'bnr_home_loader_serve', 0 );
