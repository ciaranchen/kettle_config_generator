import os
import bs4
import csv
from itertools import product
from xml_template import entry_template, start_hop, end_hop


# =========  OPTIONS  =================
kettles_path = "D:\ljy\jobs\\"
is_windows = True
is_from_dir = True
objective_dir = "outputs"
read_name_from = ["C:\\Users\ciaran\Desktop\Projects\kettle_config_generator\kettle_config"]
xlocs = 10
ylocs = 9
x_tuple = (100, 900)
y_tuple = (100, 820)
showProgress = True
# =====================================


ftemplate = bs4.BeautifulSoup(open("main_run_jobs.kjb"), "lxml")
base_cnt = xlocs * ylocs
if objective_dir is not None and not os.path.exists(objective_dir):
    os.mkdir(objective_dir)
if showProgress:
    from progress.bar import Bar


def get_table_names():
    tablenames = []
    if is_from_dir:
        for path in read_name_from:
            tablenames.extend([ f for f in os.listdir(path) if not os.path.isfile(os.path.join(path,f)) ])
    else:
        for filename in read_name_from:
            tablenames.extend([row[1] for row in csv.reader(open(filename))])
    return tablenames


def get_matrix():
    x_diff = int((x_tuple[1] - x_tuple[0])/xlocs)
    y_diff = int((y_tuple[1] - y_tuple[0])/ylocs)
    matrix = [(x, y) for x, y in product(range(x_tuple[0], x_tuple[1], x_diff), range(y_tuple[0], y_tuple[1], y_diff))]
    return matrix[:base_cnt]


def draw_pic(matrix, tablenames, file_cnt):
    cnt = 0
    for tablename in tablenames:
        job_code = tablename
        entries = ftemplate.find("entries")
        hops = ftemplate.find("hops")
        # append_entry(job_code, matrix[cnt])
        entries.append(bs4.BeautifulSoup(entry_template.format(
            path=kettles_path,
            name=job_code,
            split='\\' if is_windows else '/',
            xloc=matrix[cnt][0], 
            yloc=matrix[cnt][1]
        ), "lxml").entry)
        # append_hops(job_code)
        hops.append(bs4.BeautifulSoup(start_hop.format(name=job_code), "lxml").hop)
        hops.append(bs4.BeautifulSoup(end_hop.format(name=job_code), "lxml").hop)
        bar.next()
        cnt += 1
    with open(objective_dir + '/output' + str(file_cnt) + '.kjb', 'w') as fw:
        fw.write(str(ftemplate.job))


def main():
    global bar
    matrix = get_matrix()
    tablenames = get_table_names()
    # print(tablenames)
    bar = Bar(' Processing', max=len(tablenames))
    cnt = 1
    while len(tablenames) > 0:
        draw_pic(matrix, tablenames[:base_cnt], cnt)
        tablenames = tablenames[base_cnt:]
        cnt += 1
    bar.finish()


if __name__ == '__main__':
    main()