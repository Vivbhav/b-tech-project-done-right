import requests

def scrape(textinput):
	try:
		line1 = []
		response = requests.get(
			'https://en.wikipedia.org/w/api.php',
			params={
				'action': 'query',
				'format': 'json',
				'titles': textinput,
				'prop': 'extracts',
				#'exintro': True,
				'explaintext': True,
			}
		).json()
		page = next(iter(response['query']['pages'].values()))
		#print(page)
		#print(page['extract'])
		output = page['extract']
		lines = output.split('\n')
		fw = open("input.txt", "w")
		for line in lines:
			if '==' in line or line == '' or len(line) < 75:
				pass
			else:
				line1.append(line)
		print(line1)
		return line1
	except KeyError:
		print("Information for such a topic doesn't exist.")
		exit(1)

#output = scrape('MS Dhoni')
#print(output)
