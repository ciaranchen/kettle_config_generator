# coding: utf-8

import csv
import os
import copy

import bs4
from temp import templateFields, t6_last

template_name = "AFS_FUND_PRODUCT"
base_dir = "kettle_config/"
base_table = "table.csv"
base_sql = "table.sql"
template_dir = "templates/"

def toUnicode(ch):
    st = ch.encode('unicode_escape')
    st = st.decode("utf-8")
    st = st.replace("\\u", ";&#x")
    return st[1:] + ';'

def get_template():
    global template_main, templateA, templateB, templateC, templateD
    with open(template_name + "/" + template_name + "主作业.kjb") as f:
        template_main = f.read()
    with open(template_name + "/" + template_name + "写入正式表.ktr") as f:
        templateA = f.read()
    with open(template_name + "/" + template_name + "回写入库状态.ktr") as f:
        templateB = f.read()
    # with open(template_name + "/" + template_name + "处理数据文件.ktr") as f:
    #     templateC = f.read()
    templateC = bs4.BeautifulSoup(open(template_name + "/" + template_name + "处理数据文件.ktr"), "xml")
    with open(template_name + '/' + template_name + '获取文件名和job_code做变量.ktr') as f:
        templateD = f.read()
    read_sql_table()

def read_sql_table():
    global sql_table
    with open(base_sql) as fp:
        # 取每行行首字段
        firsts = [line.strip().split(' ')[0] for line in fp.readlines()]
        t = {}
        now_key = ''
        s = ''
        for f in firsts:
            # 略过关键字
            if f == 'create' or f == 'location' or f == 'stored':
                continue
            # 取段名
            if f[:5] == 'tmp2.':
                print(f[5:-1])
                t[now_key] = s
                now_key = f[5:-1]
                s = ''
            # 取字段
            else:
                s += ', ' + f
    sql_table = t
    del sql_table['']
            
        

def get_table_name(filename):
    with open(filename) as fp:
        return [row for row in csv.reader(fp)]


def mk_row_struct(row):
    job_code = row[0]
    # copy file from template
    if not os.path.exists(job_code):
        os.mkdir(job_code)
    toMain(job_code)
    toA(job_code)
    toB(job_code)
    toC(job_code)
    toD(job_code)


def toMain(code):
    # template_main
    with open(code + "/" + code + "主作业.kjb", 'w') as fw:
        fw.write(template_main.replace(template_name, code))

def toA(code):
    with open(code + "/" + code + "写入正式表.ktr", 'w') as fw:
        fw.write(templateA.replace(template_name, code))

def toB(code):
    with open(code + "/" + code + "回写入库状态.ktr", 'w') as fw:
        fw.write(templateB.replace(template_name, code))

def toC(code):
    # 生成新的 “处理数据文件”
    structs = find_struct(code)
    # structs = ["EXCH_TRADEBIZ_TYPE_CD", "EXCH_TRADEBIZ_TYPE_DESC"]
    print(structs)
    add_fields(code, structs)

def toD(code):
    with open(code + "/" + code + "获取文件名和job_code做变量.ktr", 'w') as fw:
        fw.write(templateD.replace(template_name, code))

def find_struct(query):
    return sql_table[query].split(", ")[1:]

def add_fields(code, structs):
    fields = templateC.find_all("fields")
    for i in range(6):
        if i != 5: 
            content = [templateFields[i].format(name=c) for c in structs]
            fields[i].clear()
            for c in content:
                fields[i].append(bs4.BeautifulSoup(c, "xml").field)
        else:
            content = [templateFields[i].format(name=c) for c in structs[:-1]]
            fields[i].clear()
            for c in content:
                fields[i].append(bs4.BeautifulSoup(c, "xml").field)
            fields[i].append(bs4.BeautifulSoup(t6_last.format(name=structs[-1]), "xml").field)
    # print(code + "/" + code + "处理数据文件.ktr")
    with open(code + "/" + code + "处理数据文件.ktr", 'wb') as fw:
        temp = str(templateC).replace(template_name, code)
        fw.write(temp.encode('utf-8'))

def main():
    get_template()
    # get name
    rows = get_table_name(base_table)
    # ch
    os.chdir(base_dir)
    with open("tablenames.txt", 'w') as fw:
        for r in rows:
            mk_row_struct(r)
            print(r[0])
            fw.write(r[0] + '\n')

if __name__ == '__main__':
    main()
    # read_sql_table()
    with open("sql_tables.csv", 'w') as fw:
        for k in sql_table:
            fw.write(k +  "," + sql_table[k].replace(", ", "|").strip().strip("|") +"\n")
    