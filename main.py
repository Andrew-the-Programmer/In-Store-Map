from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import json, os, pathlib

app = FastAPI()

pathlib.Path("data").mkdir(exist_ok=True)
pathlib.Path("static/svgs").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PRODUCTS_FILE = "data/products.json"
VOXELS_FILE = "data/voxels.json"


def read_json(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def opt_float(s: Optional[str]) -> Optional[float]:
    return float(s) if s and s.strip() != "" else None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/table", response_class=HTMLResponse)
async def table_view(request: Request):
    products = read_json(PRODUCTS_FILE)
    voxels = {v["product_id"]: v for v in read_json(VOXELS_FILE)}
    rows = [{**p, **voxels.get(p["product_id"], {})} for p in products]
    return templates.TemplateResponse("table.html", {"request": request, "rows": rows})


@app.get("/form", response_class=HTMLResponse)
async def form_new(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "p": None, "v": None})


@app.get("/form/{product_id}", response_class=HTMLResponse)
async def form_edit(request: Request, product_id: str):
    products = read_json(PRODUCTS_FILE)
    voxels = {v["product_id"]: v for v in read_json(VOXELS_FILE)}
    p = next((x for x in products if x["product_id"] == product_id), None)
    if not p:
        raise HTTPException(404)
    return templates.TemplateResponse("form.html", {"request": request, "p": p, "v": voxels.get(product_id)})


@app.post("/product/new")
async def create_product(
    product_id: str = Form(...),
    name: str = Form(...),
    svg_filepath: str = Form(""),
    description: str = Form(""),
    color: str = Form("#4f46e5"),
    x: float = Form(...),
    y: float = Form(...),
    z: Optional[str] = Form(None),
    dx: float = Form(...),
    dy: float = Form(...),
    dz: Optional[str] = Form(None),
):
    products = read_json(PRODUCTS_FILE)
    if any(p["product_id"] == product_id for p in products):
        raise HTTPException(400, "product_id already exists")
    products.append({
        "product_id": product_id, "name": name,
        "svg_filepath": svg_filepath, "description": description, "color": color,
    })
    write_json(PRODUCTS_FILE, products)

    voxels = read_json(VOXELS_FILE)
    voxels.append({
        "product_id": product_id,
        "x": x, "y": y, "z": opt_float(z),
        "dx": dx, "dy": dy, "dz": opt_float(dz),
    })
    write_json(VOXELS_FILE, voxels)
    return RedirectResponse("/table", status_code=303)


@app.post("/product/{product_id}/edit")
async def edit_product(
    product_id: str,
    name: str = Form(...),
    svg_filepath: str = Form(""),
    description: str = Form(""),
    color: str = Form("#4f46e5"),
    x: float = Form(...),
    y: float = Form(...),
    z: Optional[str] = Form(None),
    dx: float = Form(...),
    dy: float = Form(...),
    dz: Optional[str] = Form(None),
):
    products = read_json(PRODUCTS_FILE)
    for p in products:
        if p["product_id"] == product_id:
            p.update({"name": name, "svg_filepath": svg_filepath,
                      "description": description, "color": color})
    write_json(PRODUCTS_FILE, products)

    voxels = read_json(VOXELS_FILE)
    updated = False
    for v in voxels:
        if v["product_id"] == product_id:
            v.update({"x": x, "y": y, "z": opt_float(z), "dx": dx, "dy": dy, "dz": opt_float(dz)})
            updated = True
    if not updated:
        voxels.append({"product_id": product_id, "x": x, "y": y, "z": opt_float(z),
                       "dx": dx, "dy": dy, "dz": opt_float(dz)})
    write_json(VOXELS_FILE, voxels)
    return RedirectResponse("/table", status_code=303)


@app.post("/product/{product_id}/delete")
async def delete_product(product_id: str):
    write_json(PRODUCTS_FILE, [p for p in read_json(PRODUCTS_FILE) if p["product_id"] != product_id])
    write_json(VOXELS_FILE, [v for v in read_json(VOXELS_FILE) if v["product_id"] != product_id])
    return RedirectResponse("/table", status_code=303)


def get_map_items():
    products = {p["product_id"]: p for p in read_json(PRODUCTS_FILE)}
    return [{**products[v["product_id"]], **v}
            for v in read_json(VOXELS_FILE) if v["product_id"] in products]


@app.get("/map2d", response_class=HTMLResponse)
async def map2d(request: Request):
    return templates.TemplateResponse("map2d.html", {
        "request": request, "items_json": json.dumps(get_map_items())
    })


@app.get("/map3d", response_class=HTMLResponse)
async def map3d(request: Request):
    return templates.TemplateResponse("map3d.html", {
        "request": request, "items_json": json.dumps(get_map_items())
    })
