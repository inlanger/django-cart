#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import models

CART_ID = 'CART-ID'


class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, owner=request.user, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    # get cart total function
    def get_total(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result

    def new(self, request):
        cart = models.Cart(owner=request.user, creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity):
        # try to get valid quantity value
        try:
            quantity = int(quantity)
        except:
            quantity = 1

        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            # if product in cart and user try to add more than 1 item
            item.quantity += quantity
            item.save()

    def remove(self, item):
        try:
            item = models.Item.objects.get(cart=self.cart, product=item)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def checkout(self):
        self.cart.checked_out = True
        self.cart.save()
        return True