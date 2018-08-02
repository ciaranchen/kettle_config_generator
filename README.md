## 文件说明

- parse.py

    解析文件的主代码。转换所需的文件名等参数写在`parse.py`的开头。

- temp.py

    放置模版字串。

- encode.js

    用于对文件进行`HTML Entity`的转换

## 注意

1. 所使用的文件一切以本文件夹內的 AFS_FUND_AGMT 为基准，因此谨慎改动此文件夹。
2. 使用`parse.py` 会生成一个tablenames.txt，用于记录已经生成记录的配置文件的表名。
3. 在`parse.py`完成生成记录后，会生成一个`sql_tables.csv`，记录从sql文件中获得的表名与对应的字段。

## How to use

生成kettle配置文件：

```shell
python parse.py
```

将配置文件中的`处理数据库文件.ktr`的所有中文转换成HTML Entity的形式，需要首先执行上一步：
(虽然这没什么用就是了)

```shell
node encode.js tablenames.txt
```

> 会在原文件夹下生成`下划线+原文件名`的新文件。

## 使用须知

### 对SQL文件的要求

文件中的代码必须以

```sql
create EXTERNAL table IF NOT EXISTS
tmp2.MB_TRANFLOW(
TRF_FLOWNO        String,
TRF_CSTNO         String,
TRF_BSNCODE       String,
TRF_PAYACC        String,
TRF_SUBTIME       String,
TRF_TRANAMT       String,
TRF_HOSTFLWNO     String,
TRF_HOSTSENDTIME  String,
TRF_HOSTERROR     String,
TRF_HOSTMESSAGE   String,
TRF_IN_BATCH      String,
TRF_BANKREM       String,
TRF_STT           String,
TRF_CLIENTVERSION String,
TRF_QRCODE_FLAG   String,
TRF_FAV_FLAG      String,
TEST              String)ROW FORMAT DELIMITED FIELDS TERMINATED BY '\8'
stored as textfile
location  '/data/hive2/input/MB_TRANFLOW/';
```

这样的格式进行存储。（每行到空格前的代码只有`create`, `stored`, `location`关键字和字段名，表名以`tmp2.`开头以`(`结尾

尽量不要出现空行。
