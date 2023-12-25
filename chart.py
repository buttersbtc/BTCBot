import datetime
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

def chart(api_response):
	multiplier = 1
	if api_response['unit'] == "USD":
		api_response['unit'] = "Thousands of USD"
		multiplier = 0.001
	if api_response['unit'] == "Bytes":
		api_response['unit'] = "Megabytes"
		multiplier = 0.000001
	pyplot.title(api_response['name'])
	pyplot.ylabel(api_response['unit'])
	pyplot.xlabel(api_response['period'])
	x = [datetime.datetime.utcfromtimestamp(value['x']) for value in api_response['values']]
	y = [(float(value['y']) * multiplier) for value in api_response['values']]
	pyplot.plot_date(x, y, linestyle='-', markersize=0.0)
	pyplot.xticks(rotation=45)
	pyplot.subplots_adjust(bottom=0.20)
	buf = io.BytesIO()
	pyplot.savefig(buf, format='png')
	buf.seek(0)
	pyplot.clf()
	return buf