# Tables

- shops (shop_id, shop_name, shop_description, tags)

```json
[
  {
    "product_id": "1234",
    "name": "Product example",
    "svg_filepath": "",
    "description": "",
    "tags": []
  }
]
```

- products (product_id, product_name, product_description, tags)

```json
[
  {
    "shop_id": "1234",
    "name": "Dixy",
    "svg_filepath": "",
    "description": "",
    "tags": []
  }
]
```

- voxels (voxel_id, shop_id, pr, oduct, voxel_description, x: R3, dx: R3, tags)

```json
[
  {
    "product_id": "1234",
    "shop_id": "1234",
    "x": [0, 0, 0],
    "dx": [10, 10, 10],
    "tags": []
  }
]
```

tags: `list[str]`, f.e. "parent::child" (like in anki)

# /data/query
`/data/query?{query}`
query is for all tables.
f.e. query: "table=shops&shop_id=1234&tag1&tag2"

See rows as tiles (query-tiles).
Tiles are in html tag `details` and are hidden by default.
Every table has it's own tile template.
Foreign keys are clickable and lead to `/data/query?foreign_id=foreign_key`.

# Data edit

Every row's data can be modified in query-tile and changes are saved with a button in the bottom-right corner "Save changes".
Primary keys (ids) can not be modified.
Foreign keys has to be set by selecting from list of existing values.

Coordinates (column x) can be modified with input boxes or in 2d map, where you can drag to move (x,y) with lmb and resize (dx,dy) with rmb.

svg_filepath column can not be set with a path (string). You can only upload a svg file. It will be saved with unique filename.

# /data/create

To create a new row in table: `/data/create?table={table}`.
Each table has a html template create-tile, which is similar to query-tile.
Has button "Create" instead of "Save changes".
Primary key can not be seen or modified, it is generated after pressing "Create".

# /map2d

`/map2d?{query}`
query is for table voxels.
f.e. query: "shop_id=1234&product_id=1234&tag1&tag2"

Query is grouped by shop_id and each shop has it's own tile.

Shows interactive 2D map with voxels.
Each voxel has it's svg image in it's middle, scaled to it's size.
Voxel bg color is selected automatically.

# /map3d

Same as /map2d but map is in 3D.

# /camera

On mobile.
Display image from phone camera on site and put voxels in 3D.
This is hard and we should keep this in mind but not implement yet.
