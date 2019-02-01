# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.core.window import Window

import sqlite3

conn = sqlite3.connect('rest_db.sqlite3')
c = conn.cursor()


class Food_Button(Button):
	pass

class Title_Label(Label):
	pass



class Total_Popup(ModalView):

	food_list = DictProperty()
	menu_grid = ObjectProperty()

	title = 'Receipt'
	back_btn = 'Back'
	new_order_btn = 'New Order'
	total_title = 'Total'

	lbl1 = 'Order'
	lbl2 = 'One Price'
	lbl3 = 'Quantity'
	lbl4 = 'Total Price'


	def __init__(self, **kwargs):
		super(Total_Popup, self).__init__(**kwargs)

		self.app_inst =  App.get_running_app()

		self.checks_list = []

		self.menu_grid.bind(minimum_height=self.menu_grid.setter('height'))					

		self.popup_status = False

	def open_pop(self):

		self.popup_status = True

		total_price = 0

		self.menu_grid.clear_widgets()

		for i, n in self.food_list.items() :

			for typ, pric in n.items() :

				if typ == 'one':
					add = ''

				elif typ == 's':
					add = ' small'
				elif typ == 'm':
					add = ' medium'
				elif typ == 'l':
					add = ' large'


				name = Food_Button(text = i+add, size_hint_x= .4, size_hint_y= None, height= '50dp', font_size=self.height/2)

				price = Label(text = str(pric[1]), color=[.8,.8,.8, 1], bold=True, size_hint_x= .2)

				quantity = Label(text = str(pric[0]), color=[.8,.8,.8, 1], bold=True, size_hint_x= .2)

				one_price = int(pric[0]) * int(pric[1])

				one_price_box = Label(text = str(one_price), color=[.8,.8,.8, 1], bold=True, size_hint_x= .2)

				self.menu_grid.add_widget(name)
				self.menu_grid.add_widget(price)
				self.menu_grid.add_widget(quantity)
				self.menu_grid.add_widget(one_price_box)

				total_price += one_price

		self.total_box.text = str(total_price)

		self.open()


	def new_order_clicked(self):

		self.dismiss()

		self.app_inst.manage_screen.add_to_today_earning(self.total_box.text)

		self.app_inst.menu_screen.reset_all_food_grid()

		self.popup_status = False



class Header_1(GridLayout):

	lbl1 = ObjectProperty()
	lbl2 = ObjectProperty()
	lbl3 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Header_1, self).__init__(**kwargs)

		self.lbl1.text = 'Name'
		self.lbl2.text = 'Price'
		self.lbl3.text = 'Quantity'



class Header_2(GridLayout):

	lbl1 = ObjectProperty()
	lbl2 = ObjectProperty()
	lbl3 = ObjectProperty()
	lbl4 = ObjectProperty()
	lbl5 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Header_2, self).__init__(**kwargs)

		self.lbl1.text = 'Name'
		self.lbl2.text = 'Small Price'
		self.lbl3.text = 'Large Price'
		self.lbl4.text = 'Small no.'
		self.lbl5.text = 'Large no.'

class Header_3(GridLayout):

	lbl1 = ObjectProperty()
	lbl2 = ObjectProperty()
	lbl3 = ObjectProperty()
	lbl4 = ObjectProperty()
	lbl5 = ObjectProperty()
	lbl6 = ObjectProperty()
	lbl7 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Header_3, self).__init__(**kwargs)

		self.lbl1.text = 'Name'
		self.lbl2.text = 'Small Price'
		self.lbl3.text = 'Medium Price'
		self.lbl4.text = 'Large Price'
		self.lbl5.text = 'Small no.'
		self.lbl6.text = 'Medium no.'
		self.lbl7.text = 'Large no.'

