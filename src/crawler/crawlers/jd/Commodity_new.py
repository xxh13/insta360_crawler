#-*- coding: UTF-8 -*-
class Commodity:
    name = ""
    price = 0.0
    comment = 0
    id = ""
    sales = 0
    good_rate = ''

    def __init__(self, name, price, comment, id, good_rate):
        self.name = name
        self.price = price
        self.comment = comment
        self.id = id
        self.good_rate = good_rate

    def setPrice(self, price):
        self.price = price

    def setName(self, name):
        self.name = name

    def setComment(self, comment):
        self.comment = comment

    def setTitle(self, good_rate):
        self.good_rate = good_rate

    def setId(self,id):
        self.id = id

    def setSales(self,sales):
        self.sales = sales


    def show(self):
        print "name: ",self.name
        print "price: ",self.price
        print "comment: ",self.comment
        print "id: ", self.id
        print "good_rate: ", self.good_rate
        print "sales: ", self.sales
        print