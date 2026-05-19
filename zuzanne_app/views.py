from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string

from .forms import (
    BlogForm,
    GalleryCategoryForm,
    ContactForm,
    TestimonialForm,
    CollectionForm,
    CategoryForm,
    ProductForm,
)
from .models import Blog, GalleryCategory, Category, Contact, GalleryImage, Testimonial, Collection, Product, ProductImage


def home(request):
    # Redirect legacy old-home to active frontend homepage
    return redirect("frontend_home")


def gallery(request):
    # Redirect legacy gallery page to homepage as gallery is integrated
    messages.info(request, "Our gallery has been integrated directly into our homepage.")
    return redirect("frontend_home")


def blog_details(request, slug=None):
    # Dynamic redirect: if slug matches a blog, redirect to details page; otherwise to blog list
    if slug:
        blog = get_object_or_404(Blog, slug=slug)
        return redirect(f"/blog-details-right-sidebar.html?id={blog.id}")
    return redirect("/blog-grid-right-sidebar.html")


def contact(request):
    # Redirect legacy contact page to contact-us.html
    return redirect("/contact-us.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "authenticate/login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("admin_dashboard")

        messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, "authenticate/login.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


@login_required(login_url="admin_login")
def admin_dashboard(request):
    now = timezone.now()
    month_labels = []
    blogs_counts = []
    contacts_counts = []
    for i in range(5, -1, -1):
        month_index = now.month - i
        year = now.year
        while month_index <= 0:
            month_index += 12
            year -= 1
        target = now.replace(year=year, month=month_index)
        month_labels.append(target.strftime("%b"))
        blogs_counts.append(
            Blog.objects.filter(
                created_at__year=target.year,
                created_at__month=target.month,
            ).count()
        )
        contacts_counts.append(
            Contact.objects.filter(
                created_at__year=target.year,
                created_at__month=target.month,
            ).count()
        )

    service_labels = []
    service_counts = []
    for collection in Collection.objects.all().order_by("name")[:6]:
        service_labels.append(collection.name)
        # Note: products are now linked via categories
        products_count = Product.objects.filter(category__collection=collection).count()
        service_counts.append(products_count)
    if not service_labels:
        service_labels = ["No Data"]
        service_counts = [1]

    stats = {
        "total_collections": Collection.objects.count(),
        "total_products": Product.objects.count(),
        "products_this_month": Product.objects.filter(created_at__year=now.year, created_at__month=now.month).count(),
        "total_blogs": Blog.objects.count(),
        "blogs_this_month": Blog.objects.filter(created_at__year=now.year, created_at__month=now.month).count(),
        "total_contacts": Contact.objects.count(),
    }

    context = {
        "stats": stats,
        "recent_blogs": Blog.objects.all().order_by("-created_at")[:5],
        "recent_contacts": Contact.objects.all().order_by("-created_at")[:5],
        "recent_products": Product.objects.all().order_by("-created_at")[:5],
        "month_labels": month_labels,
        "blogs_counts": blogs_counts,
        "contacts_counts": contacts_counts,
        "service_labels": service_labels,
        "service_counts": service_counts,
    }
    return render(request, "admin_pages/dashboard.html", context)


@login_required(login_url="admin_login")
def admin_blog_list(request):
    blogs_qs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs_qs, 8)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    return render(request, "admin_pages/blog_list.html", {"blogs": blogs})


@login_required(login_url="admin_login")
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog created.")
            return redirect("admin_blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})


@login_required(login_url="admin_login")
def blog_update(request, pk):
    blog_obj = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated.")
            return redirect("admin_blog_list")
    else:
        form = BlogForm(instance=blog_obj)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog_obj})


@login_required(login_url="admin_login")
def blog_delete(request, pk):
    blog_obj = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog_obj.delete()
        messages.success(request, "Blog deleted.")
    return redirect("admin_blog_list")


@login_required(login_url="admin_login")
def category_list(request):
    categories = GalleryCategory.objects.all().order_by("name")
    return render(request, "admin_pages/category_list.html", {"categories": categories})


