import requests

class HTTPScanner:
    def __init__(self, timeout=3):
        self.timeout = timeout

    def scan(self, host, port=80):
        url = f"http://{host}:{port}/"
        try:
            resp = requests.get(url, timeout=self.timeout)
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "url": url,
                "ok": resp.ok
            }
        except Exception as e:
            return {"error": str(e), "url": url}
