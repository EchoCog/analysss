import re
from collections import defaultdict


def analyze_dependencies(log_file, dot_file):
    dependencies = defaultdict(set)
    with open(log_file, "r") as f:
        for line in f:
            match = re.match(r"\./(.*?\.py):from (.*?) import", line)
            if match:
                file, module = match.groups()
                dependencies[file].add(module)

    with open(dot_file, "w") as f:
        f.write("digraph G {\n")
        f.write("  rankdir=LR;\n")
        for file, modules in dependencies.items():
            for module in modules:
                f.write(f'  "{module}" -> "{file}";\n')
        f.write("}\n")


if __name__ == "__main__":
    analyze_dependencies("dependency_analysis.txt", "dependencies.dot")
