import requests
from users_info_storage.users_info_storage import users_info_dict
from telebot.types import Message

url = "https://hotels4.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "dfdcae03ffmsh6500f2709b7b791p162bf0jsn593c1397f57a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def request_to_api(endpoint: str, querystring: dict):
	try:
		response = requests.get(url + endpoint, headers=headers, params=querystring, timeout=10)
		if response.status_code == requests.codes.ok:
			return response
		else:
			print('Ошибка', response.status_code)
	except Exception:
		print('Ошибка', Exception)


def get_city_districts(city: str) -> dict:
	endpoint_city_id = 'locations/v2/search'
	querystring = {"query": city}
	response = request_to_api(endpoint=endpoint_city_id, querystring=querystring)
	districts = {}
	for district in response.json().get('suggestions', {})[0].get('entities'):
		districts[district['name']] = district['destinationId']
	return districts


def get_hotels(message: Message) -> dict:
	endpoint_hotels = 'properties/list'
	destination_id = users_info_dict.get(message.from_user.id)[2]['destination_id']
	check_in = users_info_dict.get(message.from_user.id)[3]['check_in']
	check_out = users_info_dict.get(message.from_user.id)[4]['check_out']
	price = users_info_dict.get(message.from_user.id)[0]['hotels_price']
	hotels_num = users_info_dict.get(message.from_user.id)[5]['hotels_num']
	try:
		min_price = users_info_dict.get(message.from_user.id)[6]['min_price']
		max_price = users_info_dict.get(message.from_user.id)[7]['max_price']
		# min_dist = users_info_dict[message.from_user.id][8]['min_dist']
		# max_dist = users_info_dict[message.from_user.id][5]['max_dist']
	except IndexError:
		min_price = None
		max_price = None
	querystring = {
		"destinationId": destination_id,
		"pageNumber": "1",
		"pageSize": hotels_num,
		"checkIn": check_in,
		"checkOut": check_out,
		"priceMin": min_price,
		"priceMax": max_price,
		"adults1": "1", "sortOrder": price,
		"locale": "ru_RU", "currency": "USD"
	}
	response = request_to_api(endpoint=endpoint_hotels, querystring=querystring)
	hotels = response.json().get('data', {}).get('body', {}).get("searchResults", {}).get('results')
	hotels_info = {}
	for hotel in hotels:
		hotels_info[hotel.get("id", {})] = (f'🏨 Название отеля: {hotel.get("name", {})}\n'
									f'🌎 Адрес: {hotel.get("address", {}).get("streetAddress", {})}\n'
									f'🌇 Расстояние до центра: {hotel.get("landmarks", {})[0].get("distance", {})}\n'
									f'⭐ Рейтинг от пользователей: {hotel.get("guestReviews", {}).get("rating", {})}\n'
									f'✨ Рейтинг по звёздам: {hotel.get("starRating", {})}\n'
									f'1️⃣ Цена за ночь: {hotel.get("ratePlan", {}).get("price", {}).get("current", {})}\n'
									f'🌐 Сайт: https://www.hotels.com/ho{hotel.get("id", {})}')
	return hotels_info


def get_photos(hotel_id: str, photos_num: int) -> list:
	endpoint_photos = 'properties/get-hotel-photos'
	querystring = {"id": hotel_id}
	response = request_to_api(endpoint=endpoint_photos, querystring=querystring)
	final_photos = []
	photos = response.json().get("hotelImages", {})
	for num, photo in enumerate(photos, 1):
		final_photos.append(str(photo.get('baseUrl', {})).replace('{size}', 'y'))
		if num == photos_num:
			break
	return final_photos
