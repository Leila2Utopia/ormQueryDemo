from django.shortcuts import render
from app01.models import *
from django.db.models import Q
from django.db.models import Count,Max

# Create your views here.
def query(request):

    #####################################################查询相关API###############################################################


    #all() 查询所有结果
    book_list=Book.objects.all() #<QuerySet [<Book: book1>, <Book: book2>, <Book: book3>]>

    #filter()它包含了与所给筛选条件相匹配的对象
    book_list = Book.objects.filter(id=1) #<QuerySet [<Book: book1>]>

    #get() model对象 有且只有一个查询结果时才有意义 如果超过一个或者没有都会抛出异常
    book = Book.objects.get(id=2)       #<Book: book2>


    #order_by()  model对象 对查询结果排序
    book = Book.objects.all().order_by("-id")   #<QuerySet [<Book: book3>, <Book: book2>, <Book: book1>]>

    #reverse()  对查询结果反向排序
    book = Book.objects.all().order_by("-id").reverse()

    #count()  返回匹配查询对象的数量
    book = Book.objects.all().order_by("-id").count()  #3


    #exists() 如果Queryset包含数据，则返回true，否则返回false
    book  = Book.objects.all().exists()   #True

    book = Book.objects.filter(id=20).exists()  #False

    #values()  返回一个valueQureyset 是一个可迭代的字典序列
    book = Book.objects.all().values("title")   #<QuerySet [{'title': 'book1'}, {'title': 'book2'}, {'title': 'book3'} ]>

    #values_list() 返回的是一个元组序列，values返回的是一个字典序列
    book = Book.objects.all().values_list("title") #<QuerySet [('book1',), ('book2',), ('book3',)]>

    #distinct() 从返回结果中剔除重复记录
    book = Book.objects.all().distinct()

    #first()  返回第一条记录
    book = Book.objects.all().first()  #<Book: book1>

    #last()  返回最后一条记录
    book = Book.objects.all().last()    #<Book: book6>

    #exclude() 它包含了与所给筛选条件不匹配的对象
    book = Book.objects.all().exclude(id=2)     #<QuerySet [<Book: book1>, <Book: book3>, <Book: book4>]>

    ######################################################双下划线之单表查询###############################################################

    #id 大于3且小于6的值
    book = Book.objects.filter(id__lt=6,id__gt=3)   #<QuerySet [<Book: book4>, <Book: book5>]>

    #获取id等于1、2、3的数据
    book = Book.objects.filter(id__in=[1,2,3])  #<QuerySet [<Book: book1>, <Book: book2>, <Book: book3>]>

    # not in
    book = Book.objects.filter().exclude(id__in=[1,2,3])    #<QuerySet [<Book: book4>, <Book: book5>, <Book: book6>]>

    #icontains大小写不敏感
    book = Book.objects.filter(title__contains="book")
    book = Book.objects.filter(title__icontains="book")

    # 范围bettwen and
    book = Book.objects.filter(id__range=[1,4])

    #startswith，istartswith, endswith, isendswith　

    #####################################################基于对象的跨表查询###############################################################
    # --------一对多：

    # 查询id=2的书籍的出版社的名称
    book_obj = Book.objects.filter(id=2).first()
    print(book_obj.publish.name)

    # 查询“邮电出版社”出版过的书籍名称
    publish_obj = Publish.objects.filter(name='邮电出版社').first()
    print(publish_obj.book_set.all())

    # --------多对多：
    # 查询book1所有作者的名字
    book_obj = Book.objects.filter(title="book1").first()
    print(book_obj.authors.values("name"))

    # 查询alex出版过的所有书籍名称
    author_obj = Author.objects.filter(name='alex').first()
    print(author_obj.book_set.all().values('title'))

    # --------一对一
    # 查询emai为123@qq.com的作者的名字
    authordetail_obj = AuthorDetail.objects.filter(email="123@qq.com").first()
    print(authordetail_obj.author.name)

    # 查询alex的email
    author_obj = Author.objects.filter(name='alex').first()
    print(author_obj.authordetail.email)

    ####################################################基于queryset的跨表查询######################################################################
    # 一对多：
    # 查询价格等于100的书籍的的出版社的名称
    book_obj = Book.objects.filter(price=100).values("title","publish__name")

    temp = []
    for book in Book.objects.filter(price=100):

         temp.append({
             "title":book.title,
             "publish__name":book.publish.name,
         })

    # 查询人民出版社出版过的书籍名称
    publish_obj = Publish.objects.filter(name='人民出版社').values("book__title")

    temp= []
    for book in publish_obj.book_set.all():
        temp.append({
            "book_title":book.title
        })

    # 多对多：
    # 查询book1所有作者的名字
    book_obj = Book.objects.filter(title='book1').values("authors__name")

    # 查询alex出版过的所有书籍名称
    author_obj = Author.objects.filter(name='alex').values("book__title")

    # 一对一：
    # 查询手email以1开头的作者出版过的所有书籍名称以及出版社名称
    authordetail_obj = AuthorDetail.objects.filter(email__startswith="1").values("author__book__title","author__book__publish__name")

    # 查询alex的email
    author_obj = Author.objects.filter(name='alex').values("authordetail__email")

    ############################################################task20180502#######################################################################
    # 1、查询人民出版社出版过的价格大于100的书籍的作者的email
    #基于对象查询
    publish_obj = Publish.objects.filter(name='人民出版社').first()
    book_list = publish_obj.book_set.filter(price__gt=10)
    for book_obj in book_list:
        print(book_obj.title)
        for author in book_obj.authors.all():
            print(author.name)

    #双下划线查询
    queryset_result = Book.objects.filter(price__gt=100,publish__name='人民出版社').values("authors__name")
    print(queryset_result)


    # 2、查询alex出版过的所有书籍的名称以及书籍的出版社的名称
    #基于对象查询
    author_obj = Author.objects.filter(name='alex').first()
    for book in author_obj.book_set.all():
        print(book.title,book.publish.name)

    #双下划线查询
    queryset_result = Book.objects.filter(authors__name='alex').values("title","publish__name")
    print(queryset_result)


    # 3、查询2011年出版过的所有书籍的作者名字以及出版社名称
    # 基于对象查询

    book_list = Book.objects.filter(publishDate__year='2011')
    for book_obj in book_list:
        print(book_obj.title,book_obj.publish.name)
        for author in book_obj.authors.all():
            print(author.name)

    # 双下划线查询
    queryset_result = Author.objects.filter(book__publishDate__year='2011').values("book__title","name","book__publish__name")
    print(queryset_result)

    # 4、查询住在沙河并且email以123开头的作者写过的所有书籍名称以及书籍的出版社名称
    # 基于对象查询
    authorDetail_list = AuthorDetail.objects.filter(addr='沙河',email__startswith='123')
    for authorDetail in authorDetail_list:
        print(authorDetail.author.name)
        for book in authorDetail.author.book_set.all():
            print(book.title,book.publish.name)

    # 双下划线查询
    queryset_result = AuthorDetail.objects.filter(addr='沙河',email__startswith='123').values("author__name","author__book__title","author__book__publish__name")
    print(queryset_result)

    # 5、查询年龄大于20岁的作者在哪些出版社出版过书籍
    # 基于对象查询
    author_list = Author.objects.filter(age__gt=20)
    for author in author_list:
        print(author.name)
        for book in author.book_set.all():
            print(book.title,book.publish.name)

    # 双下划线查询
    queryset_result = Author.objects.filter(age__gt=20).values("name","book__title","book__publish__name")
    print(queryset_result)

    # 6、查询每一个出版社的名称以及出版过的书籍个数
    queryset_result = Publish.objects.all().annotate(c=Count("book")).values("name","c")
    print(queryset_result)


    # 7、查询每一个作者的名字以及出版过的所有书籍的最高价格
    queryset_result = Author.objects.all().annotate(max_Price=Max("book__price")).values("name","max_Price")
    print(queryset_result)

    # 8、查询每一本书的名字，对应出版社名称以及作者的个数
    queryset_result = Book.objects.all().annotate(c=Count("authors")).values("title","publish__name","c")
    print(queryset_result)

    #9.根据一本图书作者数量的多少对查询集 QuerySet进行排序:
    Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')



