import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if (path[0]) == "/" :
            print(host + path)
    else :
            print(host + "/" + path)


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
            return True
    else:
            return False
    


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    return requests.get(url).status_code, requests.get(url).headers.get("Content-Type")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    response = requests.get(url, timeout=5)
    dictionar = {
        "status": response.status_code,
        "content_type": response.headers.get("Content-Type"),
        "length": len(response.content),
        "server": response.headers.get("Server"),
    }


    return dictionar

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []

    for site in SITES:
        rezultat = check_site(site)
        rezultate.append((site, rezultat))
    reusite = []

    for site, rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append((site, rezultat))
    reusite.sort(key=lambda x: x[1]["length"], reverse=True)

    for site, rezultat in reusite:
        print(site, " ", rezultat["status"], ",", rezultat["length"], "octeți")
    print("Reușite:", len(reusite), " Eșuate:", len(rezultate) - len(reusite))



def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    response = requests.get(url, timeout=5)
    present = []
    missing = []
    for header in SECURITY_HEADERS:
        if header in response.headers:
            present.append(header)
        else:
            missing.append(header)

    scor = len(present) / len(SECURITY_HEADERS) * 100
    return {"present": present, "missing": missing, "scor": scor}



def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for _ in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            return {"status": response.status_code, "attempts": _ + 1}
        except requests.RequestException:
            continue

    return {"status": None, "attempts": attempts}

