from catalog.models import Collection, Color, Feature, Material, Product, Tag


materials = [
    "Дерево",
    "МДФ",
    "Металл",
    "Стекло",
    "Ткань",
    "Кожа",
    "Шпон",
]

colors = [
    ("Белый", "#ffffff"),
    ("Черный", "#000000"),
    ("Серый", "#9e9e9e"),
    ("Бежевый", "#f5f5dc"),
    ("Коричневый", "#8b5a2b"),
    ("Зеленый", "#2e7d32"),
    ("Синий", "#1976d2"),
]

tags = ["new", "sale", "popular", "eco", "premium"]

collections = {
    "Сканди": "scandi",
    "Лофт": "loft",
    "Минимал": "minimal",
    "Классика": "classic",
}


def ensure_objects():
    mat_objs = {m: Material.objects.get_or_create(title=m)[0] for m in materials}
    color_objs = {
        title: Color.objects.get_or_create(title=title, defaults={"hex_code": hex_code})[0]
        for title, hex_code in colors
    }
    tag_objs = {t: Tag.objects.get_or_create(title=t)[0] for t in tags}
    col_objs = {}
    for title, slug in collections.items():
        obj = Collection.objects.filter(slug=slug).first()
        if not obj:
            obj = Collection.objects.filter(title=title).first()
            if obj and not obj.slug:
                obj.slug = slug
                obj.save(update_fields=["slug"])
            if not obj:
                obj = Collection.objects.create(title=title, slug=slug)
        if obj.title != title:
            obj.title = title
            obj.save(update_fields=["title"])
        col_objs[title] = obj
    return mat_objs, color_objs, tag_objs, col_objs


def assign_collection(product, col_objs, title):
    if product.collection_id:
        return
    if ("лофт" in title) or ("loft" in title):
        product.collection = col_objs["Лофт"]
    elif ("scandi" in title) or ("сканди" in title):
        product.collection = col_objs["Сканди"]
    elif ("minimal" in title) or ("минимал" in title):
        product.collection = col_objs["Минимал"]
    else:
        product.collection = col_objs["Классика"]
    product.save(update_fields=["collection"])


def pick_materials(title, mat_objs):
    mats = set()
    if any(k in title for k in ["диван", "sofa", "кресло", "chair", "bed", "кровать"]):
        mats.update([mat_objs["Ткань"], mat_objs["Дерево"]])
    if any(k in title for k in ["стол", "table", "desk"]):
        mats.update([mat_objs["Дерево"], mat_objs["Металл"]])
    if any(k in title for k in ["шкаф", "wardrobe", "тумба", "shelf", "стеллаж"]):
        mats.update([mat_objs["МДФ"], mat_objs["Шпон"]])
    if not mats:
        mats.add(mat_objs["Дерево"])
    return mats


def pick_tags(product, title, tag_objs):
    tset = []
    if product.price and product.price < 50000:
        tset.append(tag_objs["sale"])
    if product.year and product.year >= 2025:
        tset.append(tag_objs["new"])
    if ("sofa" in title) or ("диван" in title):
        tset.append(tag_objs["popular"])
    if not tset:
        tset.append(tag_objs["eco"])
    return tset


def upsert_features(product, title):
    if ("диван" in title) or ("sofa" in title):
        dims = ("220 см", "90 см", "95 см")
    elif ("кровать" in title) or ("bed" in title):
        dims = ("180 см", "110 см", "210 см")
    elif ("стол" in title) or ("table" in title) or ("desk" in title):
        dims = ("140 см", "75 см", "80 см")
    elif ("кресло" in title) or ("chair" in title):
        dims = ("80 см", "90 см", "80 см")
    elif ("шкаф" in title) or ("wardrobe" in title) or ("стеллаж" in title) or ("shelf" in title):
        dims = ("100 см", "200 см", "45 см")
    else:
        dims = ("120 см", "90 см", "60 см")

    Feature.objects.update_or_create(
        product=product,
        name="Ширина",
        defaults={"value": dims[0]},
    )
    Feature.objects.update_or_create(
        product=product,
        name="Высота",
        defaults={"value": dims[1]},
    )
    Feature.objects.update_or_create(
        product=product,
        name="Глубина",
        defaults={"value": dims[2]},
    )


def run():
    mat_objs, color_objs, tag_objs, col_objs = ensure_objects()
    color_list = list(color_objs.values())

    for product in Product.objects.all():
        title = product.title.lower()
        assign_collection(product, col_objs, title)
        product.materials.set(pick_materials(title, mat_objs))

        idx = product.id % len(color_list)
        product.colors.set([color_list[idx], color_list[(idx + 2) % len(color_list)]])

        product.tags.set(pick_tags(product, title, tag_objs))
        upsert_features(product, title)

    print("materials", Material.objects.count())
    print("colors", Color.objects.count())
    print("tags", Tag.objects.count())
    print("collections", Collection.objects.count())
    print("products", Product.objects.count())
    print("products_with_materials", Product.objects.filter(materials__isnull=False).distinct().count())


run()
