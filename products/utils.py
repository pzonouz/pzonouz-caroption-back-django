from django.db import transaction

from entities.models import Entity
from products.models import PEVGEOT_OLD_NAME, Product


def calculate_price_with_cover(product, entity):
    english_name = entity.english_name
    if english_name == PEVGEOT_OLD_NAME:
        return product.price + 1000000


def calculate_price_with_cover_and_install(product, entity):
    english_name = entity.english_name
    if english_name == PEVGEOT_OLD_NAME:
        return product.price + 3000000


@transaction.atomic
def sync_entity_products():
    # Step 1: Fetch all children entities in one query
    children = Entity.objects.filter(parent__isnull=False)

    # Step 2: Fetch all main products
    main_products = Product.objects.filter(generated=False, generatable=True)

    # Step 3: Create the new product combinations
    new_products = []
    existing = set(
        Product.objects.filter(main_product__isnull=False).values_list(
            "main_product_id", "entity_id"
        )
    )
    for child in children:
        for main in main_products:
            key = (main.id, child.id)  # type: ignore[reportIncompatibleVariableOverride]
            if key not in existing:  # only create missing on
                product_name = f"{main.name} {child.name}"  # type: ignore[reportIncompatibleVariableOverride]
                new_products.append(
                    Product(
                        name=product_name, main_product_id=main.id, entity_id=child.id, generated=True, image_url=child.image_url, price2=calculate_price_with_cover(product=main, entity=child), price3=calculate_price_with_cover_and_install(product=main, entity=child)  # type: ignore[reportIncompatibleVariableOverride]
                    )
                )

    # Step 4: Bulk insert in one query
    Product.objects.bulk_create(
        new_products, ignore_conflicts=True
    )  # ignore_conflicts avoids duplicates


@transaction.atomic
def update_all_derived_products():
    # Step 1: Fetch all derived products with their main product and entity in one query
    derived_products = Product.objects.select_related("main_product", "entity").filter(
        main_product__isnull=False
    )

    # Step 2: Update their names
    for dp in derived_products:
        dp.name = f"{dp.main_product.name} {dp.entity.name}"
        dp.image_url = dp.entity.image_url
        dp.price2 = calculate_price_with_cover(
            product=dp.main_product, entity=dp.entity
        )
        dp.price3 = calculate_price_with_cover_and_install(
            product=dp.main_product, entity=dp.entity
        )

    # Step 3: Bulk update in one query
    Product.objects.bulk_update(
        derived_products, ["name", "image_url", "price2", "price3"]
    )
