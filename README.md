# gluten.rocks

A love letter to gluten — written by someone who can never have it.

This is a static website celebrating the magnificent, stretchy, structurally-superior protein that makes real bread *real bread*. It also catalogues, with great tenderness, exactly why gluten-free bread cannot replicate it.

The site owner has celiac disease. Yes, really.

---

## Tech stack

- **Static HTML/CSS** — zero JavaScript required
- **NGINX** — web server with security headers
- **Docker Compose** — for the local demo
- **pytest** — integration test suite

---

## Running the demo locally

**Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
# 1. Start the site
make up

# 2. Open in your browser
make open
# or visit http://localhost:8080 manually

# 3. Stop when done
make down
```

That's it. No database. No build step. No node_modules.

---

## Running the tests

```bash
# Install test dependencies (one-time)
make install-test

# Start the site and run the full suite
make test
```

The test suite covers:

| Category | What it checks |
|---|---|
| Availability | HTTP 200 for all pages and assets |
| Security headers | X-Frame-Options, CSP, XCTO, Referrer-Policy, Permissions-Policy |
| Server hardening | Version not disclosed in Server header |
| Content | Key copy, images, the famous quote |
| Accessibility | Alt text on all images, SVG ARIA labels |
| HTML validity | Charset, viewport, lang attribute |

You can point the tests at any environment:

```bash
BASE_URL=https://gluten.rocks pytest tests/test_site.py -v
```

---

## Deploying to production

1. Point your DNS at your server.
2. Copy the repo to `/var/www/gluten.rocks` (or wherever you prefer).
3. Copy `nginx/nginx.conf` → `/etc/nginx/nginx.conf` and `nginx/conf.d/gluten.conf` → `/etc/nginx/conf.d/gluten.conf`.
4. Set `root` in the nginx config to point at the `website/` directory.
5. Add SSL with Let's Encrypt:

   ```bash
   certbot --nginx -d gluten.rocks -d www.gluten.rocks
   ```

6. Uncomment the SSL server blocks in `nginx/conf.d/gluten.conf`.

---

## Project structure

```
gluten.rocks/
├── website/
│   ├── index.html            # The whole site
│   ├── css/
│   │   └── style.css         # All styles
│   └── images/
│       ├── beautiful-bread.svg   # Original SVG illustration
│       └── sad-gf-bread.svg      # Original SVG illustration
├── nginx/
│   ├── nginx.conf            # Main nginx config
│   └── conf.d/
│       └── gluten.conf       # Site config + security headers
├── tests/
│   ├── test_site.py          # pytest integration tests
│   └── requirements.txt      # Test dependencies
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## Silly quotes about gluten-free bread

*Because someone has to say it.*

> "The first ingredient in gluten-free baked goods is disappointment."

> "Gluten-free bread: the loaf that wanted to be bread when it grew up, but gave up halfway through."

> "It's not a sandwich if it crumbles before you finish building it. It's a warning."

> "Gluten-free focaccia is an oxymoron and I will not be taking questions."

> "The density of a gluten-free boule could theoretically anchor a small vessel."

> "Somewhere between rice flour and grief lies gluten-free sourdough."

> "I didn't choose the gluten-free life. The gluten-free life chose me. And it is very disappointing."

> "A baguette walks into a bar. A gluten-free baguette disintegrates in the parking lot before it even gets there."

> "Gluten-free pizza crust: a cracker that got ideas above its station."

> "The correct response to 'I made gluten-free croissants' is silence and respect for the attempt."

---

## License

[MIT](LICENSE) — go wild. Eat bread if you can. Grieve if you cannot.
