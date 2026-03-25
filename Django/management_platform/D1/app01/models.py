

# Create your models here.
'''
为什么要用 models.py（核心价值）
告别手写 SQL：对新手友好，不用记复杂的 SQL 建表语句，用 Python 类就能定义表；
ORM 核心载体：Django 的 ORM（对象关系映射）机制，就是通过models.py里的类，把「Python 对象操作」转换成「数据库 SQL 操作」（比如用Article.objects.create()代替INSERT INTO）；
表结构可迁移：通过makemigrations/migrate命令，能轻松把表结构同步到 MySQL、PostgreSQL 等不同数据库，不用改代码；
自带数据校验：Model 里可以定义字段规则（比如max_length=100、null=False），Django 会自动校验数据，避免脏数据进入数据库。
models.py 基本用法（新手易懂示例）
以你之前想了解的「文章表」为例，对比 SQL 和 Django Model，你就能秒懂：
1. 用 SQL 创建文章表（需要手写）
sql
CREATE TABLE `app01_article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
2. 用 Django Model 创建（写在models.py里）
python
运行
# app01/models.py
from django.db import models

# 一个类 = 一张数据库表
class Article(models.Model):
    # 类的属性 = 表的字段
    title = models.CharField(max_length=100, verbose_name="文章标题")  # 对应varchar(100)
    content = models.TextField(verbose_name="文章内容")  # 对应text
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 对应datetime，自动填充创建时间

    # 可选：配置表的元信息（比如表名、后台显示名称）
    class Meta:
        db_table = "article"  # 自定义数据库表名（默认是app名_类名，比如app01_article）
        verbose_name = "文章"  # 后台管理显示的单名
        verbose_name_plural = "文章"  # 后台管理显示的复数名（避免默认加s）

    # 可选：打印对象时显示有意义的内容（比如文章标题）
    def __str__(self):
        return self.title
3. 同步到 MySQL（只需两条命令）
写完上面的 Model 后，执行你之前用过的命令，Django 会自动生成 SQL 并执行：
bash
运行
python manage.py makemigrations  # 生成迁移脚本（相当于把Model转成SQL草稿）
python manage.py migrate         # 执行脚本（把SQL真正跑在MySQL里）
Model 操作数据库（不用写 SQL）
定义好 Model 后，你可以用 Python 代码直接操作数据库，比如：
python
运行
# 1. 新增一篇文章（代替INSERT INTO）
Article.objects.create(title="我的第一篇文章", content="Django Model真好用！")

# 2. 查询所有文章（代替SELECT * FROM article）
all_articles = Article.objects.all()

# 3. 查询标题包含「Django」的文章（代替WHERE条件）
django_articles = Article.objects.filter(title__contains="Django")

# 4. 删除文章（代替DELETE）
Article.objects.filter(id=1).delete()
总结
models.py 是 Django 的「数据库表结构定义文件」，核心是用 Python 类替代 SQL 建表；
它是 ORM 机制的核心，让你能用 Python 代码操作数据库，不用手写 SQL；
开发流程：在models.py写类 → makemigrations生成迁移脚本 → migrate同步到数据库 → 用 Model 的 API 操作数据。'''


 
from django.db import models

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()


    """
    create table app01_userInfo(
    id bigint auto_increment primary key,
    name varchar(32,
    password carchar(64),
    age int
    )
    """

