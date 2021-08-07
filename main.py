import requests
from pprint import pprint
import os


class YandexDisk:
    def __init__(self, token):
        self.token = UserData.token_ya_disk

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
            }

    def create_a_folder(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        name_folder = f'photo_vk_id{UserData.id_vk}'
        params = {"path": name_folder}
        response = requests.put(url, headers=headers, params=params).json()
        res = f'/{name_folder}/'
        return res

    def upload_file_to_ya_disk(self, name_file, url_file_path):
        href = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        url = url_file_path
        name_folder = self.create_a_folder()
        path = f'{name_folder}{name_file}.jpg'
        params = {
            'path': path,
            'url': url
            }
        response = requests.post(href, headers=self.get_headers(), params=params)
        res = response.json()
        return res


class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version,
            }

    def get_photos(self, count_photo=5):
        self.count_photo = count_photo
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': new_user_data.id_vk,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count_photo
            }
        response = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        if response.status_code != 200:
            print("ERROR")
            return

        dict_photo_info = response.json()
        list_photo_info = dict_photo_info['response']['items']

        dict_url_and_name_photo = {}
        for photo_info in list_photo_info:
            photo_sizes_list = photo_info['sizes']
            name_photo = photo_info['likes']['count']
            date_photo = photo_info['date']

            dict_width_and_url_photo = {}
            for type_photo in photo_sizes_list:
                list_type_and_url = []
                url_photo = type_photo['url']
                width = type_photo['width']
                type_photo = type_photo['type']
                list_type_and_url.append(type_photo)
                list_type_and_url.append(url_photo)
                dict_width_and_url_photo[width] = list_type_and_url
            url_photo_list = list(dict_width_and_url_photo.values())
            width_list = list(dict_width_and_url_photo.keys())

            largest_image_link = url_photo_list[width_list.index(max(width_list))]

            for name in dict_url_and_name_photo.keys():
                if name == name_photo:
                    name_photo = f'{name_photo}_{date_photo}'
            dict_url_and_name_photo[name_photo] = largest_image_link

        ya_disk_new_folder = YandexDisk(UserData.token_ya_disk)
        ya_disk_new_folder.create_a_folder()
        log_json = []
        for name_photo, url_photo in dict_url_and_name_photo.items():
            ya_disk_new_folder.upload_file_to_ya_disk(name_photo, url_photo[1])
            info_about_file = {"file_name": None, "size": None}
            info_about_file["file_name"] = f'{name_photo}.jpg'
            info_about_file["size"] = url_photo[0]
            log_json.append(info_about_file)

        with open(f'photo_vk_id{UserData.id_vk}.json', 'a', encoding='utf-8') as file:
            file.write(f'\nphoto_vk_id{UserData.id_vk}\n{log_json}')
       #return log_json


class UserData:
    id_vk = input('Введите, пожалуйста, номер страницы(id) на сайте https://vk.com/: ')
    token_ya_disk = input('Введите, пожалуйста, TOKEN c Полигона Яндекс.Диска: ')


if __name__ == '__main__':
    vk_client = VkUser('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008', '5.131')
    new_user_data = UserData
    pprint(vk_client.get_photos())
