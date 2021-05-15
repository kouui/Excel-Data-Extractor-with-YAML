
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

## TODO

- [ ] functionality to append the `data_dict` directly into a `pandas.DataFrame`
- [ ] functionality to read a `sqlite3` database into a `pandas.DataFrame`
