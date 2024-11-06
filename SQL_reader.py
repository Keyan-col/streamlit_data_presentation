import streamlit as st
import pandas as pd
import pymysql
from datetime import datetime
import traceback


def get_data(metadata_input, starter, items_per_page, password):
    try:
        connection = pymysql.connect(host="117.50.205.210",
                                     port=3306,
                                     user="data_manage",
                                     password=password,
                                     database="data_manage",
                                     connect_timeout=10,
                                     read_timeout=10,
                                     write_timeout=10,
                                     charset='utf8mb4')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT * FROM {metadata_input} order by video_id limit {starter}, {items_per_page}"

        cursor.execute(sql)
        data = cursor.fetchall()

        # 关闭连接
        cursor.close()
        connection.close()

        return {"code": 200, "msg": "success", "data": data}

    except pymysql.Error as err:
        print(f"连接错误: {err}")
        return {"code": 500, "msg": str(err), "data": None}
    except Exception as e:
        print(f"其他错误: {str(e)}")
        return {"code": 500, "msg": str(e), "data": None}


def get_length(metadata_input, password):
    try:
        connection = pymysql.connect(host="117.50.205.210",
                                     port=3306,
                                     user="data_manage",
                                     password=password,
                                     database="data_manage",
                                     connect_timeout=10,
                                     read_timeout=10,
                                     write_timeout=10,
                                     charset='utf8mb4')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT count(*) as num FROM {metadata_input}"

        cursor.execute(sql)
        data = cursor.fetchall()

        # 关闭连接
        cursor.close()
        connection.close()

        return {"code": 200, "msg": "success", "data": data}

    except pymysql.Error as err:
        print(f"连接错误: {err}")
        return {"code": 500, "msg": str(err), "data": None}
    except Exception as e:
        print(f"其他错误: {str(e)}")
        return {"code": 500, "msg": str(e), "data": None}


if __name__ == '__main__':
    try:
        aa = get_data('temp_video')
    except Exception as e:
        print(f"主程序错误: {str(e)}")
        traceback.print_exc()
