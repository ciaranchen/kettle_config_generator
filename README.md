# kettle config generator

本项目用于批量生成针对不同数据表进行ETL的kettle项目。

## 安装依赖

```shell
pip install -r requirements.txt
```

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

## 选项说明

- showProgress。 显示进度条
- template_name。 作为模板的文件夹
- base_dir。 生成结果存放地
- base_table。 可以为按列表格式写出的一个或多个文件。列出文件为需要生成的表名组成的csv文件。必须有三列：`job_code, 表名, 平台名称`。文件中不需出现列标题。
- tables_desc。 可以为按列表格式写出的一个或多个文件。按照特殊格式生成的建表语句，详细要求见下文。

## 使用须知

### 对SQL文件的要求

文件中的代码必须以

```shell
hive -e "use xxx; show tables;" | awk '{printf"show create table %s", $1}' > show_tables.sql
hive -f show_tables.sql >> output_cfpt.txt
```

生成的代码格式进行存储。