@login_required(login_url="admin_login")
def category_create(request):
    if request.method == "POST":
        form = GalleryCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created.")
            return redirect("category_list")
    else:
        form = GalleryCategoryForm()
    return render(request, "admin_pages/add_category.html", {"form": form})


@login_required(login_url="admin_login")
def category_update(request, pk):
    category_obj = get_object_or_404(GalleryCategory, pk=pk)
    if request.method == "POST":
        form = GalleryCategoryForm(request.POST, instance=category_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated.")
            return redirect("category_list")
    else:
        form = GalleryCategoryForm(instance=category_obj)
    return render(request, "admin_pages/add_category.html", {"form": form, "category": category_obj})


@login_required(login_url="admin_login")
def category_delete(request, pk):
    category_obj = get_object_or_404(GalleryCategory, pk=pk)
    if request.method == "POST":
        category_obj.delete()
        messages.success(request, "Category deleted.")
    return redirect("category_list")


@login_required(login_url="admin_login")
def gallery_list(request):
    categories = GalleryCategory.objects.all().prefetch_related("images").order_by("name")
    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)
        page_number = request.GET.get(f"page_{category.id}", 1)
        category_pages[category.id] = paginator.get_page(page_number)
    return render(
        request,
        "admin_pages/image_list.html",
        {"categories": categories, "category_pages": category_pages},
    )


@login_required(login_url="admin_login")
def gallery_create(request):
    categories = GalleryCategory.objects.all().order_by("name")
    if request.method == "POST":
        category_id = request.POST.get("category")
        images = request.FILES.getlist("images")
        category = GalleryCategory.objects.filter(id=category_id).first()
        if category and images:
            for image in images:
                GalleryImage.objects.create(category=category, image=image)
            messages.success(request, "Gallery images added.")
            return redirect("list_image")
        messages.error(request, "Please select category and images.")
    return render(request, "admin_pages/add_image.html", {"categories": categories})


@login_required(login_url="admin_login")
def gallery_delete(request, pk):
    image_obj = get_object_or_404(GalleryImage, pk=pk)
    if request.method == "POST":
        image_obj.delete()
        messages.success(request, "Gallery image deleted.")
    return redirect("list_image")


@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials_qs = Testimonial.objects.all().order_by("-created_at")
    paginator = Paginator(testimonials_qs, 8)
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


