import sys
from pprint import pprint

API_Key = '6ad0df660f00129f96ce5c5df90c9376'

try:
	import requests
except ImportError:
	print('The `requests` package is required. Install with: pip install requests')
	sys.exit(1)

def get_city_from_args_or_input():
	if len(sys.argv) > 1:
		return ' '.join(sys.argv[1:])
	try:
		return input('Enter City Name: ')
	except EOFError:
		print('No city provided.')
		sys.exit(1)

def main():
	city = get_city_from_args_or_input().strip()
	if not city:
		print('City name is empty.')
		sys.exit(1)

	base_url = 'https://api.openweathermap.org/2.5/weather'
	params = {'q': city, 'appid': API_Key}

	try:
		resp = requests.get(base_url, params=params, timeout=10)
	except requests.RequestException as e:
		print('Network error:', e)
		sys.exit(1)

	try:
		weather_data = resp.json()
	except ValueError:
		print('Invalid response from API (not JSON). Status:', resp.status_code)
		sys.exit(1)

	if resp.status_code != 200:
		msg = weather_data.get('message') if isinstance(weather_data, dict) else None
		print(f'API error (status {resp.status_code}):', msg or weather_data)
		sys.exit(1)

	pprint(weather_data)

if __name__ == '__main__':
	main()