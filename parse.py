# coding: utf-8

import csv
import os
import copy

import bs4
from temp import templateFields, special_field

# ================== OPTIONS ========================

showProgress = True
ignoreCheck = False
template_name = "AFS_FIN_PROD_NETVALUE_H"
base_dir = "kettle_config/"
base_table = ["table.csv"]
tables_desc = ["output_cfpt.txt", "output_xzpt.txt"]
errorlog = "error.log"

# ====================================================

sql_table = {}

step_names = [k[1] for k in templateFields]

def check_config():
    print("checking...")
    if not os.path.exists(template_name):
        return ["not such a directory: " + template_name]
    ## check _2 template
    errs = []
    with open(template_name + "/" + template_name + "_2.ktr") as fp:
        basicC = bs4.BeautifulSoup(fp, "xml")
        steps = basicC.find_all("step")
        names = [step.find("name").text for step in steps]
        ## check steps' number
        if len(steps) != 6:
            errs.append("step number wrong: except 6, exact 7")
        ## check all step name exists
        no_names = [sn for sn in step_names if sn not in names]
        errs.extend(["step not found: " + name for name in no_names])
    return errs


def prepare_work():
    ## read template files
    global template_main, templateA, templateB, templateC, templateD
    with open(template_name + "/" + template_name + "_0.kjb") as f:
        template_main = f.read()
    with open(template_name + "/" + template_name + "_1.ktr") as f:
        templateA = f.read()
    with open(template_name + "/" + template_name + "_2.ktr") as f:
        templateB = bs4.BeautifulSoup(f, "xml")
    with open(template_name + "/" + template_name + "_3.ktr") as f:
        templateC = f.read()
    with open(template_name + '/' + template_name + '_4.ktr') as f:
        templateD = f.read()
    ## read sql descriptions from tables_desc
    for filename in tables_desc:
        read_sql_table(filename)


def read_sql_table(filename):
    global sql_table
    res = {}
    now_table = ''
    for line in open(filename).readlines():
        words = line.strip().split(' ')
        if len(words) == 2 and words[0] != "TBLPROPERTIES":
            res[now_table].append(words[0].strip('`\'\"'))
        elif len(words) == 3 and words[0].lower() == 'create' and words[1].lower() == 'table':
            now_table = words[2][:-1].strip('`\'\"')
            res[now_table] = []
    sql_table.update(res)
    if '' in sql_table:
        del sql_table['']


def mk_row_struct(row):
    job_code, tablename, ptname = row
    ## copy file from template
    if not os.path.exists(job_code):
        os.mkdir(job_code)
    try:
        structs = sql_table[ptname.lower() + "." + tablename.lower()]
    except KeyError as e:
        log_err.write(str(e) + '\n')
        return False
    toMain(job_code)
    toA(job_code)
    toB(job_code, structs)
    toC(job_code)
    toD(job_code)
    return True


def toMain(code):
    ## 主作业
    with open(code + "/" + code + "_0.kjb", 'w') as fw:
        fw.write(template_main.replace(template_name, code))


def toA(code):
    with open(code + "/" + code + "_1.ktr", 'w') as fw:
        fw.write(templateA.replace(template_name, code))


def toB(code, structs):
    steps = templateB.find_all("step")
    for step in steps:
        name = step.find("name").text
        fields = step.find("fields")
        fields.clear()

        ## append with basic stituations
        if name in step_names:
            template_field, _ = [e for e in filter(lambda x: x[1] == name, templateFields)][0]
            content = [template_field.format(name=c) for c in structs]
            for c in content:
                fields.append(bs4.BeautifulSoup(c, "xml").field)

        ## deal with special stituation
        if name == special_field[0]:
            _, template1, template2 = special_field
            contents = [template1.format(name=c) for c in structs[:-1]]
            for c in contents:
                fields.append(bs4.BeautifulSoup(c, "xml").field)
            fields.append(bs4.BeautifulSoup(template2.format(name=structs[-1]), "xml"))
    with open(code + "/" + code + "_2.ktr", 'wb') as fw:
        fw.write(str(templateB).replace(template_name, code).encode('utf-8'))


def toC(code):
    with open(code + "/" + code + "_3.ktr", 'w') as fw:
        fw.write(templateC.replace(template_name, code))


def toD(code):
    with open(code + "/" + code + "_4.ktr", 'w') as fw:
        fw.write(templateD.replace(template_name, code))


def main():
    errs = check_config()
    if len(errs) != 0:
        print('\n'.join(['- ' + err for err in errs]))
        if not ignoreCheck:
            os.remove(temporary_filename)
            log_err.close()
            print('exit.')
            return
    else:
        print('no problems.')
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
            if mk_row_struct(r):
                # print(r[0])
                fw.write(r[0] + '\n')
            if showProgress:
                bar.next()
            # break
    ## end of procedure
    if showProgress:
        bar.finish()
    log_err.close()
    with open("sql_tables.csv", 'w') as fw:
        for k in sql_table:
            fw.write(k +  "," + str(sql_table[k]).replace(", ", "|") +"\n")
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
            if mk_row_struct(r):
                # print(r[0])
                fw.write(r[0] + '\n')
            if showProgress:
                bar.next()
            # break
    ## end of procedure
    if showProgress:
        bar.finish()
    os.remove(temporary_filename)
    log_err.close()
    with open("sql_tables.csv", 'w') as fw:
        for k in sql_table:
            fw.write(k +  "," + str(sql_table[k]).replace(", ", "|") +"\n")

if __name__ == '__main__':
    global log_err
    log_err = open("error.log" if errorlog is None else errorlog, 'w')
    main()