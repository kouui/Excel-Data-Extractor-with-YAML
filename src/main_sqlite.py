# 3.8 MB Excel file ~ 2.1 MB sqlite db file

from typing_extensions import TypeAlias
import xlrd, openpyxl
import sys
from lib import _Logger, yaml_read, getMergeValueDict
from lib import getSheetsIndex, getFileNames, generateDataDict

from sqliteLib import initializeDatabase, addDataDict

from typing import Dict, List, Tuple


if __name__ == "__main__":


    fyaml  : str = sys.argv[1]
    handle : Dict[str,Dict] = yaml_read( fyaml )

    files : Tuple[str] = getFileNames(handle)
    # sqlite way
    isCreate : bool = handle["database"]["new"]
    conn, attr_code = initializeDatabase(handle, isCreate)
    #conn.close()
    #exit(0)
    count_record : int = 0
    count_miss   : int = 0
    for file in files:
        _Logger.info(f"Processing file : {file}")
        if file.endswith(".xls"):
            wb = xlrd.open_workbook(file, formatting_info=True)
            fCode = 0
        elif file.endswith(".xlsx"):
            wb = openpyxl.load_workbook(file)
            fCode = 1
        else:
            raise ValueError("Supported file extension : .xls, .xlsx")

        indices : Tuple[int] = getSheetsIndex(handle, wb, fCode)

        for kS in indices:

            if fCode == 0:
                ws = wb.sheet_by_index(kS)
                ws_name = ws.name
            elif fCode == 1:
                ws = wb.worksheets[kS]
                ws_name = ws.title
            _Logger.info(f"Processing sheet : {ws_name}")
            mValue_dict = getMergeValueDict(ws, fCode)

            for data_dict in generateDataDict(handle, ws, mValue_dict, fCode):
                #_Logger.debug(data_dict)
                # sqlite way
                res = addDataDict(conn, data_dict, attr_code, handle)
                if res:
                    count_record += 1
                else:
                    count_miss += 1



    conn.commit()
    conn.close()
    _Logger.info(f"number of added recode = {count_record}, number of missing record = {count_miss}")
