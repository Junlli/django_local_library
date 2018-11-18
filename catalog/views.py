from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.core.paginator import Paginator
from django.shortcuts import render
def index(request, page_number = '1'):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()  # 获取记录计数（书本）
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    book_list = Book.objects.all()
    p = Paginator(book_list, 20)
    current_page = p.page(int(page_number))


    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genres': num_genres, 'num_visits': num_visits, 'book_list': book_list, 'pages': p,
                 'current_page': current_page})


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 10  # 数据超过10条，就进行分页

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book

    # def book_detail_view(request, pk):
    #     try:
    #         book_id = Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         raise Http404("Book does not exist")
    #
    #     # book_id=get_object_or_404(Book, pk=pk)
    #
    #     return render(
    #         request,
    #         'catalog/book_detail.html',
    #         context={'book': book_id, }
    #     )


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)  # 从模型返回指定的对象，不存在则返回404

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))  # 创建指向指定URL的重定向

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.contrib.auth.mixins import PermissionRequiredMixin


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    fields = '__all__'  # 包含所有字段
    initial = {'date_of_death': ''}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    success_url = reverse_lazy('authors')
    # 在删除作者后，重定向到我们的作者列表 -  reverse_lazy()是一个延迟执行的reverse()版本，在这里使用，是因为我们提供了一个基于类的 URL 查看属性


from .models import Book


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Book
    success_url = reverse_lazy('books')


class Xiaoshuo(generic.ListView):
    model = Book
    template_name = 'catalog/xiaoshuowenxue.html'  # Specify your own template name/location


class Zhuanji(generic.ListView):
    model = Book
    template_name = 'catalog/mingrenzhuanji.html'  # Specify your own template name/location


class Xuexi(generic.ListView):
    model = Book
    template_name = 'catalog/xuexijiaoyu.html'  # Specify your own template name/location


class Lizhi(generic.ListView):
    model = Book
    template_name = 'catalog/chenggonglizhi.html'  # Specify your own template name/location


class Ertong(generic.ListView):
    model = Book
    template_name = 'catalog/ertongduwu.html'  # Specify your own template name/location


class Shenghuo(generic.ListView):
    model = Book
    template_name = 'catalog/shenghuoshishang.html'  # Specify your own template name/location


class Renwen(generic.ListView):
    model = Book
    template_name = 'catalog/renwensheke.html'  # Specify your own template name/location


class Xinli(generic.ListView):
    model = Book
    template_name = 'catalog/xinlibaike.html'  # Specify your own template name/location