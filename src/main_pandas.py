
import xlrd
import sys
from lib import _Logger, yaml_read, getMergeValueDict
from lib import getSheetsIndex, getFileNames, generateDataDict
from pandasLib import yamlCreateEmptyDataframe
from sqliteLib import sqlite_SaveDataFrame



if __name__ == "__main__":


    fyaml = sys.argv[1]
    handle = yaml_read( fyaml )


    files = getFileNames(handle)
    # pandas way
    df = yamlCreateEmptyDataframe(handle)

    for file in files:
        _Logger.info(f"Processing file : {file}")
        if file.endswith(".xls"):
            wb = xlrd.open_workbook(file, formatting_info=True)
        else:
            raise ValueError("Supported file extension : .xls")

        indices = getSheetsIndex(handle, wb)
        for kS in indices:
            _Logger.info(f"Processing sheet : {wb.sheet_names()[kS]}")
            ws = wb.sheet_by_index(kS)
            mValue_dict = getMergeValueDict(ws)
            for data_dict in generateDataDict(handle, ws, mValue_dict):
                # pandas way
                df = df.append(data_dict, ignore_index=True)
            break
        break



    # pandas way
    _Logger.info(f"Total rows in df : {len(df)}")
    #db_path = fyaml.replace(".yaml",".db")
    #table_name = fyaml.replace(".yaml",'')
    #_Logger.info(f"Saving to sqlite : {db_path}")
    #sqlite_SaveDataFrame(db_path, df, table_name)
