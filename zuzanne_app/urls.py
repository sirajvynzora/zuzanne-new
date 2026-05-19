from django.urls import path

from . import views

urlpatterns = [
    path("", views.frontend_home, name="frontend_home"),
    # Legacy Redirection Routes (to prevent 404/500 errors and preserve backwards compatibility)
    path("old-home/", views.home, name="home"),

    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("dashboard/blocks/", views.admin_blog_list, name="admin_blog_list"),
    path("dashboard/blogs/", views.admin_blog_list, name="admin_blog_list"),
    path("dashboard/blocks/create/", views.blog_create, name="block_create"),
    path("dashboard/blogs/create/", views.blog_create, name="blog_create"),
    path("dashboard/blocks/<int:pk>/edit/", views.blog_update, name="block_update"),
    path("dashboard/blogs/<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("dashboard/blocks/<int:pk>/delete/", views.blog_delete, name="block_delete"),
    path("dashboard/blogs/<int:pk>/delete/", views.blog_delete, name="blog_delete"),


    path("dashboard/testimonials/", views.testimonial_list, name="testimonial_list"),
    path("dashboard/reviews/", views.testimonial_list, name="review_list"),
    path("dashboard/testimonials/create/", views.testimonial_create, name="testimonial_create"),
    path("dashboard/testimonials/<int:pk>/edit/", views.testimonial_update, name="testimonial_update"),
    path("dashboard/testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),

    path("dashboard/contacts/", views.contact_list, name="contact_list"),
    path("dashboard/contacts/<int:pk>/delete/", views.delete_contact, name="delete_contact"),

    path("dashboard/collections/", views.collection_list, name="collection_list"),
    path("dashboard/collections/add/", views.collection_create, name="collection_create"),
    path("dashboard/collections/edit/<int:pk>/", views.collection_update, name="collection_update"),
    path("dashboard/collections/delete/<int:pk>/", views.collection_delete, name="collection_delete"),

    # Store Categories (New 3-Tier Hierarchy)
    path("dashboard/store-categories/", views.store_category_list, name="store_category_list"),
    path("dashboard/store-categories/add/", views.store_category_create, name="store_category_create"),
    path("dashboard/store-categories/edit/<int:pk>/", views.store_category_update, name="store_category_update"),
    path("dashboard/store-categories/delete/<int:pk>/", views.store_category_delete, name="store_category_delete"),

    path("dashboard/products/", views.product_list, name="product_list"),
    path("dashboard/products/add/", views.product_create, name="product_create"),
    path("dashboard/products/edit/<int:pk>/", views.product_update, name="product_update"),
    path("dashboard/products/delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("dashboard/products/image/delete/<int:pk>/", views.product_image_delete, name="product_image_delete"),

    # Shop & Hierarchical Filters (Unified View)
    path("shop/", views.shop_view, name="shop"),
    path("shop/<slug:collection_slug>/", views.shop_view, name="collection"),
    path("shop/<slug:collection_slug>/<slug:category_slug>/", views.shop_view, name="category"),

    # Blogs, About, and Contact clean routes
    path("blogs/", views.blog_list_view, name="blog_list"),
    path("blogs/<slug:slug>/", views.blog_detail_view, name="blog_detail"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),

    # Dynamic preview routing for frontend templates
    path("product/<slug:slug>/", views.product_detail_view, name="product_detail"),
    path("unused/<str:page_name>.html", views.frontend_page_unused, name="frontend_page_unused"),
    path("<str:page_name>.html", views.frontend_page, name="frontend_page"),
]
