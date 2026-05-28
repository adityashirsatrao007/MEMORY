# docs/generate_architecture.py
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.programming.language import Nodejs, Javascript

graph_attr = {
    "fontsize": "14",
    "bgcolor": "#1C1C1E",        # dark background matching Apple HIG
    "fontcolor": "white",
    "pad": "0.5",
    "splines": "curved",
    "nodesep": "0.6",
    "ranksep": "0.8",
}

with Diagram(
    "Remix Docs Site Architecture",
    filename="docs/images/architecture",   # saves as architecture.png
    outformat="png",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
):
    users = Users("Web Browser\n(Client)")

    with Cluster("Express Server Environment (PM2 Managed)"):
        express = Nodejs("Express.js App\n(Port 3010)")
        
        with Cluster("Static Assets"):
            html = Javascript("index.html\n(Structure)")
            css = Javascript("index.css\n(Design System)")
            js = Javascript("index.js\n(Interactions)")

    users >> Edge(label="HTTP GET /", color="#57cda4", fontcolor="#57cda4") >> express
    express >> Edge(color="#dee2e6") >> [html, css, js]
    html >> Edge(label="Rendered UI", color="#57cda4", fontcolor="#57cda4") >> users

print("✅ docs/images/architecture.png generated")
