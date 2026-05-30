import pathlib
p = pathlib.Path("models/primarycare_model/app.py")
c = p.read_text(encoding="utf-8")
print("tabs[11]:", c.find("tabs[11]"))
print("tabs[0]:", c.find("tabs[0]"))
print("tab_names:", c.find("tab_names"))
print("Length:", len(c))
