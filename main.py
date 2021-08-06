import requests
from pprint import pprint


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
        name_folder = f'foto_vk_id{UserData.id_vk}'
        params = {"path": name_folder}
        response = requests.put(url, headers=headers, params=params).json()
        res = f'/{name_folder}/'
        return res

    def upload_file_to_ya_disk(self, name_file, url_file_path):
        href = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        url = url_file_path
        name_folder = self.create_a_folder()
        path = f'{name_folder}{name_file}.jpg'
        params = {'path': path, 'url': url}
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

    def get_photos(self, count_foto=5):
        self.count_foto = count_foto
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': new_user_data.id_vk,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count_foto
            }
        response = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        if response.status_code != 200:
            print("ERROR")
            return

        dict_foto_info = response.json()
        list_foto_info = dict_foto_info['response']['items']

        dict_url_and_name_photo = {}
        for foto_info in list_foto_info:
            name_foto = foto_info['likes']['count']
            foto_sizes_list = foto_info['sizes']
            dict_height_and_url_photo = {}
            for type_foto in foto_sizes_list:
                url_photo = type_foto['url']
                height = type_foto['width']
                dict_height_and_url_photo[url_photo] = height

            url_photo_list = list(dict_height_and_url_photo.keys())
            heights_list = list(dict_height_and_url_photo.values())
            largest_image_link = url_photo_list[heights_list.index(max(heights_list))]

            dict_url_and_name_photo[name_foto] = largest_image_link

            ya_disk_new_folder = YandexDisk(UserData.token_ya_disk)
            ya_disk_new_folder.create_a_folder()
            for name_photo, url_photo in dict_url_and_name_photo.items():
                ya_disk_new_folder.upload_file_to_ya_disk(name_photo, url_photo)

        #return dict_url_and_name_photo

class UserData:
    id_vk = input('Введите, пожалуйста, номер страницы(id) на сайте https://vk.com/: ')
    token_ya_disk = input('Введите, пожалуйста, TOKEN c Полигона Яндекс.Диска: ')


if __name__ == '__main__':
    vk_client = VkUser('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008', '5.131')
    new_user_data = UserData
    vk_client.get_photos()