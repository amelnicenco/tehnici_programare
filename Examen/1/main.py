def build_url(host, path):
    if (path[0]) == "/" :
        print(host + path)
    else :
        print(host + "/" + path)

is_https(url):
    if url.startswith("https://"):
        return True
    else:
        return False

