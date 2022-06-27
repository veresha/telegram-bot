import requests
from users_info_storage.users_info_storage import users_info_dict
from telebot.types import Message

url = "https://hotels4.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "27c3b873d3msh5961c422d735f01p1d55e2jsne5957d6966a4",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def get_city_districts(city) -> dict:
	endpoint_city_id = 'locations/v2/search'
	querystring = {"query": city}

	response = requests.request("GET", url + endpoint_city_id, headers=headers, params=querystring)
	districts = {}
	for district in response.json()['suggestions'][0]['entities']:
		districts[district['name']] = district['destinationId']
	return districts


def get_hotels(message: Message):
	endpoint_hotels = 'properties/list'
	check_in = users_info_dict[message.from_user.id][3]['check_in']
	check_out = users_info_dict[message.from_user.id][4]['check_out']
	price = users_info_dict[message.from_user.id][0]['hotels_price']
	hotels_num = users_info_dict[message.from_user.id][5]['hotels_num']
	querystring = {
		"destinationId": users_info_dict[message.from_user.id][2]['destination_id'], "pageNumber": "1",
		"pageSize": hotels_num, "checkIn": check_in, "checkOut": check_out, "adults1": "1", "sortOrder": price,
		"locale": "en_US", "currency": "USD"
	}
	response = requests.request("GET", url + endpoint_hotels, headers=headers, params=querystring)

	hotels = response.json()['data']['body']["searchResults"]['results']

	for i in hotels:
		print(i['name'])
		print(i['guestReviews']['rating'])
		print(i['ratePlan']['price']['current'])
		print('***********')
