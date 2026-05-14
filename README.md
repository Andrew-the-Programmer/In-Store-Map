tables

- shops (shop_id, shop_name, shop_description, tags)
- products (product_id, product_name, product_description, tags)
- voxels (voxel_id, shop_id, pr, oduct, voxel_description, x: R3, dx: R3, tags)

tags: lost[str], f.e. "parent::child" (like in anki)

/data/?{query}
e. query: "table=shops shop_id=1234 tag1 tag2"


