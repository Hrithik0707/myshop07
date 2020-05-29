from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,OrderItem, Order
from .forms import UploadProduct
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'website/index.html',{'products':products})

class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "website/index.html"

def upload_prod(request):
    if request.method == 'POST':
        u_form = UploadProduct(request.POST,request.FILES or None)
        if u_form.is_valid():
            prod = u_form.save()
            prod.save()
            messages.success(request, f'Your product has been uploaded!')
            return redirect('upload')
    else:
        u_form = UploadProduct()
    return render(request,'website/upload.html',{'u_form':u_form})

class ProductDetailView(DetailView):
    model = Product
    template_name = "website/prod.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")

def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'website/ordersummary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("Website-index")