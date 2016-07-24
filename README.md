Date:2016/7/24 18:31:35

django电子商城

@nevermoreluo

python3.4.4，django1.8+

所有库依赖已写入src/requirements.txt

各位可以按自己需求安装或者直接pip install -r requirements.txt

主目录为src文件，

static_in_env文件用于更新static文件(js,css,img等)，不需要原有数据的可以删除db.sqlite3文件自己设立

setting文件位于src/ecommerce-2/settings/内，建议仅对local.py进行修改

static文件建议在src/static_in_pro文件内修改后利用manage.py进行修改（python manage.py collectstatic）

需要修改home页面的在templates/home.html内修改

已有cart（购物车），products（产品），orders（订单），ecommerce2（主页面）,favorite（收藏）等app