class Food_BoxLayout_1(BoxLayout):

	food_name = ObjectProperty()

	check_1 = ObjectProperty()
	price_1 = ObjectProperty()
	inp_1 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Food_BoxLayout_1, self).__init__(**kwargs)

		self.food_n = ''

		self.app_inst =  App.get_running_app()

		self.check_1.bind(active=self.on_checkbox_active_1)



	def on_checkbox_active_1(self, check_1, value):

		n = self.food_name.text

		if value == True :

			i1 = {'one': [self.inp_1.text,self.price_1.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i1)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i1

			self.app_inst.menu_screen.total_pop.checks_list.append(check_1)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['one']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_1)

	def quantity_added_1(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_1.text,self.price_1.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['one'] = new_add



class Food_BoxLayout_2(BoxLayout):

	food_name = ObjectProperty()

	check_1 = ObjectProperty()
	check_2 = ObjectProperty()

	price_1 = ObjectProperty()
	price_2 = ObjectProperty()

	inp_1 = ObjectProperty()
	inp_2 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Food_BoxLayout_2, self).__init__(**kwargs)

		self.food_n = ''

		self.app_inst =  App.get_running_app()

		self.check_1.bind(active=self.on_checkbox_active_1)

		self.check_2.bind(active=self.on_checkbox_active_2)




	def on_checkbox_active_1(self, check_1, value):

		n = self.food_name.text

		if value == True :

			i1 = {'s': [self.inp_1.text,self.price_1.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i1)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i1

			self.app_inst.menu_screen.total_pop.checks_list.append(check_1)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['s']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_1)

	def on_checkbox_active_2(self, check_2, value):

		n = self.food_name.text

		if value == True :

			i2 = {'l': [self.inp_2.text,self.price_2.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i2)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i2

			self.app_inst.menu_screen.total_pop.checks_list.append(check_2)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['l']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_2)


	def quantity_added_1(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_1.text,self.price_1.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['s'] = new_add


	def quantity_added_2(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_2.text,self.price_2.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['l'] = new_add




class Food_BoxLayout_3(BoxLayout):

	food_name = ObjectProperty()

	check_1 = ObjectProperty()
	check_2 = ObjectProperty()
	check_3 = ObjectProperty()

	price_1 = ObjectProperty()
	price_2 = ObjectProperty()
	price_3 = ObjectProperty()

	inp_1 = ObjectProperty()
	inp_2 = ObjectProperty()
	inp_3 = ObjectProperty()

	def __init__(self, **kwargs):
		super(Food_BoxLayout_3, self).__init__(**kwargs)

		self.food_n = ''

		self.app_inst =  App.get_running_app()

		self.check_1.bind(active=self.on_checkbox_active_1)

		self.check_2.bind(active=self.on_checkbox_active_2)

		self.check_3.bind(active=self.on_checkbox_active_3)

	def on_checkbox_active_1(self, check_1, value):

		n = self.food_name.text

		if value == True :

			i1 = {'s': [self.inp_1.text,self.price_1.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i1)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i1

			self.app_inst.menu_screen.total_pop.checks_list.append(check_1)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['s']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_1)

	def on_checkbox_active_2(self, check_2, value):

		n = self.food_name.text

		if value == True :

			i2 = {'m': [self.inp_2.text,self.price_2.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i2)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i2

			self.app_inst.menu_screen.total_pop.checks_list.append(check_2)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['m']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_2)


	def on_checkbox_active_3(self, check_3, value):

		n = self.food_name.text

		if value == True :

			i3 = {'l': [self.inp_3.text,self.price_3.text] }

			if self.food_n in self.app_inst.menu_screen.total_pop.food_list :
				self.app_inst.menu_screen.total_pop.food_list[self.food_n].update(i3)
			else:
				self.app_inst.menu_screen.total_pop.food_list[self.food_n] = i3

			self.app_inst.menu_screen.total_pop.checks_list.append(check_3)

		elif value == False and self.app_inst.menu_screen.total_pop.popup_status == False:

			del self.app_inst.menu_screen.total_pop.food_list[self.food_n]['l']

			self.app_inst.menu_screen.total_pop.checks_list.remove(check_3)


	def quantity_added_1(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_1.text,self.price_1.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['s'] = new_add


	def quantity_added_2(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_2.text,self.price_2.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['m'] = new_add


	def quantity_added_3(self):

		if self.food_n in self.app_inst.menu_screen.total_pop.food_list :

			new_add = [self.inp_3.text,self.price_3.text]

			self.app_inst.menu_screen.total_pop.food_list[self.food_n]['l'] = new_add




class kebab_screen(Screen):

	food_grid = ObjectProperty()

	def __init__(self, **kwargs):
		super(kebab_screen, self).__init__(**kwargs)

		self.kebab_grid()

	def kebab_grid(self):

		query = c.execute("SELECT * FROM Kebab")
		rows = query.fetchall()

		self.grid1 = GridLayout(cols= 1, padding=3,spacing=3,size_hint_y= None)
		self.grid1.bind(minimum_height=self.grid1.setter('height'))					

		for i in rows:
			self.one_food = Food_BoxLayout_2()

			self.one_food.food_n = i[0]
			self.one_food.food_name.text = i[0]
			self.one_food.price_1.text = str(i[1])
			self.one_food.price_2.text = str(i[2])

			if self.one_food.price_1.text == '0' :
				self.one_food.check_1.disabled = True
				self.one_food.inp_1.disabled = True

			if self.one_food.price_2.text == '0' :
				self.one_food.check_2.disabled = True
				self.one_food.inp_2.disabled = True

			self.grid1.add_widget(self.one_food)

		self.food_grid.add_widget(self.grid1)





class pizza_screen(Screen):

	food_grid = ObjectProperty()

	def __init__(self, **kwargs):
		super(pizza_screen, self).__init__(**kwargs)

		self.pizza_grid()

	def pizza_grid(self):

		query = c.execute("SELECT * FROM Pizza")
		rows = query.fetchall()

		self.grid1 = GridLayout(cols= 1, padding=3,spacing=3,size_hint_y= None)
		self.grid1.bind(minimum_height=self.grid1.setter('height'))					

		for i in rows:
			self.one_food = Food_BoxLayout_3()

			self.one_food.food_n = i[0]
			self.one_food.food_name.text = i[0]
			self.one_food.price_1.text = str(i[1])
			self.one_food.price_2.text = str(i[2])
			self.one_food.price_3.text = str(i[3])

			if self.one_food.price_1.text == '0' :
				self.one_food.check_1.disabled = True
				self.one_food.inp_1.disabled = True

			if self.one_food.price_2.text == '0' :
				self.one_food.check_2.disabled = True
				self.one_food.inp_2.disabled = True

			if self.one_food.price_3.text == '0' :
				self.one_food.check_3.disabled = True
				self.one_food.inp_3.disabled = True


			self.grid1.add_widget(self.one_food)

		self.food_grid.add_widget(self.grid1)




class drinks_screen(Screen):

	food_grid = ObjectProperty()

	def __init__(self, **kwargs):
		super(drinks_screen, self).__init__(**kwargs)

		self.drinks_grid()

	def drinks_grid(self):

		query = c.execute("SELECT * FROM Drinks")
		rows = query.fetchall()

		self.grid1 = GridLayout(cols= 1, padding=3,spacing=3,size_hint_y= None)
		self.grid1.bind(minimum_height=self.grid1.setter('height'))					

		for i in rows:
			self.one_food = Food_BoxLayout_1()

			self.one_food.food_n = i[0]
			self.one_food.food_name.text = i[0]
			self.one_food.price_1.text = str(i[1])

			self.grid1.add_widget(self.one_food)

		self.food_grid.add_widget(self.grid1)




class deserts_screen(Screen):

	food_grid = ObjectProperty()

	def __init__(self, **kwargs):
		super(deserts_screen, self).__init__(**kwargs)

		self.deserts_grid()

	def deserts_grid(self):

		query = c.execute("SELECT * FROM Deserts")
		rows = query.fetchall()

		self.grid1 = GridLayout(cols= 1, padding=3,spacing=3,size_hint_y= None)
		self.grid1.bind(minimum_height=self.grid1.setter('height'))					

		for i in rows:
			self.one_food = Food_BoxLayout_1()

			self.one_food.food_n = i[0]
			self.one_food.food_name.text = i[0]
			self.one_food.price_1.text = str(i[1])

			self.grid1.add_widget(self.one_food)

		self.food_grid.add_widget(self.grid1)



class Menu_Screen(Screen):
	btn = ObjectProperty()

	tbh1 = ObjectProperty()
	tbh2 = ObjectProperty()
	tbh3 = ObjectProperty()
	tbh4 = ObjectProperty()

	total_btn = ObjectProperty()

	header = ObjectProperty()

	admin_title = 'Management'

	sm = ObjectProperty()

	def __init__(self, **kwargs):
		super(Menu_Screen, self).__init__(**kwargs)

		self.btn.text = 'Restaurant'

		self.tbh1.text = 'Kebab'
		self.tbh2.text = 'Pizza'
		self.tbh3.text = 'Drinks'
		self.tbh4.text = 'Deserts'

		self.total_btn.text = 'Reciept'

		self.total_pop = Total_Popup()

		self.kebab_scr = kebab_screen()
		self.pizza_scr = pizza_screen()
		self.drinks_scr = drinks_screen()
		self.deserts_scr = deserts_screen()


		self.sm.add_widget(self.kebab_scr)
		self.sm.add_widget(self.pizza_scr)
		self.sm.add_widget(self.drinks_scr)
		self.sm.add_widget(self.deserts_scr)




		self.toggle_clicked()

	def toggle_clicked(self):

		if self.tbh1.state == 'down' :		# Kebab
			self.header.clear_widgets()
			self.header.add_widget(Header_2())
			self.sm.current = 'kebab_scr'

		elif self.tbh2.state == 'down' :	# pizza
			self.header.clear_widgets()
			self.header.add_widget(Header_3())
			self.sm.current = 'pizza_scr'


		elif self.tbh3.state == 'down' :	# Drinks
			self.header.clear_widgets()
			self.header.add_widget(Header_1())
			self.sm.current = 'drinks_scr'

		elif self.tbh4.state == 'down' :	# Deserts
			self.header.clear_widgets()
			self.header.add_widget(Header_1())
			self.sm.current = 'deserts_scr'


	def go_to_manage_screen(self):
			self.manager.current = 'manage_screen'


	def open_total_pop(self):

		self.total_pop.open_pop()


	def reset_all_food_grid(self):

		x = list(self.total_pop.checks_list)
		for i in x :
			i.active = False



class Manage_Screen(Screen):

	manage_title = 'Management'
	today_earning_title = 'Today Earning'
	reset_title = 'Reset Earning'
	back_btn_title = 'Back'

	earning_amount = ObjectProperty()

	def __init__(self, **kwargs):
		super(Manage_Screen, self).__init__(**kwargs)

		self.app_inst =  App.get_running_app()

		result = c.execute('SELECT * from Config WHERE balance = "Total"')
		amount = result.fetchone()

		self.today_earning_value = amount[1]
		self.earning_amount.text = str(self.today_earning_value)

	def reset_today_earning(self):
		self.today_earning_value = 0		
		self.earning_amount.text = str(self.today_earning_value)

		c.execute('UPDATE Config SET amount = {0} WHERE balance = "Total" '.format(self.today_earning_value) )
		conn.commit()


	def go_to_menu_screen(self):
			self.manager.current = 'menu_screen'


	def add_to_today_earning(self, add):
		self.today_earning_value += int(add)

		self.earning_amount.text = str(self.today_earning_value)
		
		c.execute('UPDATE Config SET amount = {0} WHERE balance = "Total" '.format(self.today_earning_value) )
		conn.commit()

class RestApp(App):

	screens = ObjectProperty()

	def build(self):

		self.sm = ScreenManager()
	
		self.menu_screen = Menu_Screen()
		self.manage_screen = Manage_Screen()

		self.sm.add_widget(self.menu_screen)
		self.sm.add_widget(self.manage_screen)

		return self.sm


if __name__ == '__main__':
	RestApp().run()
