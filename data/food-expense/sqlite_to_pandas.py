


if __name__ == "__main__":

    import pandas as pd
    import sqlite3
    from typing import Dict, List, Tuple

    import os

    file_sqlite3 : str = __file__.replace(os.path.basename(__file__), "out.db")
    conn : sqlite3.Connection = sqlite3.connect(file_sqlite3)

    attr_tables : Dict[str, pd.DataFrame] = {}
    attr_names : Tuple[str] = ( "income", "type", "city", "year" )
    attr_names : List[str] = [f"attr_{name}" for name in attr_names]
    
    for attr_table_name in attr_names:
        #attr_table_name : str = "attr_name"
        df_attr_select : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM {attr_table_name}", conn)
        df_attr_select.set_index("id", inplace=True)
        attr_tables[attr_table_name] = df_attr_select
    del attr_table_name, df_attr_select

    #attr_select_value : str = "消費支出"
    #attr_name : str = "attr_type"
    #attr_select_df : pd.DataFrame = attr_tables[attr_name]
    #attr_select_id : int = attr_select_df[ attr_select_df["value"] == attr_select_value ].index.tolist()[0]
    #df_data : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM data WHERE {attr_name}='{attr_select_id}'", conn)
    df_data : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM data", conn)

    for key, df_attr in attr_tables.items():
        df_data[key] = df_data[key].map( lambda x : df_attr.at[x, "value"] )


    cities  : List[str] = attr_tables["attr_city"]["value"].tolist()
    types   : List[str] = attr_tables["attr_type"]["value"].tolist()
    years   : List[str] = attr_tables["attr_year"]["value"].tolist()
    incomes : List[str] = attr_tables["attr_income"]["value"].tolist()

    columns : List[str] = ["city", "type", "year"] + [f"{s}" for s in incomes]
    coltype = {column : float for column in columns}
    coltype["city"] = str
    coltype["type"] = str
    coltype["year"] = str


    data_dict = {column : [] for column in columns}
    for year_ in years:
        for type_ in types:
            for city_ in cities:
                for income_ in incomes:
                    df_data_temp = df_data[ (df_data["attr_city"]==city_) & (df_data["attr_type"]==type_) & (df_data["attr_income"]==income_) & (df_data["attr_year"]==year_) ]
                    try:
                        val = df_data_temp["value"].tolist()[0]
                    except IndexError:
                        val = pd.NA
                    data_dict[income_].append(val)
                data_dict["city"].append(city_)
                data_dict["type"].append(type_)
                data_dict["year"].append(year_)
    
    df_data_new : pd.DataFrame = pd.DataFrame(data_dict)
    del data_dict
    print(df_data_new)