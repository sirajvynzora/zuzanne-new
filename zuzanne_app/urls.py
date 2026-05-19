from django.urls import path

from . import views

urlpatterns = [
    path("", views.frontend_home, name="frontend_home"),
    path("old-home/", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("blogs/", views.blog_details, name="blog_details"),
    path("blogs/<slug:slug>/", views.blog_details, name="blog_details_slug"),
    path("contact/", views.contact, name="contact"),

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

    # Gallery Categories
    path("dashboard/categories/", views.category_list, name="category_list"),
    path("dashboard/categories/create/", views.category_create, name="category_create"),
    path("dashboard/categories/add/", views.category_create, name="add_category"),
    path("dashboard/categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("dashboard/categories/<int:pk>/update/", views.category_update, name="update_category"),
    path("dashboard/categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("dashboard/categories/<int:pk>/remove/", views.category_delete, name="delete_category"),

    path("dashboard/gallery/", views.gallery_list, name="gallery_list"),
    path("dashboard/gallery/list/", views.gallery_list, name="list_image"),
    path("dashboard/gallery/create/", views.gallery_create, name="gallery_create"),
    path("dashboard/gallery/add/", views.gallery_create, name="add_image"),
    path("dashboard/gallery/<int:pk>/delete/", views.gallery_delete, name="gallery_delete"),
    path("dashboard/gallery/<int:pk>/remove/", views.gallery_delete, name="delete_image"),

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

    # Dynamic preview routing for frontend templates
    path("product/<slug:slug>/", views.product_detail_view, name="product_detail"),
    path("unused/<str:page_name>.html", views.frontend_page_unused, name="frontend_page_unused"),
    path("<str:page_name>.html", views.frontend_page, name="frontend_page"),
]
