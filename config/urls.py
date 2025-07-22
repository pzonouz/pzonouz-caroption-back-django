from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from authentication.views import signup
from categories.views import CategoryViewSet, ParentCategoryList, products_in_category
from invoices.views import InvoiceItemViewset, InvoiceViewset
from persons.views import PersonsViewset
from products.views import ProductsViewset

router = SimpleRouter()
router.register("categories", CategoryViewSet, basename="Category")
router.register("products", ProductsViewset, basename="Product")
router.register("persons", PersonsViewset, basename="Person")
router.register("invoices", InvoiceViewset, basename="Invoice")
router.register("invoiceitems", InvoiceItemViewset, basename="InvoiceItem")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("core.urls")),
    path("products_in_category/<int:pk>", products_in_category),
    path("parent_categories", ParentCategoryList.as_view()),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/signup", signup),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
