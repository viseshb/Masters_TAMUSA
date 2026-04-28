"""
vulnerable_sample.py
BIG multi-vulnerability file for AST -> Neo4j graph testing.

Contains:
- Hard-coded secrets (CWE-259 / CWE-798)
- SQL Injection (CWE-89)
- Command Injection (CWE-78)
- Eval Injection (CWE-94)
- Insecure Deserialization (CWE-502)
- Path Traversal (CWE-22)
- Weak Hashing (CWE-327)
- Reflected XSS-like behavior (CWE-79-ish)
- Lots of helper functions to create more nodes/edges

DO NOT USE IN PRODUCTION.
"""

import os
import sqlite3
import subprocess
import pickle
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# ============================================================
# GLOBAL CONSTANTS / SECRETS (good for Variable nodes)
# ============================================================

DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "SuperSecretPassword123!"   # hard-coded password
API_KEY = "AKIAEXAMPLEKEY1234567890"      # looks like key
JWT_SECRET = "jwt-signing-secret"
MASTER_SECRET_KEY = "MASTER_KEY_ABC_999"
SERVICE_TOKEN = "service-token-xyz"

DEFAULT_DIR = "/var/data/"
LOG_FILE = "app.log"
DEBUG_MODE = "true"


# ============================================================
# UTILITY / LOGGING
# ============================================================

def log_info(msg):
    with open(LOG_FILE, "a") as f:
        f.write("[INFO] " + msg + "\n")


def log_error(msg):
    with open(LOG_FILE, "a") as f:
        f.write("[ERROR] " + msg + "\n")


def weak_hash(data):
    """
    Weak hashing (MD5, unsalted) – CWE-327.
    """
    return hashlib.md5(data.encode()).hexdigest()


def strong_hash(data):
    """
    Fake 'strong' hash just to create extra nodes.
    """
    return hashlib.sha256(data.encode()).hexdigest()


# ============================================================
# DATABASE LAYER (with SQL injection)
# ============================================================

