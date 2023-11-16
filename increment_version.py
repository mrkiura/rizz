import toml

# Load the pyproject.toml file
with open("pyproject.toml", "r") as file:
    pyproject = toml.load(file)

# Get the current version number
version = pyproject["project"]["version"]

# Split the version number into major, minor, and patch
major, minor, patch = map(int, version.split("."))

# Increment the patch number
patch += 1

# Update the version number in the pyproject dictionary
pyproject["project"]["version"] = f"{major}.{minor}.{patch}"

# Write the updated pyproject back to the file
with open("pyproject.toml", "w") as file:
    toml.dump(pyproject, file)