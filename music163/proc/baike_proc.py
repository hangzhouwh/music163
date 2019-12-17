# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 9:46
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : baike_proc.py 
# @Software: PyCharm
import re
import pandas as pd
from music163.proc import lyric_cloudy
from music163.tool import json_tool


def get_occupation_scatter(datas):
	occupation = []
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '职业' in attr_name:
			idx = attr_name.index('职业')
			occupation.append(attr_value[idx])

	ocs = []
	for occu in occupation:
		for occ in occu:
			occ_lst = re.split(" |,|，|/|;|；", occ)
			for occ_value in reversed(occ_lst):
				if occ_value == '':
					occ_lst.remove(occ_value)
			ocs.extend(occ_lst)
	# ocs = list(set(ocs))
	ocs_frequency = lyric_cloudy.get_word_frequency(ocs)

	ocs_fre = []
	count = []
	oc = []
	rate = []
	sum = 0
	for x in ocs_frequency:
		if x[1] >= 10:
			ocs_fre.append(x)
			sum = sum + x[1]

	for x in ocs_fre:
		oc.append(x[0])
		count.append(x[1])
		rate.append(x[1]/sum)

	df = pd.DataFrame([oc, count, rate], index=['oc', 'count', 'rate'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_职业分布.csv', encoding='utf_8_sig')


def occ_morethanone(datas):
	occupation = []
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '职业' in attr_name:
			idx = attr_name.index('职业')
			occupation.append(attr_value[idx])
	morethanone = []
	count = []
	for x in occupation:
		if len(x) in morethanone:
			idx = morethanone.index(len(x))
			count[idx] += 1
		else:
			morethanone.append(len(x))
			count.append(1)

	df = pd.DataFrame([morethanone, count], index=['morethanone', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_个人职业数量分布.csv', encoding='utf_8_sig')



def get_nationality(datas):
	nationality = []
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '国籍' in attr_name:
			idx = attr_name.index('国籍')
			for x in attr_value[idx]:
				country_lst = re.split(",|，|/|;|；", x)
				nationality.extend(country_lst)
	nationality_set = list(set(nationality))
	count = {}
	for i in nationality:
		count[i] = count.get(i, 0) + 1

	nationality_x = []
	nationality_count = []
	for i in nationality_set:
		nationality_x.append(i)
		nationality_count.append(count.get(i))

	df = pd.DataFrame([nationality_x, nationality_count], index=['nationality', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_国籍分布信息.csv', encoding='utf_8_sig')


def get_company(datas):
	companys = []
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '经纪公司' in attr_name:
			idx = attr_name.index('经纪公司')
			for value in attr_value[idx]:
				value_list = re.split(",|，|/|;|；", value)
				companys.extend(value_list)

	company_set = list(set(companys))
	company_count = {}
	for company in company_set:
		company_count[company] = company_count.get(company, 0) + 1

	count = []
	for i in company_set:
		count.append(company_count.get(i))

	df = pd.DataFrame([company_set, count], index=['company', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_经济公司.csv', encoding='utf_8_sig')


def get_school(datas):
	schools = []
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '毕业院校' in attr_name:
			idx = attr_name.index('毕业院校')
			schools.extend(attr_value[idx])

	school_set = list(set(schools))
	school_count = {}
	for school in school_set:
		school_count[school] = school_count.get(school, 0) + 1

	count = []
	for i in school_set:
		count.append(school_count.get(i))

	df = pd.DataFrame([school_set, count], index=['school', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_毕业院校.csv', encoding='utf_8_sig')


def wash_1():
	filepath = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\baike_chinese_ar.json'
	datas = json_tool.load_json(filepath)
	for artist in reversed(datas):
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if len(attr_name) == 0:
			datas.remove(artist)
	filepath2 = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\baike_chinese_ar_1.0.json'
	json_tool.write_json(datas, filepath2)


def get_decade(datas):
	births = []
	pattern = re.compile(r'\d{4}')
	for artist in datas:
		attr_name = artist['attr_name']
		attr_value = artist['attr_value']
		if '出生日期' in attr_name:
			idx = attr_name.index('出生日期')
			value = attr_value[idx][0]
			year = pattern.findall(value)
			births.extend(year)

	birth_set = list(set(births))
	birth_count = [0 for index in range(len(birth_set))]
	for birth in births:
		idx = birth_set.index(birth)
		birth_count[idx] += 1

	df = pd.DataFrame([birth_set, birth_count], index=['birth_year', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\百科_出生.csv', encoding='utf_8_sig')


if __name__ == "__main__":
	# artist_name  # 中文名
	# nationality  # 国籍 √
	# occupation  # 职业 √
	# birthday  # 出生日期
	# IBEC  # 经纪公司 √
	# university  # 毕业院校 √

	filepath = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\baike_chinese_ar_clean.json'
	datas = json_tool.load_json(filepath)
	get_decade(datas)