from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Создаем базу данных SQLite
DATABASE_URL = 'sqlite:///PH.db'
engine = create_engine(DATABASE_URL)

# Создаем базовый класс
Base = declarative_base()


# Определяем модель
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    updated = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text, nullable=True)
    review = Column(Text, nullable=True)
    linkPH = Column(String, nullable=True)
    link = Column(String, nullable=True)
    img = Column(String, nullable=True)
    posted = Column(Integer, default=0)


# Создаем таблицы
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_product(title, content=None, review=None, linkPH=None, link=None, img=None, posted=0):
    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        new_product = Product(title=title,
                              content=content,
                              review=review,
                              linkPH=linkPH,
                              link=link,
                              img=img,
                              posted=posted)
        session.add(new_product)
        session.commit()
    except Exception as e:
        session.rollback()
        print('Ошибка добавления в БД')
    finally:
        session.close()


def get_product_by_id(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == id).first()

    except:
        session.rollback()
    finally:
        session.close()
    return product


def get_product_by_title(tit):
    session = Session()
    try:
        product = session.query(Product).filter(Product.title == tit).first()

    except:
        session.rollback()
    finally:
        session.close()
    return product

def get_all_products():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        products = session.query(Product).all()  # Получаем все записи из таблицы products
        return products
    except Exception as e:
        print('Ошибка при получении данных из БД:', e)
        return []
    finally:
        session.close()


def upd_posted(title):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        product = session.query(Product).filter(Product.title == title).first()
        product.posted = 1
        session.commit()

    except Exception as e:

        session.rollback()

    finally:
        session.close()
