from bs4 import BeautifulSoup
import requests
import xlwt

schs = []
for page in range(107):
    # 页面请求
    url = 'http://infomap.cdedu.gov.cn/Home/Index?all=2'
    req = requests.get(url)
    # 页面处理
    soup = BeautifulSoup(req.content, "html.parser")
    schools = soup.find_all(class_='index_ul01')
    for school in schools:
        for item in school:
            schs.append(item)

# 学校信息
sch_infos = []
for item in schs:
    # 学校名
    title = '【学校】' + item.a.h1.string
    # 学校信息
    text_div = item.find_all(class_='text_div')
    for ps in text_div:
        all_p = ps.find_all('p')
        item_info = []
        item_info.append(title)
        for p in all_p:
            item_info.append(p.string)
        sch_infos.append(item_info)

sch_infos.insert(0, ['【学校】学校', '【学段】学段', '【区域】区域', '【性质】性质', '【电话】电话', '【地址】地址', '【网站】网站', '【信息】信息'])
print(sch_infos)

# 创建xlwt工作簿
workbook = xlwt.Workbook()

# 添加板块
booksheet = workbook.add_sheet('学校信息', cell_overwrite_ok=True)
for i,row in enumerate(sch_infos):
    for j,col in enumerate(row):
        if col != None:
            # 添加数据
            booksheet.write(i, j, col[4:])

# 保存到本地文件
workbook.save('schools.xls')
