# 3.8 MB Excel file ~ 2.1 MB sqlite db file

import xlrd
import sys
from lib import _Logger, yaml_read, getMergeValueDict
from lib import getSheetsIndex, getFileNames, generateDataDict

from sqliteLib import initializeDatabase, addDataDict



if __name__ == "__main__":


    fyaml = sys.argv[1]
    handle = yaml_read( fyaml )


    files = getFileNames(handle)
    # sqlite way
    conn, attr_code = initializeDatabase(handle, isCreate=True)
    #conn.close()
    #exit(0)
    count_record = 0
    count_miss   = 0
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
                #_Logger.debug(data_dict)
                # sqlite way
                res = addDataDict(conn, data_dict, attr_code, handle)
                if res:
                    count_record += 1
                else:
                    count_miss += 1


    conn.commit()
    conn.close()
    _Logger.info(f"number of added recode = {count_record}, number of miss record = {count_miss}")
