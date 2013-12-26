import datetime
try:
	from dateutil.parser import parse
except:
	def parse(input):
		return datetime.datetime.strptime(input, "%Y-%m-%d").date()

def parse_date(date):
	if date == 'today':
		return datetime.date.today()
	elif date == 'tomorrow':
		return datetime.date.fromordinal(datetime.date.today().toordinal()+1)
	elif date == 'nextweek':
		return datetime.date.fromordinal(datetime.date.today().toordinal()+7)
	return parse(date)
