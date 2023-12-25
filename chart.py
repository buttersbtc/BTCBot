import datetime
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

def chart(api_response):
	x = [datetime.datetime.utcfromtimestamp(value['x']) for value in api_response['values']]
	y = [value['y'] for value in api_response['values']]
	pyplot.title(api_response['name'])
	pyplot.ylabel(api_response['unit'])
	pyplot.xlabel(api_response['period'])
	pyplot.plot_date(x, y, linestyle='-')
	buf = io.BytesIO()
	pyplot.savefig(buf, format='png')
	buf.seek(0)
	pyplot.clf()
	return buf