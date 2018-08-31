import bs4
import csv
from itertools import product
from xml_template import entry_template, start_hop, end_hop

ftemplate = bs4.BeautifulSoup(open("main_run_jobs.kjb"), "lxml")

# ========= ================
base_table = ["table.csv"]
base_cnt = 90
xlocs = 10
ylocs = 9
x_tuple = (100, 900)
y_tuple = (100, 820)
showProgress = True
# ==========================


if showProgress:
    from progress.bar import Bar


def get_matrix():
    if xlocs*ylocs != base_cnt:
        raise Exception("options are wrong.")
    x_diff = int((x_tuple[1] - x_tuple[0])/xlocs)
    y_diff = int((y_tuple[1] - y_tuple[0])/ylocs)
    matrix = [(x, y) for x, y in product(range(x_tuple[0], x_tuple[1], x_diff), range(y_tuple[0], y_tuple[1], y_diff))]
    if len(matrix) < base_cnt:
        raise Exception("space is not enough.")
    return matrix[:base_cnt]

matrix = get_matrix()

def draw_pic(rows, file_cnt):
    cnt = 0
    for row in rows:
        _, tablename = row
        job_code = tablename
        entries = ftemplate.find("entries")
        hops = ftemplate.find("hops")
        # append_entry(job_code, matrix[cnt])
        entries.append(bs4.BeautifulSoup(entry_template.format(name=job_code, xloc=matrix[cnt][0], yloc=matrix[cnt][1]), "lxml").entry)
        # append_hops(job_code)
        hops.append(bs4.BeautifulSoup(start_hop.format(name=job_code), "lxml").hop)
        hops.append(bs4.BeautifulSoup(end_hop.format(name=job_code), "lxml").hop)
        bar.next()
        cnt += 1
    with open('output' + str(file_cnt) + '.kjb', 'w') as fw:
        fw.write(str(ftemplate.job))


def main():
    global bar
    rows = []
    for filename in base_table:
        rows.extend([row for row in csv.reader(open(filename))])
    bar = Bar(' Processing', max=len(rows))
    cnt = 1
    while len(rows) > 0:
        draw_pic(rows[:base_cnt], cnt)
        rows = rows[base_cnt:]
        cnt += 1
    bar.finish()



if __name__ == '__main__':
    main()