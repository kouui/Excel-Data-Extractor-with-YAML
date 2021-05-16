
# Excel-Data-Extractor-with-YAML

By defining a YAML configuration file, extract your excel data along with attributes and save them as tables in sqlites database or pandas DataFrame.


## run

I built this library with `python=3.8`. `python=3.x` should work.
```python

$ git clone https://github.com/kouui/Excel-Data-Extractor-with-YAML.git
$ cd Excel-Data-Extractor-with-YAML/src
$ conda create -n <env_name> python=3.8
$ conda activate <env_name>
$ pip install requirements.txt
$ python main_sqlite.py
$ python main_sqlite.py income.yaml
[12:15:48     INFO] Read income.yaml
[12:15:48     INFO] Processing file : ../data/(1-8-1-7)aa2n11.xls
[12:15:49     INFO] skip sheet (東京)産業計
[12:15:49     INFO] skip sheet (神奈川)産業計
[12:15:49     INFO] Processing sheet : (東京)Ｃ鉱業，採石業，砂利採取業
[12:15:49     INFO] Processing sheet : (東京)Ｄ建設業
[12:15:49     INFO] Processing sheet : (東京)Ｅ製造業
...
[12:15:56     INFO] Processing sheet : (神奈川)Ｒ９１職業紹介・労働者派遣業
[12:15:56     INFO] Processing sheet : (神奈川)Ｒ９２その他の事業サービス業
[12:15:56     INFO] Processing file : ../data/(1-8-1-6)aa2n11.xls
[12:15:57     INFO] skip sheet (埼玉)産業計
[12:15:57     INFO] skip sheet (千葉)産業計
[12:15:57     INFO] Processing sheet : (埼玉)Ｃ鉱業，採石業，砂利採取業
[12:15:57     INFO] Processing sheet : (埼玉)Ｄ建設業
[12:15:57     INFO] Processing sheet : (埼玉)Ｅ製造業
...
[12:16:03     INFO] Processing sheet : (千葉)Ｒ９１職業紹介・労働者派遣業
[12:16:03     INFO] Processing sheet : (千葉)Ｒ９２その他の事業サービス業
[12:16:03     INFO] number of added recode = 121776, number of miss record = 31824
```
roughly, `../data/*.xls` files (totally 7.2 MB) were converted into a sqlite3 database with size of 4.1 MB.

## sample results

with the sample `income.yaml`, the created `income.db` looks like
```
$ sqlite3 income.db
SQLite version 3.35.4 2021-04-02 15:20:15
Enter ".help" for usage hints.
sqlite> .mode line
sqlite> select * from sqlite_master;
    type = table
    name = data
tbl_name = data
rootpage = 2
     sql = CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, value FLOAT, attr_size INTEGER, attr_name INTEGER, attr_unit INTEGER, attr_age INTEGER, attr_region INTEGER, attr_industry INTEGER, attr_gender INTEGER)

    type = table
    name = sqlite_sequence
tbl_name = sqlite_sequence
rootpage = 3
     sql = CREATE TABLE sqlite_sequence(name,seq)

    type = table
    name = attr_size
tbl_name = attr_size
rootpage = 4
     sql = CREATE TABLE attr_size(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_name
tbl_name = attr_name
rootpage = 5
     sql = CREATE TABLE attr_name(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_unit
tbl_name = attr_unit
rootpage = 6
     sql = CREATE TABLE attr_unit(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_age
tbl_name = attr_age
rootpage = 7
     sql = CREATE TABLE attr_age(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_region
tbl_name = attr_region
rootpage = 8
     sql = CREATE TABLE attr_region(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_industry
tbl_name = attr_industry
rootpage = 9
     sql = CREATE TABLE attr_industry(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)

    type = table
    name = attr_gender
tbl_name = attr_gender
rootpage = 10
     sql = CREATE TABLE attr_gender(id INTEGER PRIMARY KEY AUTOINCREMENT, value STRING)
sqlite> select * from attr_name;
   id = 1
value = 年齢

   id = 2
value = 勤続年数

   id = 3
value = 所定内実労働時間数

   id = 4
value = 超過実労働時間数

   id = 5
value = きまって支給する現金給与額

   id = 6
value = 所定内給与額

   id = 7
value = 年間賞与その他特別給与額

   id = 8
value = 労働者数
sqlite> select * from data limit 5;
           id = 1
        value = 19.5
    attr_size = 1
    attr_name = 1
    attr_unit = 1
     attr_age = 1
  attr_region = 1
attr_industry = 1
  attr_gender = 1

           id = 2
        value = 0.5
    attr_size = 1
    attr_name = 2
    attr_unit = 2
     attr_age = 1
  attr_region = 1
attr_industry = 1
  attr_gender = 1

           id = 3
        value = 150.0
    attr_size = 1
    attr_name = 3
    attr_unit = 3
     attr_age = 1
  attr_region = 1
attr_industry = 1
  attr_gender = 1

           id = 4
        value = 20.0
    attr_size = 1
    attr_name = 4
    attr_unit = 3
     attr_age = 1
  attr_region = 1
attr_industry = 1
  attr_gender = 1

           id = 5
        value = 237.6
    attr_size = 1
    attr_name = 5
    attr_unit = 4
     attr_age = 1
  attr_region = 1
attr_industry = 1
  attr_gender = 1
sqlite> .exit
```

---

## `sqlite3` --> `pandas.DataFrame`

As shown in `src/example.sqlite_to_pandas.py`, by loading the data table and attribute tables, you are able to construct your `pandas.DataFrame` very easily with several rows of code.

```python

if __name__ == "__main__":

    import pandas as pd
    import sqlite3
    from typing import Dict, List, Tuple

    file_sqlite3 : str = "./income.db"
    conn : sqlite3.Connection = sqlite3.connect(file_sqlite3)
    
    ## : read attribute table and then set the 'id' column as index
    attr_tables : Dict[str, pd.DataFrame] = {}
    attr_names : Tuple[str] = ( "attr_size",  "attr_name",  "attr_unit",  "attr_age",  
                                "attr_region",  "attr_industry",  "attr_gender")
    
    for attr_table_name in attr_names:
        #attr_table_name : str = "attr_name"
        df_attr_select : pd.DataFrame = pd.read_sql_query(f"SELECT * FROM {attr_table_name}", conn)
        df_attr_select.set_index("id", inplace=True)
        attr_tables[attr_table_name] = df_attr_select
    del attr_table_name, df_attr_select
    
    ## : read data table and for example we only apply the "所定内実労働時間数" data
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
    
    ## : reshape your dataframe
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
```

---

## TODO (perhaps)

(If there is a need ...)

- [ ] functionality to append the `data_dict` directly into a `pandas.DataFrame`

