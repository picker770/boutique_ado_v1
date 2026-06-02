from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ View all products """

    products = Product.objects.all()

    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(
                category__name__in=categories,
                category__isnull=False
            )
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']

            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if 'sort' in request.GET:
            sortkey = request.GET.get('sort')
            direction = request.GET.get('direction', 'asc')

            if sortkey == 'name':
                products = products.annotate(lower_name=Lower('name'))
                sortkey = 'lower_name'

            elif sortkey == 'category':
                sortkey = 'category__name'

            elif sortkey == 'price':
                sortkey = 'price'

            elif sortkey == 'rating':
                sortkey = 'rating'

            else:
                products = products.annotate(lower_name=Lower('name'))
                sortkey = 'lower_name'

            if direction == 'desc':
                sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)
            sort = sortkey

    current_sorting = f'{sort}_{direction}'

    return render(request, 'products/products.html', {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    })


def product_detail(request, product_id):
    """ Single product view """

    product = get_object_or_404(Product, pk=product_id)

    return render(request, 'products/product_detail.html', {
        'product': product,
    })


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can do that.")
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Form invalid.")
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can do that.")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Update failed.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product,
    })


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can do that.")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()

    messages.success(request, "Product deleted!")
    return redirect(reverse('products'))