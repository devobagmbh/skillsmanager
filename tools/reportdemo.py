from dataclasses import asdict, dataclass
import os
import sys
from weasyprint import HTML
from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
env = Environment(loader=PackageLoader("skillsManager"), autoescape=select_autoescape())


@dataclass
class Context:
    given_name: str = "Mr."
    last_name: str = "X"


if __name__ == "__main__":
    f = Context()
    template = env.get_template("cvreport.html")
    pdf = HTML(string=template.render(asdict(f)))
    pdf.write_pdf("export.pdf")
