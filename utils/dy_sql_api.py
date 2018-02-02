"""@author: Young
@license: (C) Copyright 2013-2018
@contact: aidabloc@163.com
@file: df_sql.py
@time: 2018/1/28 15:20
数据库读取API
"""
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
pymysql.install_as_MySQLdb()


class ConSql(object):
    # 配置数据库
    # define db dict
    db_dict = create_engine('mysql+pymysql://<user>:<password>@<host>[:<port>]/<dbname>')

    @classmethod
    def table(cls, name, index_col=None, db="em"):
        if db == "em":
            engine = cls.em
        elif db == "rs":
            engine = cls.rs
        else:
            raise KeyError

        if index_col is not None:
            return pd.read_sql_table(name, engine, index_col=index_col)
        else:
            return pd.read_sql_table(name, engine)

    @classmethod
    def query(cls, sql, index_col=None, db="em"):
        if db == "em":
            engine = cls.em
        elif db == "rs":
            engine = cls.rs
        else:
            raise KeyError

        if index_col is not None:
            return pd.read_sql_query(sql, engine, index_col=index_col)
        else:
            return pd.read_sql_query(sql, engine)

    @classmethod
    def create_table(cls, table_class, check_first=True):
        if type(table_class) == DeclarativeMeta:
            table = table_class.__table__
        else:
            raise TypeError
        Base = declarative_base(cls.rs)
        Base.metadata.create_all(cls.rs, [table], check_first)
        print("创建表", table_class)

    @classmethod
    def to_sql(cls, df, name, **kwargs):
        pd.io.sql.to_sql(df, name, cls.rs, **kwargs)
        return ("数据上传完毕！")

    @classmethod
    def del_table(cls, name):
        db = pymysql.connect(host='gz-cdb-57rybl5p.sql.tencentcdb.com',
                             port=63763,
                             user='research_dev',
                             password='SZZ1lsfdjKdf',
                             db="research",
                             charset='utf8mb4')
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute("""DROP TABLE {}""".format(name))
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print("删除操作发生错误，回滚")
            db.rollback()

    @classmethod
    def clean_table(cls, name):
        db = pymysql.connect(host='gz-cdb-57rybl5p.sql.tencentcdb.com',
                             port=63763,
                             user='research_dev',
                             password='SZZ1lsfdjKdf',
                             db="research",
                             charset='utf8mb4')
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute("""TRUNCATE {}""".format(name))
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print("清空操作发生错误，回滚")
            db.rollback()



