"""This service allows to get comment/s from db"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()

def get_comments(type, value=False):
    """Returns comment/s from databse"""
    cursor, _ = get_cursor()
    if not cursor:
        # log that failed getting cursor
        return False
    if "tmp" not in name:
        # log that name was wrong
        return False
    q = f"""SELECT * FROM comments """
    if type is not None:
        if value:
            value = value.replace(";", "")
            value = value.replace("'", "''")
        if type == "WHERE_CHANNEL" and value:
            q += f"""WHERE channel_id = '{value}'"""
        elif type == "WHERE_COMMENT" and value:
            q += f"""WHERE id = '{value}'"""
        elif type == "WHERE_VIDEO" and value:
            q += f"""WHERE video_id = '{value}'"""
        else:
            return False
    try:
        cursor.execute(q)
    except MySQLdb.Error as error:
        print(error)
        # Log
        return False
        # sys.exit("Error:Failed getting comments from database")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    q = Queue('get_tmp_table', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='get_tmp_table')
        worker.work()
