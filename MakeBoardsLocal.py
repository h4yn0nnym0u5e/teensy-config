import json

menud = {
    "header":
    """## Audio
# Extra menu entries to tune the behaviour of the Audio library
""",
    "entries": [
        {
            "id": "audiorate",
            "name": "Audio sample rate",
            "boards": ["teensy41", "teensy40"],
            "options": [
                {"id": 44, "text": "44.1kHz",
                 "entries": ["build.flags.audiorate=44100.0f"]},
                {"id": 48, "text": "48kHz",
                 "entries": ["build.flags.audiorate=48000.0f"]},
                {"id": 96, "text": "96kHz",
                 "entries": ["build.flags.audiorate=96000.0f"]}
            ]
        },
        {
            "id": "audioblocksize",
            "name": "Audio block size",
            "boards": ["teensy41", "teensy40"],
            "options": [
                {"id": "normal", "text": "128 samples (normal)",
                 "entries": ["build.flags.audioblocksize=128"]},
                {"id": 16, "text": "16 samples",
                 "entries": ["build.flags.audioblocksize=16"]},
                {"id": 256, "text": "256 samples",
                 "entries": ["build.flags.audioblocksize=256"]}
            ]
        }
    ]
}

#print(json.dumps(menud,indent=2))

def json2txt(d):
    s=""
    s += d["header"]
    s += "\n"
    for e in d["entries"]:
        s += f"menu.{e['id']}={e['name']}\n"
        for b in e["boards"]:
            for o in e["options"]:
                s += f"{b}.menu.{e['id']}.{o['id']}={o['text']}\n"
                for ee in o["entries"]:
                    s += f"{b}.menu.{e['id']}.{o['id']}.{ee}\n"
        s += "\n"
    return s

menud=json.load(open("boards.local.json"))
print(json2txt(menud))
