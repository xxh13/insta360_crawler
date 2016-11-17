#-*- coding: UTF-8 -*-
class Commodity:
    name = ""
    price = 0.0
    comment = 0
    link = ""
    id = ""
    sales = 0
    title = ''

    def __init__(self, name, price, comment, link, id, title):
        self.name = name
        self.price = price
        self.comment = comment
        self.link = link
        self.id = id
        self.title = title

    def setPrice(self, price):
        self.price = price

    def setName(self, name):
        self.name = name

    def setComment(self, comment):
        self.comment = comment

    def setLink(self, link):
        self.link = link

    def setTitle(self, title):
        self.title = title

    def setId(self,id):
        self.id = id

    def setSales(self,sales):
        self.sales = sales


    def show(self):
        print "name: ",self.name
        print "price: ",self.price
        print "comment: ",self.comment
        print "link: ",self.link
        print "id: ", self.id
        print "title: ", self.title
        print