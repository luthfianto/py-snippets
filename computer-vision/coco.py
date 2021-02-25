import json

f=json.loads(open('./data/annotations/instances_default.json').read())
category_dict={c['id']: c['name'] for c in f['categories']}
image_dict = {c['id']: c['file_name'] for c in f['images']}

[
    {
        **d,
        "category_name": category_dict.get(d['category_id']),
        "file_name": image_dict.get(d['image_id'])
    }
    for d in f['annotations']
]
