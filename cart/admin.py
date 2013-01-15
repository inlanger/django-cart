#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Cart
from models import Item

admin.site.register(Cart)
admin.site.register(Item)
