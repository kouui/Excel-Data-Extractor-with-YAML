
import sqlite3

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

def isTableExist(conn, table):
    c = conn.cursor()
    c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}';")
    if c.fetchone()[0] == 1:
        #conn.commit()
        return True
    else:
        #conn.commit()
        return False


def dropTable(conn, table):
    c = conn.cursor()
    sql = f"drop table {table};"
    c.execute(sql);
    conn.commit()
    return None

def initializeDatabase(handle, isCreate=True):

    dbname = handle["database"]["name"]
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    #
    attr_code = {}
    attr_info = {}
    tar = handle["attribute"]
    for key, val in tar.items():
        attr_info[ "attr_"+val["table"]["name"] ] = _datatype[val["dtype"]]
        attr_code[ "attr_"+val["table"]["name"] ] = {}

    if isCreate:
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
            dropTable(conn, name)
        cur.execute( sql )

        # create attribtue table
        tar = handle["attribute"]
        for name, dtype in attr_info.items():
            if isTableExist(conn, name):
                dropTable(conn, name)
            sql = f"CREATE TABLE {name}(id INTEGER PRIMARY KEY AUTOINCREMENT, value {dtype});"
            cur.execute( sql )

        conn.commit()
    else:
        # read attribute code from database
        raise NotImplementedError("isCreate = False not yet.")
    #conn.close()

    return conn, attr_code

def addDataDict(conn, data_dict, attr_code, handle):

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