############################################################聚合查询与分组查询#######################################################################

#聚合查询
#计算所有图书的平均价格
from django.db.models import Avg
Book.objects.all().aggregate(Avg('price'))    #{'price__avg': 107.14285714285714}


Book.objects.aggregate(average_price=Avg('price')) #{'average_price': 107.14285714285714}

from django.db.models import Avg,Max,Min
Book.objects.aggregate(Avg('price'),Max('price'),Min('price'))#{'price__avg': 107.14285714285714, 'price__max': Decimal('200.00'), 'price__min': Decimal('30.00')}


def query2(request):
    #普通字段
    #方法一
    book_obj = Book(title='book7',publishDate='2011-05-02',price=200,publish_id=1)
    book_obj.save()

    #方式二
    Book.objects.create(title='book8',publishDate='2014-05-02',price=200,publish_id=1)

    #外键字段
    #方法一
    publish_obj = Publish.objects.get(nid=1)
    Book.objects.create(title='book7',publishDate='2011-05-02',price=200,publish=publish_obj)

    #方法二
    Book.objects.create(title='book8', publishDate='2014-05-02', price=200, publish_id=1)

    #多对多字段
    book_obj = Book.objects.create(title='book9', publishDate='2015-05-02', price=200, publish_id=1)
    author_1 = Author.objects.create(name='a1',age=20)
    author_2 = Author.objects.create(name='a2',age=23)
    book_obj.authors.add(author_1,author_2) #将某个特定的model对象添加到被关联对象集合中
    book_obj.authors.create()               #创建并保存一个新对象

    #解除关系
    book_obj.authors.remove() #将某个特定的对象从被关联对象集合中去除
    book_obj.authors.clear()  #清空被关联对象集合
    book_obj.authors.set(author_1) #先清空，再设置

#对于所有类型的关联字段，add()、create()、remove()和clear(),set()都会马上更新数据库。在关联的任何一端，都不需要再调用save()方法

    #修改表记录
    #方式一
    author_obj = Author.objects.get(id=5)
    author_obj.name = 'jane'
    author_obj.save()

    #方式二
    # Author.objects.filter(id=5).update(name='jane')

    #删除表记录

    Book.objects.filter(publishDate__year='2011').delete()