def get_db_connection():
    """
    In-memory DB for demo.
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.execute("INSERT INTO users (username, password) VALUES ('alice', 'pass1')")
    cur.execute("INSERT INTO users (username, password) VALUES ('bob', 'pass2')")
    conn.commit()
    return conn


def unsafe_find_user(conn, username):
    """
    SQL Injection via string formatting – CWE-89.
    """
    query = f"SELECT id, username, password FROM users WHERE username = '{username}';"
    log_info(f"Executing query: {query}")
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def safe_find_user(conn, username):
    """
    Safe query using parameterization.
    """
    query = "SELECT id, username, password FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchall()


def unsafe_authenticate(conn, username, password):
    """
    Chains SQL injection with weak hashing.
    """
    hashed = weak_hash(password)
    query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{hashed}'"
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchone()


# ============================================================
# COMMAND EXECUTION (CWE-78)
# ============================================================

def list_directory(user_input):
    """
    Command injection with os.system.
    """
    cmd = "ls -la " + user_input
    log_info("Running command: " + cmd)
    os.system(cmd)


def run_arbitrary_command(cmd):
    """
    Command injection with subprocess.Popen.
    """
    log_info("Popen command: " + cmd)
    subprocess.Popen(cmd, shell=True)


def safe_list_directory():
    """
    Safe version – but still a node.
    """
    os.system("ls -la .")


# ============================================================
# PATH TRAVERSAL (CWE-22)
# ============================================================

def read_user_file(filename):
    """
    Vulnerable: simple concatenation of path and filename.
    """
    path = DEFAULT_DIR + filename
    with open(path, "r") as f:
        data = f.read()
    return data


def safe_read_user_file(filename):
    """
    Safe-ish, just for extra nodes.
    """
    base = os.path.abspath(DEFAULT_DIR)
    joined = os.path.abspath(os.path.join(base, filename))
    if not joined.startswith(base):
        raise ValueError("Invalid path")
    with open(joined, "r") as f:
        return f.read()


# ============================================================
# EVAL INJECTION (CWE-94)
# ============================================================

def calculate_expression(expr):
    """
    Direct eval on user expression.
    """
    log_info("Evaluating expression: " + expr)
    return eval(expr)


def safe_calculate_expression(expr):
    """
    Fake safe version.
    """
    allowed = {"x": 1, "y": 2}
    if expr not in allowed:
        return None
    return allowed[expr]


# ============================================================
# INSECURE DESERIALIZATION (CWE-502)
# ============================================================

def load_profile(raw_bytes):
    """
    Using pickle.loads on untrusted bytes.
    """
    profile = pickle.loads(raw_bytes)
    return profile


def safe_load_profile(raw_bytes):
    """
    Stub for safe version.
    """
    return {"status": "disabled"}


# ============================================================
# SIMPLE AUTH FLOWS (HARD-CODED + CALL CHAINS)
# ============================================================

def check_hardcoded_password(pwd):
    """
    Directly compares with a hard-coded secret.
    """
    if pwd == DB_PASSWORD:
        log_info("Authenticated with hard-coded DB password")
        return True
    return False


def login_flow_with_hardcode(user_input_pwd):
    """
    Login flow that calls check_hardcoded_password.
    """
    if check_hardcoded_password(user_input_pwd):
        return "OK"
    return "DENY"


def login_flow_with_hash(user_input_pwd):
    """
    Another flow using weak hash and a constant.
    """
    stored_hash = weak_hash("SuperSecretPassword123!")
    given_hash = weak_hash(user_input_pwd)
    if stored_hash == given_hash:
        log_info("Weak-hash based login success")
        return True
    return False


# ============================================================
# HTTP HANDLER (Reflected XSS-like)
# ============================================================

class VulnerableHandler(BaseHTTPRequestHandler):
    """
    Simple handler that reflects input without sanitization.
    """

    def do_GET(self):
        query = self.path.split("?", 1)[-1] if "?" in self.path else ""
        params = parse_qs(query)
        name = params.get("name", [""])[0]
        msg = "<html><body>Hello " + name + "</body></html>"  # reflected
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(msg.encode("utf-8"))


def start_test_server():
    """
    Helper to start HTTP server (not called by default).
    """
    httpd = HTTPServer(("localhost", 8081), VulnerableHandler)
    try:
        log_info("Starting vulnerable HTTP server on :8081")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


# ============================================================
# EXTRA HELPERS (more nodes & edges)
# ============================================================

def helper_transform_username(username):
    return username.strip().lower()


def helper_build_greeting(username):
    return "Welcome " + username


def chain_of_calls_example(username):
    """
    Intentionally long chain to create multiple CALL edges.
    """
    u1 = helper_transform_username(username)
    g = helper_build_greeting(u1)
    log_info("Greeting built: " + g)
    return g


def debug_dump_state():
    """
    Extra function just for graph noise.
    """
    s1 = "STATE_DEBUG"
    s2 = "USER_COUNT_UNKNOWN"
    s3 = "LAST_ERROR_NONE"
    return s1 + s2 + s3


# ============================================================
# MAIN EXECUTION ENTRY
# ============================================================

def main_demo():
    """
    Simulate attacker flows.
    This will create realistic call chains for Neo4j.
    """
    log_info("Starting main_demo")
    conn = get_db_connection()

    # SQL Injection example
    malicious_name = "alice'; DROP TABLE users; --"
    try:
        rows = unsafe_find_user(conn, malicious_name)
        print("Unsafe user lookup result:", rows)
    except Exception as e:
        log_error("SQL error: " + str(e))

    # Command injection
    list_directory("; echo HACKED_BY_CMD")

    # Eval injection
    try:
        print("Eval result:", calculate_expression("2+3*4"))
    except Exception as e:
        log_error("Eval error: " + str(e))

    # Deserialization
    raw = pickle.dumps({"role": "attacker", "debug": True})
    print("Loaded profile:", load_profile(raw))

    # Hard-coded password flow
    print("Login with hard-coded flow:", login_flow_with_hardcode("SuperSecretPassword123!"))

    # Hash-based login flow
    print("Weak hash login:", login_flow_with_hash("SuperSecretPassword123!"))

    # Extra chain
    print(chain_of_calls_example("  Alice  "))

    debug_dump_state()
    log_info("main_demo finished")


if __name__ == "__main__":
    main_demo()
