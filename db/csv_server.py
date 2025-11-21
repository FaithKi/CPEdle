import csv
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class CsvDb:
    def __init__(self, csv_file):
        self.rows = []
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.rows.append(row)

    def get_by_name(self, name):
        for row in self.rows:
            full_name = row[0].strip()
            if full_name.lower() == name.lower():
                return row
        return None

    def get_by_rownum(self, n):
        if 0 <= n < len(self.rows):
            return self.rows[n]
        return None


db = CsvDb("data.csv")


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        # GET /by-name?name=John%20Smith
        if parsed.path == "/by-name":
            name = query.get("name", [None])[0]
            result = db.get_by_name(name)
            self.respond(result)
            return

        # GET /by-row?num=5
        if parsed.path == "/by-row":
            num = query.get("num", [None])[0]
            if num is not None:
                result = db.get_by_rownum(int(num))
                self.respond(result)
                return

        # Default
        self.respond({"error": "Invalid endpoint"})

    def respond(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        import json
        self.wfile.write(json.dumps(content).encode("utf-8"))


if __name__ == "__main__":
    print("Server running on http://localhost:8080")
    HTTPServer(("localhost", 8080), RequestHandler).serve_forever()
