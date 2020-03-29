import pickle, json

# with open("jo.pkl", "rb") as f:
#     json_object = pickle.load(f)


# with open("jo.pkl", "rb") as f:
#     json_object = pickle.load(f)

with open("pretty_outfile.json", "r") as f:
    json_object = json.load(f)
print(len(json_object['data']))
