# vuln_graph_loader.py
# Neo4j + AST analyzer (updated for new vulnerability file)

import ast
from neo4j import GraphDatabase

AURA_URI = "neo4j+s://4259b476.databases.neo4j.io"
AURA_USER = "neo4j"
AURA_PASSWORD = "ZeiddFrukfPm9k3u3jnv4FvNLSV-8yLqfpMxZM2eUHg"

driver = GraphDatabase.driver(AURA_URI, auth=(AURA_USER, AURA_PASSWORD))


# ============================================================
# AST PARSER
# ============================================================
class CodeGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.functions = set()
        self.calls = []       # (caller, callee)
        self.variables = []   # (var_name, var_value)

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    self.calls.append((node.name, child.func.id))
                elif isinstance(child.func, ast.Attribute):
                    self.calls.append((node.name, child.func.attr))
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self.variables.append((t.id, node.value.value))
        self.generic_visit(node)


# ============================================================
# GRAPH BUILDER
# ============================================================
def build_graph_from_code(source_code):
    tree = ast.parse(source_code)
    builder = CodeGraphBuilder()
    builder.visit(tree)
    return builder


# ============================================================
# UPLOAD TO NEO4J
# ============================================================
def upload_to_neo4j(builder):
    with driver.session() as session:

        session.run("MATCH (n) DETACH DELETE n")

        for f in builder.functions:
            session.run("MERGE (fn:Function {name:$x})", x=f)

        for var, val in builder.variables:
            session.run("MERGE (v:Variable {name:$n}) SET v.value=$v", n=var, v=val)

        for caller, callee in builder.calls:
            session.run("""
                MERGE (a:Function {name:$c1})
                MERGE (b:Function {name:$c2})
                MERGE (a)-[:CALLS]->(b)
            """, c1=caller, c2=callee)


# ============================================================
# SCANNER
# ============================================================
def detect_vulnerabilities():
    with driver.session() as session:

        # Hardcoded secrets
        print("\n=== Hardcoded Secrets ===")
        q = """
        MATCH (v:Variable)
        WHERE toLower(v.value) =~ '.*(password|secret|key|token).*'
        RETURN v
        """
        for r in session.run(q):
            print(r["v"])

        # Dangerous function calls
        print("\n=== Dangerous Calls ===")
        q = """
        MATCH (a:Function)-[:CALLS]->(b:Function)
        WHERE toLower(b.name) IN ['eval','popen','system','loads']
        RETURN a.name AS caller, b.name AS callee
        """
        for r in session.run(q):
            print(r)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    with open("Juliet_Vuln_Code.py", "r") as f:
        code = f.read()

    builder = build_graph_from_code(code)

    print("Functions:", builder.functions)
    print("Calls:", builder.calls)
    print("Vars:", builder.variables)

    upload_to_neo4j(builder)
    detect_vulnerabilities()

    driver.close()
