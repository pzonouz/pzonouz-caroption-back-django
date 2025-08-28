from entities.models import Entity
from products.models import Product


def sync_entity_products():
    # Step 1: Fetch all children entities in one query
    children = Entity.objects.filter(parent__isnull=False)

    # Step 2: Fetch all main products
    main_products = Product.objects.filter(generated=False, generatable=True)

    # Step 3: Create the new product combinations
    new_products = []

    for child in children:
        for main in main_products:
            product_name = f"{child.name} {main.name}"  # type: ignore[reportIncompatibleVariableOverride]
            new_products.append(
                Product(
                    name=product_name, main_product_id=main.id, entity_id=child.id, generated=True, image_url=child.image_url, category=main.category  # type: ignore[reportIncompatibleVariableOverride]
                )
            )

    # Step 4: Bulk insert in one query
    Product.objects.bulk_create(
        new_products, ignore_conflicts=True
    )  # ignore_conflicts avoids duplicates
