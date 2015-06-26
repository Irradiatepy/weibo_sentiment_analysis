# -*- coding:utf-8 -*-
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def detailprofile_re(content):
	gender_regex = u'性别:(.*)'
	gr = re.search(gender_regex, content)
	gender = gr.group(1) if gr is not None else None

	if gender:
		if gender == '女':
			gender = 0;
		else:
			gender = 1
	else:
		gender = -1

	desc_regex = u'简介:(.*)'
	dr = re.search(desc_regex, content)
	description = dr.group(1) if dr is not None else None

	region_regex = u'地区:(.*)'
	rr = re.search(region_regex, content)
	region = rr.group(1) if rr is not None else None

	birth_regex = u'生日:(.*)'
	br = re.search(birth_regex, content)
	birthday = br.group(1) if br is not None else None

	blog_regex = u''
	blog = None

	status_regex = u'感情状况：(.*)'
	sta_r = re.search(status_regex, content)
	status = sta_r.group(1) if sta_r is not None else None

	sex_regex = u'性取向:(.*)'
	sr = re.search(sex_regex, content)
	sexuality = sr.group(1) if sr is not None else None
	if sexuality:
		if sexuality == '女':
			sexuality = 0
		else:
			sexuality = 1
	else:
		sexuality = -1

	blood_regex = u''
	bloodtype = None

	fashion_regex = u'达人:(.*)'
	fr = re.search(fashion_regex, content)
	fashion = fr.group(1) if fr is not None else None

	return gender, description,region, birthday, blog, status, sexuality, bloodtype, fashion
	
def taginfo_re(content):
	tag_regex = u'标签:(\n.*)+更多'
	tr = re.search(tag_regex, content)
	taginfo = tr.group() if tr is not None else None
	if taginfo:
		return taginfo.replace('\n','').split()
	else:
		return None
	
def education_re(content):
	school_regex = u'学习经历(\n.*)+级'
	sr = re.search(school_regex, content)
	school = sr.group() if sr is not None else None
	if school:
		school = school.replace('\n','').replace('·','').split()[1:]
		sname = []
		stime = []
		for i,s in enumerate(school):
			if i % 2 == 0:
				sname.append(s)
			else:
				stime.append(s)
		return sname, stime
	else:
		return None

def contact_re(content):
	pass
def employment_re(content):
	employ_regex = u'工作经历(\n.*)+年'
	er = re.search(employ_regex, content)
	employment = er.group() if er is not None else None
	if employment:
		employment = employment.replace('\n','').replace('·','').split()[1:]
		ename = []
		etime = []
		for i,e in enumerate(employment):
			if i % 2 == 0:
				ename.append(e)
			else:
				etime.append(e)
		return ename, etime
	else:
		return None
		
def weibodetail_re(content):
	pass
def main():
	pass

if __name__ == '__main__':
	main()