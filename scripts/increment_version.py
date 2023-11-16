import toml

with open("pyproject.toml", "r") as file:
    pyproject = toml.load(file)

version = pyproject["project"]["version"]

major, minor, patch = map(int, version.split("."))

patch += 1

pyproject["project"]["version"] = f"{major}.{minor}.{patch}"

with open("pyproject.toml", "w") as file:
    toml.dump(pyproject, file)
