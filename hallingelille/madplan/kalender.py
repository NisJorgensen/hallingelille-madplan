# coding=utf-8
from django_ical.views import ICalFeed
from models import Maddag
import datetime
from django.conf import settings

HOSTNAME = settings.ALLOWED_HOSTS[0]

class MaddagFeed(ICalFeed):

	file_name = "faellesspisning.ics"

	def title(self):
		return 'Hallingelille Fællesspisning'

	def items(self):
		return Maddag.objects.filter(dato__gte=datetime.date.today()).order_by('dato')

	def item_link(self,item):
		return 'http://%s/maddag/%s' % (HOSTNAME,item.dato)

	def item_title(self,item):
		return item.menu or u"Fællesspisning"

	def item_description(self,item):
		if item.menu:
			return item.menu
		else:
		   return self.item_title(item)

	def item_start_datetime(self, item):
        	return item.spisetid(naive=False)