@login_required(login_url="admin_login")
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial created.")
            return redirect("review_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})


@login_required(login_url="admin_login")
def testimonial_update(request, pk):
    testimonial_obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated.")
            return redirect("review_list")
    else:
        form = TestimonialForm(instance=testimonial_obj)
    return render(request, "admin_pages/create_review.html", {"form": form, "testimonial": testimonial_obj})


@login_required(login_url="admin_login")
def testimonial_delete(request, pk):
    testimonial_obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial_obj.delete()
        messages.success(request, "Testimonial deleted.")
    return redirect("review_list")


@login_required(login_url="admin_login")
def contact_list(request):
    # Mark all unread messages as read
    Contact.objects.filter(is_read=False).update(is_read=True)
    contacts = Contact.objects.all().order_by("-created_at")
    return render(request, "admin_pages/view_contacts.html", {"contacts": contacts})


@login_required(login_url="admin_login")
def delete_contact(request, pk):
    contact_obj = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact_obj.delete()
        messages.success(request, "Contact deleted.")
    return redirect("contact_list")


@login_required(login_url="admin_login")
def collection_list(request):
    collections = Collection.objects.all().order_by("-created_at")
    
    paginator = Paginator(collections, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin_pages/collection_list.html", {"collections": page_obj})


@login_required(login_url="admin_login")
def collection_create(request):
    if request.method == "POST":
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Collection created successfully.")
            return redirect("collection_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CollectionForm()
    
    return render(request, "admin_pages/create_collection.html", {"form": form})


@login_required(login_url="admin_login")
def collection_update(request, pk):
    collection_obj = get_object_or_404(Collection, pk=pk)
    if request.method == "POST":
        form = CollectionForm(request.POST, request.FILES, instance=collection_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Collection updated successfully.")
            return redirect("collection_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CollectionForm(instance=collection_obj)
        
    return render(request, "admin_pages/create_collection.html", {"form": form, "collection": collection_obj})


@login_required(login_url="admin_login")
def collection_delete(request, pk):
    collection_obj = get_object_or_404(Collection, pk=pk)
    if request.method == "POST":
        collection_obj.delete()
        messages.success(request, "Collection deleted successfully.")
    return redirect("collection_list")


@login_required(login_url="admin_login")
def store_category_list(request):
    categories = Category.objects.select_related("collection").all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    collections = Collection.objects.all().order_by("name")
    return render(request, "admin_pages/store_category_list.html", {"categories": page_obj, "collections": collections})


@login_required(login_url="admin_login")
def store_category_create(request):
    collections = Collection.objects.all().order_by("name")
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Store Category created successfully.")
            return redirect("store_category_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm()
    return render(request, "admin_pages/create_store_category.html", {"form": form, "collections": collections})


@login_required(login_url="admin_login")
def store_category_update(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    collections = Collection.objects.all().order_by("name")
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Store Category updated successfully.")
            return redirect("store_category_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm(instance=category_obj)
    return render(request, "admin_pages/create_store_category.html", {"form": form, "category": category_obj, "collections": collections})


@login_required(login_url="admin_login")
def store_category_delete(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category_obj.delete()
        messages.success(request, "Store Category deleted successfully.")
    return redirect("store_category_list")


@login_required(login_url="admin_login")
def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.select_related("category__collection").prefetch_related("images").all().order_by("-created_at")
    if category_id:
        products = products.filter(category_id=category_id)
    
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    collections = Collection.objects.prefetch_related("categories").all().order_by("name")
    
    return render(request, "admin_pages/product_list.html", {
        "products": page_obj,
        "collections": collections,
        "selected_category": category_id,
    })


@login_required(login_url="admin_login")
def product_create(request):
    collections = Collection.objects.prefetch_related("categories").all().order_by("name")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_obj = form.save()
            
            images = request.FILES.getlist("images")
            for img in images:
                ProductImage.objects.create(product=product_obj, image=img)
                
            messages.success(request, "Product created successfully.")
            return redirect("product_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
        
    return render(request, "admin_pages/create_product.html", {"form": form, "collections": collections})


@login_required(login_url="admin_login")
def product_update(request, pk):
    product_obj = get_object_or_404(Product, pk=pk)
    collections = Collection.objects.prefetch_related("categories").all().order_by("name")
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product_obj)
        if form.is_valid():
            product_obj = form.save()
            
            images = request.FILES.getlist("images")
            if images:
                for img in images:
                    ProductImage.objects.create(product=product_obj, image=img)
                    
            messages.success(request, "Product updated successfully.")
            return redirect("product_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product_obj)
        
    return render(request, "admin_pages/create_product.html", {"form": form, "product": product_obj, "collections": collections})


@login_required(login_url="admin_login")
def product_delete(request, pk):
    product_obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product_obj.delete()
        messages.success(request, "Product deleted successfully.")
    return redirect("product_list")


@login_required(login_url="admin_login")
def product_image_delete(request, pk):
    img = get_object_or_404(ProductImage, pk=pk)
    img.delete()
    messages.success(request, "Product image deleted successfully.")
    return redirect("product_list")


def frontend_home(request):
    products = Product.objects.select_related("category").prefetch_related("images").all()[:15]
    return render(request, 'frontend/index.html', {"products": products})


def frontend_page(request, page_name):
    if page_name == "shop":
        collection_id = request.GET.get("collection_id")
        category_id = request.GET.get("category_id")
        title = "Shop"
        collection = None
        categories = []

        products = Product.objects.select_related(
            "category__collection"
        ).prefetch_related("images").all()

        if collection_id:
            collection = get_object_or_404(
                Collection, id=collection_id)
            products = products.filter(
                category__collection=collection)
            title = collection.name
            categories = Category.objects.filter(
                collection=collection).order_by("name")
        elif category_id:
            cat = get_object_or_404(Category, id=category_id)
            products = products.filter(category=cat)
            title = cat.name
            collection = cat.collection
            categories = Category.objects.filter(
                collection=collection).order_by("name")

        return render(request, "frontend/shop.html", {
            "products": products,
            "shop_title": title,
            "collection": collection,
            "categories": categories,
            "selected_collection_id": collection_id,
            "selected_category_id": category_id,
        })

    if page_name == "blog-grid-right-sidebar":
        blogs_list = Blog.objects.all().order_by("-created_at")
        
        # Paginate 4 blogs per page
        paginator = Paginator(blogs_list, 4)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
        if is_ajax:
            html = render_to_string("frontend/partials/blog_items.html", {"blogs": page_obj})
            return JsonResponse({
                "html": html,
                "has_next": page_obj.has_next(),
                "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None
            })
            
        recent_blogs = blogs_list[:3]
        return render(request, "frontend/blog-grid-right-sidebar.html", {
            "blogs": page_obj,
            "recent_blogs": recent_blogs
        })

    if page_name == "blog-details-right-sidebar":
        blog_id = request.GET.get('id')
        blog = None
        if blog_id:
            try:
                blog = Blog.objects.get(id=blog_id)
            except (Blog.DoesNotExist, ValueError):
                pass
        if not blog:
            blog = Blog.objects.all().order_by("-created_at").first()
            
        # Get up to 2 related blogs (excluding the current blog)
        related_blogs = Blog.objects.exclude(id=blog.id).order_by("-created_at")[:2] if blog else Blog.objects.all().order_by("-created_at")[1:3]
        recent_blogs = Blog.objects.all().order_by("-created_at")[:3]
        
        return render(request, "frontend/blog-details-right-sidebar.html", {
            "blog": blog,
            "related_blogs": related_blogs,
            "recent_blogs": recent_blogs
        })

    if request.method == "POST" and page_name == "contact-us":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not first_name or not last_name or not phone or not email or not message:
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                Contact.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    message=message,
                    best_time_to_contact="Anytime"
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Failed to submit message: {str(e)}")

        return redirect(request.path)

    if page_name == "about-us-2":
        testimonials = Testimonial.objects.all().order_by("-created_at")
        return render(request, "frontend/about-us-2.html", {
            "testimonials": testimonials
        })

    try:
        return render(request, f"frontend/{page_name}.html")
    except TemplateDoesNotExist:
        raise Http404("Template not found")


def product_detail_view(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("images"), slug=slug)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        product_name = request.POST.get("product_name", "").strip()
        if first_name and phone and message:
            Contact.objects.create(
                first_name=first_name,
                last_name="",
                phone=phone,
                email=email,
                message=f"Product Enquiry: {product_name}\n\n{message}",
            )
            messages.success(request, "Your enquiry has been sent successfully!")
        else:
            messages.error(request, "Please fill in all required fields.")
        return redirect(request.path)

    recommended_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).prefetch_related("images")[:6]

    sizes_list = [
        s.strip() for s in product.available_sizes.split(',')
    ] if product.available_sizes else []

    return render(
        request,
        "frontend/product-details-fullwidth.html",
        {
            "product": product,
            "recommended_products": recommended_products,
            "sizes_list": sizes_list,
        }
    )


def frontend_page_unused(request, page_name):
    if page_name == "product-details":
        product_id = request.GET.get('id')
        product = None
        if product_id:
            try:
                product = Product.objects.prefetch_related("images").get(id=product_id)
            except (Product.DoesNotExist, ValueError):
                pass
        if not product:
            product = Product.objects.prefetch_related("images").first()
            
        # Get up to 6 recommended products from the same category
        recommended_products = []
        sizes_list = []
        if product:
            recommended_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]
            sizes_list = [s.strip() for s in product.available_sizes.split(',')] if product.available_sizes else []
            
        return render(request, "frontend/unused/product-details.html", {
            "product": product,
            "recommended_products": recommended_products,
            "sizes_list": sizes_list,
        })

    if page_name == "portfolio-3-columns":
        collections = Collection.objects.all().order_by("name")
        return render(request, "frontend/unused/portfolio-3-columns.html", {
            "collections_tree": collections,
        })

    try:
        return render(request, f"frontend/unused/{page_name}.html")
    except TemplateDoesNotExist:
        raise Http404("Template not found")

def custom_404_view(request, exception=None):
    return render(request, 'frontend/404.html', status=404)
