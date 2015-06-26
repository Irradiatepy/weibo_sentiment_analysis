# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *
from pgu import gui
from getconnect import GetConnect
import my_text_processing as tp
reload(sys)
from intermediate import Intermediate
sys.setdefaultencoding('utf-8')
##########################################################
# 初始化中间层对象，中间层是用来连接该图形化界面与实现该图形化
weibo_interm = Intermediate()
# 初始化数据库访问层
myconnect = GetConnect()
##########################################################
def get_random_weiboid(schoolname):
	'随机返回一个学校的微博用户id'
	get_weibo_id_sql = "select weiboid from %s where is_wb_ori_no_pic = 1 order by rand() limit 1;" % schoolname
	results = myconnect.getData(get_weibo_id_sql)
	if results:
		weiboid = results[0][0]
	else:
		print "get weiboid wrong"
		weiboid = '2591961830'
	return weiboid
##########################################################
class MachineLearningAnalysis(gui.Dialog):
	def __init__(self, **params):
		title = gui.Label("Weibo Machine Learning Analysis")
		container = gui.Container(width=500, height=400)
		td_style = {"padding_right": 10}
		############################
		table = gui.Table(width=400, height=300)

		table.tr()
		table.td(gui.Label("Dlut", style=td_style, cls="h2"))
		dut_button = gui.Button("School")
		dut_button.connect(gui.CLICK, self.show_machine_analysis, 'dlut')
		table.td(dut_button, style=td_style)
		dut_person_button = gui.Button("Person")
		dut_person_button.connect(gui.CLICK, self.show_person_person_analysis, 'dlut')
		table.td(dut_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Tsinghua", style=td_style, cls="h2"))
		Tsinghua_button = gui.Button("School")
		Tsinghua_button.connect(gui.CLICK, self.show_machine_analysis, 'tsinghua')
		table.td(Tsinghua_button, style=td_style)
		Tsinghua_person_button = gui.Button("Person")
		Tsinghua_person_button.connect(gui.CLICK, self.show_person_person_analysis, 'tsinghua')
		table.td(Tsinghua_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Peking", style=td_style, cls="h2"))
		peking_button = gui.Button("School")
		peking_button.connect(gui.CLICK, self.show_machine_analysis, 'peking')
		table.td(peking_button, style=td_style)
		peking_person_button = gui.Button("Person")
		peking_person_button.connect(gui.CLICK, self.show_person_person_analysis, 'peking')
		table.td(peking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Nanking", style=td_style, cls="h2"))
		naking_button = gui.Button("School")
		naking_button.connect(gui.CLICK, self.show_machine_analysis, 'nanking')
		table.td(naking_button, style=td_style)
		naking_person_button = gui.Button("Person")
		naking_person_button.connect(gui.CLICK, self.show_person_person_analysis, 'nanking')
		table.td(naking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Ecupsl", style=td_style, cls="h2"))
		ecupsl_button = gui.Button("School")
		ecupsl_button.connect(gui.CLICK, self.show_machine_analysis, 'ecupsl')
		table.td(ecupsl_button, style=td_style)
		ecupsl_person_button = gui.Button("Person")
		ecupsl_person_button.connect(gui.CLICK, self.show_person_person_analysis, 'ecupsl')
		table.td(ecupsl_person_button, style=td_style)
		############################
		container.add(table, 20, 30)
		gui.Dialog.__init__(self, title, container)
	def show_machine_analysis(self, schoolname):
		weibo_interm.show_school_machine_analysis(schoolname)
	def show_person_person_analysis(self, schoolname):
		pass
##########################################################
class WeiboWordContrast(gui.Dialog):
	click_values = []
	def __init__(self, **params):
		
		title = gui.Label("Weibo Word Contrast")
		container = gui.Container(width=500, height=400)
		td_style = {'padding_right':10}
		#################################
		table = gui.Table(width=490, height=300)
		g = gui.Group()

		table.tr()
		table.td(gui.Label("Dlut", style=td_style, cls="h2"))
		check_box_1 = gui.Checkbox(g, value=1)
		check_box_1.connect(gui.CLICK, self.get_checked,1)
		table.td(check_box_1)

		table.td(gui.Label("Tsinghua", style=td_style, cls="h2"))
		check_box_2 = gui.Checkbox(g, value=2)
		check_box_2.connect(gui.CLICK, self.get_checked,2)
		table.td(check_box_2)

		table.td(gui.Label("Peking", style=td_style, cls="h2"))
		check_box_3 = gui.Checkbox(g, value=3)
		check_box_3.connect(gui.CLICK, self.get_checked,3)
		table.td(check_box_3)

		table.tr()
		table.td(gui.Label("Naking", style=td_style, cls="h2"))
		check_box_4 = gui.Checkbox(g, value=4)
		check_box_4.connect(gui.CLICK, self.get_checked,4)
		table.td(check_box_4)

		table.td(gui.Label("Ecupsl", style=td_style, cls="h2"))
		check_box_5 = gui.Checkbox(g, value=5)
		check_box_5.connect(gui.CLICK, self.get_checked,5)
		table.td(check_box_5)
		'''
		table.tr()
		table.td(gui.Label("With IDF", style=td_style, cls="h2"))
		check_box_6 = gui.Checkbox(g, value=6)
		check_box_6.connect(gui.CLICK, self.get_checked,6)
		table.td(check_box_6)

		table.td(gui.Label("Without IDF", style=td_style, cls="h2"))
		check_box_7 = gui.Checkbox(g, value=7)
		check_box_7.connect(gui.CLICK, self.get_checked,7)
		table.td(check_box_7)
		'''
		table.tr()
		table.td(gui.Label("Show difference", style=td_style, cls="h2"))
		word_contrast_button = gui.Button("Click")
		word_contrast_button.connect(gui.CLICK, self.show_word_contrast, -1)
		table.td(word_contrast_button)

		table.td(gui.Label("clear", style=td_style, cls="h2"))
		check_box_7 = gui.Checkbox(g, value=0)
		check_box_7.connect(gui.CLICK, self.clear_value,0)
		table.td(check_box_7)
		#################################
		container.add(table, 1, 10)
		gui.Dialog.__init__(self, title, container)

	def get_checked(self, value):
		WeiboWordContrast.click_values.append(value)
		print set(WeiboWordContrast.click_values)
		#print value
	def show_word_contrast(self, value):
		print set(WeiboWordContrast.click_values)
		weibo_interm.show_school_word_contrast(WeiboWordContrast.click_values[0],WeiboWordContrast.click_values[1])
	def clear_value(self, value):
		WeiboWordContrast.click_values = []
##########################################################
class DocDialog(gui.Dialog):
	def __init__(self, **params):
		title = gui.Label("Doc content")
		container = gui.Container(width=500, height=400)
		td_style = {"padding_right": 10}
		doc = gui.Document(width=400)
		space = title.style.font.size(" ")
		contents = params['contents']
		doc.block(align=0)
		#for content in contents:
		'''for word in """Cuzco's Paint v1.0 by Phil Hassey""".split(" "):
			doc.add(gui.Label(word))
			doc.space(space)
		doc.br(space[1])'''
		doc.block(align=-1)

		for w in contents:
			doc.add(gui.Label(w[0]))
			doc.br(space[1])
			print '', w[0], w[1], w[2], w[3], w[4]

		container.add(gui.ScrollArea(doc, 470, 370), 20, 20)
		gui.Dialog.__init__(self, title, container)
##########################################################
class DictAnalysis(gui.Dialog):
	def __init__(self, **params):
		title = gui.Label("Weibo Dict Analysis")
		container = gui.Container(width=500, height=400)
		td_style = {"padding_right": 10}
		############################
		table = gui.Table(width=400, height=300)

		table.tr()
		table.td(gui.Label("Dlut", style=td_style, cls="h2"))
		dut_button = gui.Button("School")
		dut_button.connect(gui.CLICK, self.show_dict_result, 'dlut')
		table.td(dut_button, style=td_style)
		dut_person_button = gui.Button("Person")
		dut_person_button.connect(gui.CLICK, self.show_dict_person_result, 'dlut')
		table.td(dut_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Tsinghua", style=td_style, cls="h2"))
		Tsinghua_button = gui.Button("School")
		Tsinghua_button.connect(gui.CLICK, self.show_dict_result, 'tsinghua')
		table.td(Tsinghua_button, style=td_style)
		Tsinghua_person_button = gui.Button("Person")
		Tsinghua_person_button.connect(gui.CLICK, self.show_dict_person_result, 'tsinghua')
		table.td(Tsinghua_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Peking", style=td_style, cls="h2"))
		peking_button = gui.Button("School")
		peking_button.connect(gui.CLICK, self.show_dict_result, 'peking')
		table.td(peking_button, style=td_style)
		peking_person_button = gui.Button("Person")
		peking_person_button.connect(gui.CLICK, self.show_dict_person_result, 'peking')
		table.td(peking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Nanking", style=td_style, cls="h2"))
		naking_button = gui.Button("School")
		naking_button.connect(gui.CLICK, self.show_dict_result, 'nanking')
		table.td(naking_button, style=td_style)
		naking_person_button = gui.Button("Person")
		naking_person_button.connect(gui.CLICK, self.show_dict_person_result, 'nanking')
		table.td(naking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Ecupsl", style=td_style, cls="h2"))
		ecupsl_button = gui.Button("School")
		ecupsl_button.connect(gui.CLICK, self.show_dict_result, 'ecupsl')
		table.td(ecupsl_button, style=td_style)
		ecupsl_person_button = gui.Button("Person")
		ecupsl_person_button.connect(gui.CLICK, self.show_dict_person_result, 'ecupsl')
		table.td(ecupsl_person_button, style=td_style)
		############################
		container.add(table, 20, 30)
		gui.Dialog.__init__(self, title, container)
	def show_dict_result(self, schoolname):
		weibo_interm.show_school_dict_analysis(schoolname)
	def show_dict_person_result(self, school):
		print school,"person"
		weiboid = get_random_weiboid(school)
		weibo_content_results = tp.get_one_weibo_data(schoolname=school, weiboid=weiboid)
		mydocdialog = DocDialog(contents=weibo_content_results)
		mydocdialog.open()
		weibo_interm.show_person_dict_analysis(school, weiboid)
##########################################################
class MeaningContrast(gui.Dialog):
	def __init__(self, **params):
		title = gui.Label("Weibo meaning Contrast")
		container = gui.Container(width=500, height=400)
		td_style = {"padding_right": 10}
		############################
		table = gui.Table(width=400, height=300)

		table.tr()
		table.td(gui.Label("Dlut", style=td_style, cls="h2"))
		dut_button = gui.Button("School")
		dut_button.connect(gui.CLICK, self.show_school_meaning_contrast, 'dlut')
		table.td(dut_button, style=td_style)
		dut_person_button = gui.Button("Person")
		dut_person_button.connect(gui.CLICK, self.show_person_meaning_contrast, 'dlut')
		table.td(dut_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Tsinghua", style=td_style, cls="h2"))
		Tsinghua_button = gui.Button("School")
		Tsinghua_button.connect(gui.CLICK, self.show_school_meaning_contrast, 'tsinghua')
		table.td(Tsinghua_button, style=td_style)
		Tsinghua_person_button = gui.Button("Person")
		Tsinghua_person_button.connect(gui.CLICK, self.show_person_meaning_contrast, 'tsinghua')
		table.td(Tsinghua_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Peking", style=td_style, cls="h2"))
		peking_button = gui.Button("School")
		peking_button.connect(gui.CLICK, self.show_school_meaning_contrast, 'peking')
		table.td(peking_button, style=td_style)
		peking_person_button = gui.Button("Person")
		peking_person_button.connect(gui.CLICK, self.show_person_meaning_contrast, 'peking')
		table.td(peking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Nanking", style=td_style, cls="h2"))
		naking_button = gui.Button("School")
		naking_button.connect(gui.CLICK, self.show_school_meaning_contrast, 'nanking')
		table.td(naking_button, style=td_style)
		naking_person_button = gui.Button("Person")
		naking_person_button.connect(gui.CLICK, self.show_person_meaning_contrast, 'nanking')
		table.td(naking_person_button, style=td_style)

		table.tr()
		table.td(gui.Label("Ecupsl", style=td_style, cls="h2"))
		ecupsl_button = gui.Button("School")
		ecupsl_button.connect(gui.CLICK, self.show_school_meaning_contrast, 'ecupsl')
		table.td(ecupsl_button, style=td_style)
		ecupsl_person_button = gui.Button("Person")
		ecupsl_person_button.connect(gui.CLICK, self.show_person_meaning_contrast, 'ecupsl')
		table.td(ecupsl_person_button, style=td_style)
		############################
		container.add(table, 20, 30)
		gui.Dialog.__init__(self, title, container)

	def show_school_meaning_contrast(self, school):
		print school
		weibo_interm.show_school_meaning_contrast(school)

	def show_person_meaning_contrast(self, school):
		print school,"person"
		weiboid = get_random_weiboid(school)
		weibo_content_results = tp.get_one_weibo_data(schoolname=school, weiboid=weiboid)
		mydocdialog = DocDialog(contents=weibo_content_results)
		mydocdialog.open()
		weibo_interm.show_person_meaning_contrast(school, weiboid)
##########################################################

def main():
	#initate pygame just for display window name
	pygame.init()      
	#Set Window name
	pygame.display.set_caption((u'Weibo sentiment analysis programme').encode('utf-8'))    
	app = gui.Desktop()
	app.connect(gui.QUIT, app.quit, None)
	main_frame = gui.Container(width=800, height=600)
	main_frame.add(gui.Label("Network Sentiment Analysis", cls="h1"), 30, 30)
	td_style = {'padding_right': 10}
	######################
	m_table = gui.Table(border="32", width=600, height=400)

	m_table.tr()
	m_table.td(gui.Label("Weibo meaning contrast", style=td_style, cls="h2"))
	m_table.td(gui.Label("Dict Analysis", style=td_style, cls="h2"))

	m_table.tr()
	w_m_c_b = gui.Button("Click me")
	w_m_c_dialog = MeaningContrast()
	w_m_c_b.connect(gui.CLICK, w_m_c_dialog.open, None)
	m_table.td(w_m_c_b, style=td_style)

	d_a_b = gui.Button("Click me")
	d_a_dialog = DictAnalysis(weiboid='123223')
	d_a_b.connect(gui.CLICK, d_a_dialog.open, None)
	m_table.td(d_a_b, style=td_style)

	m_table.tr()
	m_table.td(gui.Label("Weibo word contrast", style=td_style, cls="h2"))
	m_table.td(gui.Label("Machine Learning Analysis", style=td_style, cls="h2"))
	
	m_table.tr()
	w_w_c_b = gui.Button("Click me")
	w_w_c_b_dialog = WeiboWordContrast()
	w_w_c_b.connect(gui.CLICK, w_w_c_b_dialog.open, None)
	m_table.td(w_w_c_b, style=td_style)

	m_l_a_b = gui.Button("Click me")
	m_l_a_b_dialog = MachineLearningAnalysis()
	m_l_a_b.connect(gui.CLICK, m_l_a_b_dialog.open, None)
	m_table.td(m_l_a_b, style=td_style)
	##################################
	main_frame.add(m_table, 70, 120)
	app.run(main_frame)
if __name__ == '__main__':
	main()

