import datetime

nightly_build_suffix = "dev" + datetime.datetime.today().strftime("%Y%m%d")

new_setup_lines = []
with open("./setup.py", "r") as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith("VERSION ="):
            version_var, version_num = line.strip("\n").strip(" ").split("=")
            line = version_var + "=" + '"' + version_num[1:-2] + nightly_build_suffix + '"'
        new_setup_lines.append(line + "\n")

with open("./setup.py", 'w') as f:
    for line in new_setup_lines:
        f.write(line)


