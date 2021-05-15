
import sqlite3
import os
from typing import List, Dict, Tuple

_datatype = {
    "int" : "INTEGER",
    "float" : "FLOAT",
    "str"  : "STRING",
}


#------------------------------------------------------------
# with pandas dataframe
#------------------------------------------------------------

def sqlite_SaveDataFrame(path, df, table):

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS SA''')
    df.to_sql(table, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

    return None


#------------------------------------------------------------
# write database record by record
#------------------------------------------------------------
from lib import yaml_except

def isTableExist(conn : sqlite3.Connection,
                 table : str) -> bool:
    c = conn.cursor()
    c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}';")
    if c.fetchone()[0] == 1:
        #conn.commit()
        return True
    else:
        #conn.commit()
        return False


def dropTable(conn : sqlite3.Connection,
              table : str) -> None:
    c = conn.cursor()
    sql = f"drop table {table};"
    c.execute(sql);
    conn.commit()
    return None

def initializeDatabase(handle : Dict[str,Dict],
                       isCreate : bool =True) -> Tuple[sqlite3.Connection, Dict[str,Dict]]:

    dbname = handle["database"]["name"]
    if isCreate and os.path.exists(dbname):
        os.remove(dbname)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    #
    attr_code = {}
    attr_info = {}
    tar = handle["attribute"]
    for key, val in tar.items():
        attr_info[ "attr_"+val["table"]["name"] ] = _datatype[val["dtype"]]
        attr_code[ "attr_"+val["table"]["name"] ] = {}

    #if isCreate:
    # create data table
    tar = handle["data"]
    name = tar["table"]["name"]
    dtype =  _datatype[tar["dtype"]]
    sql = f"CREATE TABLE {name}(id INTEGER PRIMARY KEY AUTOINCREMENT, value {dtype}"
    for name, dtype in attr_info.items():
        sql += f", {name} INTEGER"
    sql += ");"
    name = tar["table"]["name"]
    if isTableExist(conn, name):
        if isCreate:
            dropTable(conn, name)
            cur.execute( sql )

    else:
        cur.execute( sql )

    # create attribtue table
    tar = handle["attribute"]
    for name, dtype in attr_info.items():
        sql = f"CREATE TABLE {name}(id INTEGER PRIMARY KEY AUTOINCREMENT, value {dtype});"
        if isTableExist(conn, name):
            if isCreate:
                dropTable(conn, name)
                cur.execute( sql )
            else:
                ##: read attribute code from database
                sql = f"SELECT * FROM {name}"
                #print(f"table : {name}")
                for row in cur.execute(sql):
                    #print(row)
                    attr_code[name][row[1]] = row[0]
        else:
            cur.execute( sql )

    conn.commit()

    #conn.close()

    return conn, attr_code

def addDataDict(conn, data_dict, attr_code, handle) -> bool:

    datakey = handle["data"]["name"]
    if data_dict[datakey] is yaml_except["na"]:
        return False


    cur = conn.cursor()
    # process attr tables first
    tar = handle["attribute"]
    data_attr_code = {}
    for key, val in data_dict.items():
        if key == datakey:
            continue
        tablename = "attr_" + tar[key]["table"]["name"]
        code_dict = attr_code[tablename]
        try:
            code = code_dict[val]
        except KeyError:
            sql = f"INSERT INTO {tablename}(value) VALUES('{val}')"
            cur.execute( sql )
            conn.commit()
            sql = f"SELECT * FROM {tablename} where value = ? "
            row = cur.execute(sql, (val,)).fetchone()
            code = row[0]
            code_dict[val] = code
        data_attr_code[tablename] = code

    # process data table
    tablename = "data"
    value = data_dict[datakey]
    sql1 = f"INSERT INTO {tablename}(value"
    sql2 = f" VALUES({value}"
    for key, val in data_dict.items():
        if key == datakey:
            continue
        colname = "attr_" + tar[key]["table"]["name"]
        code = data_attr_code[colname]

        sql1 += f",{colname}"
        sql2 += f", {code}"
    sql1 += ")"
    sql2 += ");"
    sql = sql1 + sql2
    cur.execute( sql )


    return True
