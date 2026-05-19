from zuzanne_app.models import Contact, Collection, Category, Product

def admin_context(request):
    unread_count = 0
    try:
        unread_count = Contact.objects.filter(is_read=False).count()
    except Exception:
        pass

    collections_tree = []
    try:
        collections = Collection.objects.all().prefetch_related('categories__products')
        for col in collections:
            col_data = {
                'id': col.id,
                'name': col.name,
                'slug': col.slug,
                'cats': []
            }
            for cat in col.categories.all():
                cat_data = {
                    'id': cat.id,
                    'name': cat.name,
                    'slug': cat.slug,
                    'prods': []
                }
                for prod in cat.products.all():
                    cat_data['prods'].append({
                        'id': prod.id,
                        'name': prod.name,
                        'slug': prod.slug
                    })
                col_data['cats'].append(cat_data)
            collections_tree.append(col_data)
    except Exception as e:
        pass

    return {
        'unread_messages_count': unread_count,
        'collections_tree': collections_tree
    }

