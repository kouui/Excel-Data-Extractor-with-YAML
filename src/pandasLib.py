import pandas as pd
from lib import yaml_dtype_func

def yamlCreateEmptyDataframe(handle):

    columns = {}
    # data
    key = "data"
    columns[ handle[key]["name"] ] = handle[key]["dtype"]
    # attribute
    for key, val in handle["attribute"].items():
        columns[key] = val["dtype"]
    for key, val in columns.items():
        columns[key] = yaml_dtype_func[ val ][0]

    df = pd.DataFrame(columns, index=[])
    return df
