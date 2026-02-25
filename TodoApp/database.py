from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

#SQLite connection
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

#create location of database
#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Poiu%40Lkjh%2312@127.0.0.1:3306/TodoApplicationDatabase'

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Poiu@Lkjh#12",
    host="127.0.0.1",
    port=3306,
    database="TodoApplicationDatabase"
)

#engine makes db connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session use that connection to run queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
