import xlrd
import yaml
import os
from colorlog.setup_logger import setup_logger
from index import C, R

from glob import glob

import pandas as pd



_Logger = setup_logger()

#------------------------------------------------------------
# file reader
#------------------------------------------------------------
def getFileNames(handle):

    tar = handle["folder"]
    path = tar["path"]
    if tar["repeat"]:
        out = []
        files = glob(os.path.join(path, "*.xls"))
        for file in files:
            basename = os.path.basename(file)
            try:
                if tar["ignore"]["contain"] in basename :
                    _Logger.info(f"skip file {basename}")
                    continue
            except KeyError:
                pass
            out.append(file)
        return tuple(out)
    elif tar["name"] != "none":
        return (os.path.join(path,tar["name"]),)
    else:
        raise ValueError("Don't know how to select files.")


def yaml_read(fname):

    with open(fname) as file:
        yaml_obj = yaml.safe_load(file)
        _Logger.info(f"Read {fname}")

    return yaml_obj

yaml_dtype_func = {
    "float" : ("float", float),
    "int"   : ("int", int),
    "str"   : ("str", str),
}

yaml_except = {
    "na" : pd.NA,
}

def hasMultiGroup(keys):
    if "row" not in keys:
        return True
    return False

def getRange(text):
    l, r = [w.strip() for w in text.split(',')]
    return l, r

def getAttrRange(range_dict, key, group_id):

    if hasMultiGroup(range_dict.keys()):
        range_dict_true = range_dict[group_id]
    else:
        range_dict_true = range_dict

    if key == "column":
        return getRange( range_dict_true["row"] )
    elif key == "row":
        return getRange( range_dict_true["col"] )
    elif key == "single":
        return getRange( range_dict_true["row"] )[0], getRange( range_dict_true["col"] )[0]
    else:
        return None

def getSheetsIndex(handle, wb):

    tar = handle["sheet"]
    if tar["repeat"]:
        out = []

        for i, sheet_name in enumerate(wb.sheet_names()):
            try:
                if tar["ignore"]["contain"] in sheet_name :
                    _Logger.info(f"skip sheet {sheet_name}")
                    continue
            except KeyError:
                pass
            out.append(i)
        return tuple(out)

    elif tar["name"] != "none":
        for i, sheet_name in enumerate(wb.sheet_names()):
            if sheet_name == tar["name"]:
                return (i,)
    elif tar["index"] != "none":
        return (tar["index"],)
    else:
        raise ValueError("Don't know how to select work sheet.")


#------------------------------------------------------------
# formator
#------------------------------------------------------------

def formatStringBasic(s_):

    return s_.replace('\n', '').strip()

def formatStringReplace(s_, replace_dict):
    for key, val in replace_dict.items():
        s_ = s_.replace(key, val)
    return s_

def formatValue(val):

    if isinstance(val, str):
        val = formatStringBasic(val)
        return val
    else:
        return val
#------------------------------------------------------------
# xlrd processor
#------------------------------------------------------------
def getMergeValueDict(ws):

    data_dict = {}
    for crange in ws.merged_cells:
        rlo, rhi,clo, chi = crange
        value = None
        for rowx in range(rlo, rhi):
            for colx in range(clo, chi):
                if value is not None:
                    break
                if ws.cell(rowx,colx).ctype not in (xlrd.XL_CELL_BLANK, xlrd.XL_CELL_EMPTY):
                    value = ws.cell(rowx,colx).value
            if value is not None:
                break

        if value is None:
            raise ValueError(f"Cannot find value in merge range row:[{rlo},{rhi}], col:[{clo},{chi}]")
        for rowx in range(rlo, rhi):
            for colx in range(clo, chi):
                data_dict[(rowx,colx)] = value

    return data_dict

def getCellValue(rowx, colx, mValue_dict, ws):

    try:
        value = mValue_dict[ (rowx,colx) ]
    except KeyError:
        value = ws.cell( rowx, colx ).value

    return value

#------------------------------------------------------------
# record generator
#------------------------------------------------------------

def generateDataDict(handle, ws, mValue_dict):

    ##: data
    tar = handle["data"]

    # except value
    data_type    = yaml_dtype_func[tar["dtype"]][0]
    convert_func = yaml_dtype_func[tar["dtype"]][1]
    except_value = yaml_except[tar["except"]]

    # multi groups
    if hasMultiGroup( tar["range"] ):
        data_groups = [(key, val) for key, val in tar["range"].items()]
    else:
        data_groups = [(1,tar["range"]),]

    ##: attribute
    #tar = handle["attribute"]

    ##: extect data and attribute
    for group in data_groups:
        group_id = group[0]

        rlo, rhi = [ R(item) for item in getRange(group[1]["row"]) ]
        clo, chi = [ C(item) for item in getRange(group[1]["col"]) ]
        rhi += 1 # to include the final row
        chi += 1 # to include the final col

        for rowx in range(rlo, rhi):
            for colx in range(clo, chi):

                data_dict = {}

                # get data value
                value = getCellValue(rowx, colx, mValue_dict, ws)
                try:
                    value = convert_func(value)
                    value = formatValue(value)
                except:
                    value = except_value
                data_dict[ handle["data"]["name"] ] = value

                # get attribute value
                for aname, adict in handle["attribute"].items():
                    attr_type = adict["dtype"]
                    attr_range = getAttrRange(adict["range"], adict["type"], group_id)

                    if adict["type"] == "column":
                        value = getCellValue(R(attr_range[0]), colx, mValue_dict, ws)
                    elif adict["type"] == "row":
                        value = getCellValue(rowx, C(attr_range[0]), mValue_dict, ws)
                    elif adict["type"] == "single":
                        value = getCellValue(R(attr_range[0]), C(attr_range[1]), mValue_dict, ws)
                    else:
                        raise ValueError("Supported attribute types : column, row, single.")

                    value = formatValue(value)
                    if "replace" in adict.keys() and yaml_dtype_func[attr_type][0]=="str":
                        value = formatStringReplace(value, adict["replace"])

                    data_dict[ aname ] = value

                yield data_dict


#------------------------------------------------------------
#
#------------------------------------------------------------
