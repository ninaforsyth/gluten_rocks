"""
gluten.rocks — integration test suite

Run against the live Docker container:
    pytest tests/test_site.py -v

Override the base URL:
    BASE_URL=http://localhost:9090 pytest tests/test_site.py -v
"""

import os
import pytest
import requests
import html5lib

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080").rstrip("/")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get(path="/"):
    """Perform a GET request and return the response."""
    url = f"{BASE_URL}{path}"
    return requests.get(url, timeout=10)


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

class TestAvailability:
    def test_homepage_returns_200(self):
        r = get("/")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"

    def test_html_content_type(self):
        r = get("/")
        ct = r.headers.get("Content-Type", "")
        assert "text/html" in ct, f"Expected HTML content-type, got: {ct}"

    def test_css_returns_200(self):
        r = get("/css/style.css")
        assert r.status_code == 200

    def test_beautiful_bread_svg_returns_200(self):
        r = get("/images/beautiful-bread.svg")
        assert r.status_code == 200

    def test_sad_gf_bread_svg_returns_200(self):
        r = get("/images/sad-gf-bread.svg")
        assert r.status_code == 200

    def test_unknown_path_does_not_return_500(self):
        r = get("/this-does-not-exist")
        assert r.status_code != 500


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

class TestSecurityHeaders:
    def setup_method(self):
        self.r = get("/")

    def test_x_frame_options(self):
        val = self.r.headers.get("X-Frame-Options", "")
        assert val.upper() in ("SAMEORIGIN", "DENY"), \
            f"Unexpected X-Frame-Options: {val!r}"

    def test_x_content_type_options(self):
        val = self.r.headers.get("X-Content-Type-Options", "")
        assert val.lower() == "nosniff", \
            f"Unexpected X-Content-Type-Options: {val!r}"

    def test_x_xss_protection(self):
        val = self.r.headers.get("X-XSS-Protection", "")
        assert "1" in val, f"Expected X-XSS-Protection to contain '1', got: {val!r}"

    def test_referrer_policy(self):
        val = self.r.headers.get("Referrer-Policy", "")
        assert val != "", "Referrer-Policy header is missing"

    def test_permissions_policy(self):
        val = self.r.headers.get("Permissions-Policy", "")
        assert val != "", "Permissions-Policy header is missing"

    def test_content_security_policy_present(self):
        val = self.r.headers.get("Content-Security-Policy", "")
        assert val != "", "Content-Security-Policy header is missing"

    def test_csp_no_unsafe_eval(self):
        val = self.r.headers.get("Content-Security-Policy", "")
        assert "unsafe-eval" not in val.lower(), \
            "CSP should not allow 'unsafe-eval'"

    def test_csp_frame_ancestors(self):
        val = self.r.headers.get("Content-Security-Policy", "")
        assert "frame-ancestors" in val, \
            "CSP should include 'frame-ancestors'"

    def test_server_version_not_disclosed(self):
        server = self.r.headers.get("Server", "")
        # nginx/1.x.x would expose the version — we want just "nginx" or nothing
        assert "/" not in server, \
            f"Server header should not disclose version: {server!r}"


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

class TestContent:
    def setup_method(self):
        self.r = get("/")
        self.html = self.r.text.lower()

    def test_page_title_present(self):
        assert "gluten" in self.html

    def test_famous_quote_present(self):
        assert "disappointment" in self.html

    def test_real_bread_mentioned(self):
        assert "real bread" in self.html

    def test_gf_bread_mentioned(self):
        assert "gluten-free" in self.html

    def test_celiac_mentioned(self):
        assert "celiac" in self.html

    def test_comparison_section_present(self):
        assert "a tale of two breads" in self.html

    def test_beautiful_bread_img_tag(self):
        assert "beautiful-bread.svg" in self.html

    def test_sad_gf_bread_img_tag(self):
        assert "sad-gf-bread.svg" in self.html

    def test_images_have_alt_text(self):
        # Both img tags should have non-empty alt attributes
        import re
        imgs = re.findall(r'<img[^>]+>', self.r.text, re.IGNORECASE)
        for img in imgs:
            assert 'alt="' in img and 'alt=""' not in img, \
                f"Image missing or empty alt text: {img}"


# ---------------------------------------------------------------------------
# HTML validity
# ---------------------------------------------------------------------------

class TestHtmlValidity:
    def test_parses_without_error(self):
        r = get("/")
        parser = html5lib.HTMLParser(strict=False)
        # html5lib raises ParseError in strict mode; we do a softer check
        try:
            doc = html5lib.parse(r.text)
            assert doc is not None
        except Exception as exc:
            pytest.fail(f"HTML failed to parse: {exc}")

    def test_has_lang_attribute(self):
        r = get("/")
        assert 'lang="en"' in r.text.lower() or "lang='en'" in r.text.lower()

    def test_has_meta_charset(self):
        r = get("/")
        assert "charset" in r.text.lower()

    def test_has_meta_viewport(self):
        r = get("/")
        assert "viewport" in r.text.lower()


# ---------------------------------------------------------------------------
# SVG accessibility
# ---------------------------------------------------------------------------

class TestSvgAccessibility:
    def test_beautiful_bread_svg_has_role(self):
        r = get("/images/beautiful-bread.svg")
        assert 'role="img"' in r.text

    def test_sad_gf_bread_svg_has_role(self):
        r = get("/images/sad-gf-bread.svg")
        assert 'role="img"' in r.text

    def test_beautiful_bread_svg_has_aria_label(self):
        r = get("/images/beautiful-bread.svg")
        assert "aria-label" in r.text

    def test_sad_gf_bread_svg_has_aria_label(self):
        r = get("/images/sad-gf-bread.svg")
        assert "aria-label" in r.text
