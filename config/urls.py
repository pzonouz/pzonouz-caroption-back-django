from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from authentication.views import signup
from brands.views import BrandsViewset
from categories.views import CategoryViewSet, ParentCategoryList, products_in_category
from entities.views import EntityViewSet, ParentEntityList
from invoices.views import InvoiceItemViewset, InvoiceViewset
from parameters.views import (
    ParameterGroupViewSet,
    ParameterViewSet,
    ProductParameterValueViewSet,
    getProductParameterValuesByProduct,
)
from persons.views import PersonsViewset
from products.views import (
    ProductsViewset,
    delete_from_image_urls,
    generate_products,
    update_generated_products,
)

router = SimpleRouter()
router.register("categories", CategoryViewSet, basename="Category")
router.register("products", ProductsViewset, basename="Product")
router.register("persons", PersonsViewset, basename="Person")
router.register("brands", BrandsViewset, basename="Brand")
router.register("entities", EntityViewSet, basename="entity")
router.register("invoices", InvoiceViewset, basename="Invoice")
router.register("invoiceitems", InvoiceItemViewset, basename="InvoiceItem")
router.register("parameters", ParameterViewSet, basename="parameter")
router.register("parameter-groups", ParameterGroupViewSet, basename="parameter_group")
router.register(
    "product-parameter-values",
    ProductParameterValueViewSet,
    basename="product-parameter-value",
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("core.urls")),
    path("products_in_category/<int:pk>", products_in_category),
    path("parent_categories", ParentCategoryList.as_view()),
    path("parent_entities", ParentEntityList.as_view()),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/signup", signup),
    path("generate_products", generate_products),
    path("update_generated_products", update_generated_products),
    path(
        "delete_from_image_urls/<int:product_id>",
        delete_from_image_urls,
    ),
    path(
        "product-parameter-values/product/<int:id>", getProductParameterValuesByProduct
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
