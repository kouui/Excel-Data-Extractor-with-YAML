
if __name__ == "__main__":

    import pandas as pd
    import sqlite3
    from typing import Dict, List, Tuple

    import os

    file_sqlite3 : str = __file__.replace(os.path.basename(__file__), "out.db")
    conn : sqlite3.Connection = sqlite3.connect(file_sqlite3)

    attr_tables : Dict[str, pd.DataFrame] = {}
    attr_names : Tuple[str] = ( "attr_size",  "attr_name",  "attr_unit",  "attr_age",  
                                "attr_region",  "attr_industry",  "attr_gender")
    
    for attr_table_name in attr_names:
        #attr_table_name : str = "attr_name"
        df_attr_select : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM {attr_table_name}", conn)
        df_attr_select.set_index("id", inplace=True)
        attr_tables[attr_table_name] = df_attr_select
    del attr_table_name, df_attr_select

    attr_select_value : str = "所定内実労働時間数"
    attr_select_df : pd.DataFrame = attr_tables["attr_name"]
    attr_select_id : int = attr_select_df[ attr_select_df["value"] == attr_select_value ].index.tolist()[0]
    df_data : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM data WHERE attr_name='{attr_select_id}'", conn)

    for key, df_attr in attr_tables.items():
        df_data[key] = df_data[key].map( lambda x : df_attr.at[x, "value"] )
    

    # print( df_data.head(n=10) )
    ## 
    ##     id value   attr_size  attr_name            attr_unit attr_age    attr_region  attr_industry          attr_gender
    ## 0   3  150.0     10人以上  所定内実労働時間数        時間     ～１９歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 1  11  150.0  100～999人  所定内実労働時間数        時間     ～１９歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 2  19  156.0     10人以上  所定内実労働時間数        時間   ２０～２４歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 3  27  158.0  1,000人以上  所定内実労働時間数        時間   ２０～２４歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 4  35  149.0  100～999人  所定内実労働時間数        時間   ２０～２４歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 5  43  174.0    10～99人  所定内実労働時間数        時間   ２０～２４歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 6  51  148.0     10人以上  所定内実労働時間数        時間   ２５～２９歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 7  59  148.0  1,000人以上  所定内実労働時間数        時間   ２５～２９歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 8  67  147.0  100～999人  所定内実労働時間数        時間   ２５～２９歳          東京  Ｃ鉱業，採石業，砂利採取業           男
    ## 9  75  160.0    10～99人  所定内実労働時間数        時間   ２５～２９歳          東京  Ｃ鉱業，採石業，砂利採取業           男

    df_data : pd.DataFrame = df_data.drop(columns=["id","attr_name","attr_unit"])
    df_data : pd.DataFrame = df_data.set_index( ["attr_region", "attr_industry", "attr_age", "attr_gender", "attr_size"] )
    df_data : pd.DataFrame = df_data.unstack( "attr_age" )
    
    #print(df_data.head(n=4))
    ##
    ##                                                          value 
    ##attr_age                                                 ２０～２４歳 ２５～２９歳 ３０～３４歳 ３５～３９歳 ４０～４４歳 ４５～４９歳 ５０～５４歳 ５５～５９歳 ６０～６４歳 ６５～６９歳   ７０歳～   ～１９歳
    ##attr_region attr_industry          attr_gender attr_size 
    ##千葉         Ｃ鉱業，採石業，砂利採取業 女          1,000人以上  NaN       NaN        NaN        137.0      NaN        147.0       NaN        NaN       NaN        NaN          NaN       NaN 
    ##                                               10人以上     NaN       NaN        NaN        137.0     176.0       147.0       NaN        NaN       NaN        NaN          NaN       NaN
    ##                                               10～99人     NaN        NaN       NaN        NaN       176.0        NaN        NaN        NaN       NaN        NaN          NaN       NaN
    ##                                   男          1,000人以上  152.0     147.0      132.0      171.0     145.0       160.0      153.0      158.0      NaN        NaN          NaN       155.0