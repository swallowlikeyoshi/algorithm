import json

Json_object = json.load(open("example.json", "r", encoding="utf8"))

print(Json_object["학교"])
print(Json_object["학년"][0])
print(Json_object["반"]["8반"][1])
print(Json_object["쿠키"])