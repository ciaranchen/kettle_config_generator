# coding: utf-8

import csv
import os
import copy

import bs4
from temp import templateFields, t6_last

# ================== OPTIONS ========================

showProgress = True
template_name = "AFS_FUND_PRODUCT"
base_dir = "kettle_config/"
base_table = ["table.csv"]
tables_desc = ["output_cfpt.txt", "output_xzpt.txt"]

# ====================================================
sql_table = {}
log_err = open("error_logs.txt", 'w')


def toUnicode(ch):
    st = ch.encode('unicode_escape')
    st = st.decode("utf-8")
    st = st.replace("\\u", ";&#x")
    return st[1:] + ';'


def prepare_work():
    # read template files
    global template_main, templateA, templateB, templateC, templateD
    with open(template_name + "/" + template_name + "_0.kjb") as f:
        template_main = f.read()
    with open(template_name + "/" + template_name + "_1.ktr") as f:
        templateA = f.read()
    with open(template_name + "/" + template_name + "_4.ktr") as f:
        templateB = f.read()
    templateC = bs4.BeautifulSoup(open(template_name + "/" + template_name + "_2.ktr"), "xml")
    with open(template_name + '/' + template_name + '_3.ktr') as f:
        templateD = f.read()
    # read sql descriptions from tables_desc
    for filename in tables_desc:
        read_sql_table(filename)


def read_sql_table(filename):
    global sql_table
    res = {}
    now_table = ''
    res[now_table] = []
    for line in open(filename).readlines():
        words = line.strip().split(' ')
        if len(words) == 2 and words[0][0] == '`' and words[0][-1] == '`':
            res[now_table].append(words[0][1:-1])
            continue
        if len(words) == 3 and words[0].lower() == 'create' and words[1].lower() == 'table':
            now_table = words[2][1:-2]
            res[now_table] = []
    sql_table.update(res)
    del sql_table['']


def mk_row_struct(row):
    job_code, tablename, ptname = row
    # copy file from template
    if not os.path.exists(job_code):
        os.mkdir(job_code)
    try:
        structs = sql_table[ptname.lower() + "." + tablename.lower()]
    except KeyError as e:
        log_err.write(str(e) + '\n')
        return False
    toMain(job_code)
    toA(job_code)
    toB(job_code)
    toC(job_code, structs)
    toD(job_code)
    return True


def toMain(code):
    # 主作业
    with open(code + "/" + code + "_0.kjb", 'w') as fw:
        fw.write(template_main.replace(template_name, code))


def toA(code):
    with open(code + "/" + code + "_1.ktr", 'w') as fw:
        fw.write(templateA.replace(template_name, code))


def toB(code):
    with open(code + "/" + code + "_4.ktr", 'w') as fw:
        fw.write(templateB.replace(template_name, code))


def toC(code, structs):
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
    with open(code + "/" + code + "_2.ktr", 'wb') as fw:
        temp = str(templateC).replace(template_name, code)
        fw.write(temp.encode('utf-8'))


def toD(code):
    with open(code + "/" + code + "_3.ktr", 'w') as fw:
        fw.write(templateD.replace(template_name, code))


def main():
    prepare_work()
    ## get all objectives
    rows = []
    for filename in base_table:
        rows.extend([row for row in csv.reader(open(filename))])
    ## into base directory
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    os.chdir(base_dir)
    ## main procedure
    print("generate: " + str(len(rows)) + " tables' kettle configurations.")
    if showProgress:
        from progress.bar import Bar
        bar = Bar(' Processing', max=len(rows))
    with open("tablenames.txt", 'w') as fw:
        for r in rows:
            if not mk_row_struct(r):
                # print(r[0])
                fw.write(r[0] + '\n')
            if showProgress:
                bar.next()
    ## end of procedure
    if showProgress:
        bar.finish()
    log_err.close()

if __name__ == '__main__':
    main()
    # prepare_work()
    with open("sql_tables.csv", 'w') as fw:
        for k in sql_table:
            fw.write(k +  "," + str(sql_table[k]).replace(", ", "|") +"\n")
    