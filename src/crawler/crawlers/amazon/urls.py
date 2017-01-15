# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urls = {}
urls['美国'] = [
    'https://www.amazon.com/Insta360-Nano-degree-Camera-iPhone/dp/B01FY8CHIA/ref=sr_1_1?ie=UTF8&qid=1482248463&sr=8-1&keywords=insta360',
    'https://www.amazon.com/Insta360-Degree-Panorama-Camera-Fisheye/dp/B01M0E8EKR/ref=sr_1_4?ie=UTF8&qid=1482248463&sr=8-4&keywords=insta360',
    'https://www.amazon.com/dp/B01NCLPZY0/ref=sr_1_12?ie=UTF8&qid=1482248463&sr=8-12&keywords=insta360',
    'https://www.amazon.com/Insta360-Panoramic-Degree-Fisheye-Camera/dp/B01MG82FNW/ref=sr_1_15?ie=UTF8&qid=1482248463&sr=8-15&keywords=insta360',
    'https://www.amazon.com/Insta360-Panorama-Fisheye-Headset-Glasses/dp/B01KH3VEO0/ref=sr_1_20?ie=UTF8&qid=1482248730&sr=8-20&keywords=insta360',
    'https://www.amazon.com/Morjava-Insta360-Nano-Panoramic-Portable/dp/B01M0MDFS4/ref=sr_1_22?ie=UTF8&qid=1482248650&sr=8-22&keywords=insta360',
    'https://www.amazon.com/panoramic-Digital-virtual-Insta360-nano/dp/B01JGPIP7E/ref=sr_1_27?ie=UTF8&qid=1482248650&sr=8-27&keywords=insta360',
    'https://www.amazon.com/dp/B01N5GW0K4/ref=sr_1_39?ie=UTF8&qid=1482248790&sr=8-39&keywords=insta360'
]

urls['加拿大'] = [
    'https://www.amazon.ca/Insta360-Nano-Degree-Camera-iPhone/dp/B01FY8CHIA/ref=sr_1_1?ie=UTF8&qid=1482248783&sr=8-1&keywords=insta360',
	'https://www.amazon.ca/Insta360-Degree-Panorama-Camera-Fisheye/dp/B01M0E8EKR/ref=sr_1_9?ie=UTF8&qid=1482248783&sr=8-9&keywords=insta360'
]

urls['墨西哥'] = [
    'https://www.amazon.com.mx/insta360-Nano-c%C3%A1mara-v%C3%ADdeo-360-grados-iPhone/dp/B01FY8CHIA/ref=sr_1_1?ie=UTF8&qid=1482248935&sr=8-1&keywords=insta360',
    'https://www.amazon.com.mx/Insta360-Camera-iPhone-Pearl-White/dp/B01IWZKLUI/ref=sr_1_2?ie=UTF8&qid=1482248935&sr=8-2&keywords=insta360',
    'https://www.amazon.com.mx/Insta360-C%C3%A1mara-iPhone-color-Plata/dp/B01KO250O4/ref=sr_1_3?ie=UTF8&qid=1482248935&sr=8-3&keywords=insta360',
    'https://www.amazon.com.mx/Boblov-Insta360-panorama-Objetivo-Auricular/dp/B01KH3VEO0/ref=sr_1_6?ie=UTF8&qid=1482248935&sr=8-6&keywords=insta360'
]

urls['英国'] = [
    'https://www.amazon.co.uk/Insta360-Compact-Panoramic-3K-HD/dp/B01HNIF9PW/ref=sr_1_1?ie=UTF8&qid=1482249079&sr=8-1&keywords=insta360',
    'https://www.amazon.co.uk/INSTA360-Nano-hardwrk-360-Degree-iPhone-Full-HD-apple/dp/B01M09S1AS/ref=sr_1_5?ie=UTF8&qid=1482249079&sr=8-5&keywords=insta360',
    'https://www.amazon.co.uk/Morjava-Insta360-Nano-Panoramic-2K/dp/B01M0MDFS4/ref=sr_1_8?ie=UTF8&qid=1482249079&sr=8-8&keywords=insta360'
]

urls['德国'] = [
    'https://www.amazon.de/Insta360-Nano-hardwrk-Kamera-zertifiziert/dp/B01M09S1AS/ref=sr_1_1?ie=UTF8&qid=1482249287&sr=8-1&keywords=insta360',
    'https://www.amazon.de/Insta360-Nano-Compact-Panoramic-HD-210-Degree/dp/B01HNIF9PW/ref=sr_1_2?ie=UTF8&qid=1482249287&sr=8-2&keywords=insta360',
    'https://www.amazon.de/Insta360-Aluminiumlegierung-Panoramakameramontageunterseiten-Halterung-Stativgewinde/dp/B01L8GZSF6/ref=sr_1_3?ie=UTF8&qid=1482249287&sr=8-3&keywords=insta360',
    'https://www.amazon.de/insta360-Kamera-360-800-mAh-iPhone-6-PLUS/dp/B01KO250O4/ref=sr_1_5?ie=UTF8&qid=1482249287&sr=8-5&keywords=insta360',
    'https://www.amazon.de/dp/0284881368/ref=sr_1_11?ie=UTF8&qid=1482249287&sr=8-11&keywords=insta360'
]

urls['西班牙'] = [
    'https://www.amazon.es/Andoer-Insta360-Panor%C3%A1mica-3K-HD/dp/B01HNIF9PW/ref=sr_1_1?ie=UTF8&qid=1482249522&sr=8-1&keywords=insta360',
    'https://www.amazon.es/Insta360-NANO-Videoc%C3%A1mara-Tarjeta-Memoria/dp/B01KO250O4/ref=sr_1_2?ie=UTF8&qid=1482249522&sr=8-2&keywords=insta360',
    'https://www.amazon.es/Andoer-Insta360-Compacto-Panor%C3%A1mica-Dispositivo/dp/B01J9YPWIW/ref=sr_1_3?ie=UTF8&qid=1482249522&sr=8-3&keywords=insta360',
    'https://www.amazon.es/dp/0284881368/ref=sr_1_7?ie=UTF8&qid=1482249522&sr=8-7&keywords=insta360',
]

urls['法国'] = [
    'https://www.amazon.fr/Insta360-Nano-panoramique-3K-HD/dp/B01HNIF9PW/ref=sr_1_1?ie=UTF8&qid=1482249606&sr=8-1&keywords=insta360',
    'https://www.amazon.fr/insta360-Nano-Appareil-360-iPhone-FULL-HD-Apple/dp/B01M09S1AS/ref=sr_1_2?ie=UTF8&qid=1482249606&sr=8-2&keywords=insta360',
    'https://www.amazon.fr/Imaxs-INSTA360-Cam%C3%A9ra-360-iPhone/dp/B01KO250O4/ref=sr_1_3?ie=UTF8&qid=1482249606&sr=8-3&keywords=insta360',
    'https://www.amazon.fr/Insta360-Nano-Cam%C3%A9ra-360-iPhone/dp/B01FY8CHIA/ref=sr_1_4?ie=UTF8&qid=1482249606&sr=8-4&keywords=insta360',
    'https://www.amazon.fr/Andoer-Insta360-daluminium-panoramique-Titulaire/dp/B01LZ1I4E5/ref=sr_1_5?ie=UTF8&qid=1482249606&sr=8-5&keywords=insta360',
    'https://www.amazon.fr/dp/0284881368/ref=sr_1_6?ie=UTF8&qid=1482249606&sr=8-6&keywords=insta360'
]

urls['意大利'] = [
    'https://www.amazon.it/Insta360-3K-HD-Panoramica-Grandangolare/dp/B01HNIF9PW/ref=sr_1_1?ie=UTF8&qid=1482249699&sr=8-1&keywords=insta360',
    'https://www.amazon.it/insta360-Fotocamera-360-800-mAh-iPhone-6-Plus/dp/B01KO250O4/ref=sr_1_2?ie=UTF8&qid=1482249699&sr=8-2&keywords=insta360',
    'https://www.amazon.it/Insta360-Panoramic-Degree-Fisheye-Camera/dp/0284881368/ref=sr_1_6?ie=UTF8&qid=1482249699&sr=8-6&keywords=insta360',
    'https://www.amazon.it/nextradeitalia-Spherical-camera-INSTA360-NANO/dp/B01NAFWMV1/ref=sr_1_7?ie=UTF8&qid=1482249699&sr=8-7&keywords=insta360'
]

urls['日本'] = [
    'https://www.amazon.co.jp/INSTA360-360%C2%B0%E5%85%A8%E5%A4%A9%E7%90%83%E3%83%91%E3%83%8E%E3%83%A9%E3%83%9E%E5%BC%8F%E3%82%AB%E3%83%A1%E3%83%A9-3040x1520%E9%AB%98%E8%A7%A3%E5%83%8F%E5%BA%A6-%E3%83%87%E3%82%B8%E3%82%BF%E3%83%AB%E3%82%AB%E3%83%A1%E3%83%A9-%E4%BA%8C%E3%81%A4%E3%81%AE%E8%B6%85%E5%BA%83%E8%A7%92%E9%AD%9A%E7%9C%BC%E3%83%AC%E3%83%B3%E3%82%BA/dp/B01HNM4UTE/ref=sr_1_1?ie=UTF8&qid=1482249820&sr=8-1&keywords=insta360',
    'https://www.amazon.co.jp/%E3%82%B5%E3%83%B3%E3%82%B3%E3%83%BC-VRCAMDEG-Insta360-Nano-VRCAMDEG-%E3%80%90iPhone7-Plus%E5%AF%BE%E5%BF%9C%EF%BC%81%E3%80%91-%E2%80%BB%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E4%BB%98%E3%81%8D-%E3%82%B5%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%AC%E3%82%A2%E3%83%A2%E3%83%8E%E3%82%B7%E3%83%A7%E3%83%83%E3%83%97/dp/B01J0QUH0C/ref=sr_1_2?ie=UTF8&qid=1482249820&sr=8-2&keywords=insta360',
    'https://www.amazon.co.jp/Insta360-INSTA-NANO-Nano-360%C2%B0%E5%85%A8%E5%A4%A9%E7%90%83%E3%82%AB%E3%83%A1%E3%83%A9/dp/B01JPH1C82/ref=sr_1_4?ie=UTF8&qid=1482249820&sr=8-4&keywords=insta360',
    'https://www.amazon.co.jp/%EF%BC%91%E5%B9%B4%E4%BF%9D%E8%A8%BC-Insta360-%E5%85%A8%E5%A4%A9%E7%90%83%E3%83%91%E3%83%8E%E3%83%A9%E3%83%9E%E5%BC%8F%E3%82%AB%E3%83%A1%E3%83%A9-%E8%A7%A3%E5%83%8F%E5%BA%A63K-%E6%97%A5%E6%9C%AC%E8%AA%9E%E8%AA%AC%E6%98%8E%E6%9B%B8%E4%BB%98%E3%81%8D/dp/B01KUHKYZS/ref=sr_1_5?ie=UTF8&qid=1482249820&sr=8-5&keywords=insta360',
    'https://www.amazon.co.jp/Insta360-Camera-iPhone-Pearl-White/dp/B01KDNZNS2/ref=sr_1_10?ie=UTF8&qid=1482249820&sr=8-10&keywords=insta360',
    'https://www.amazon.co.jp/Insta360-Nano-360-%E5%85%A8%E5%A4%A9%E7%90%83%E3%83%91%E3%83%8E%E3%83%A9%E3%83%9E%E5%BC%8F%E3%82%AB%E3%83%A1%E3%83%A9-3040x1520%E9%AB%98%E8%A7%A3%E5%83%8F%E5%BA%A6-%E4%BA%8C%E3%81%A4%E3%81%AE%E8%B6%85%E5%BA%83%E8%A7%92%E9%AD%9A%E7%9C%BC%E3%83%AC%E3%83%B3%E3%82%BA/dp/B01MYN2UZQ/ref=sr_1_12?ie=UTF8&qid=1482249820&sr=8-12&keywords=insta360'
]

urls['印度'] = [
    'http://www.amazon.in/Insta360-Nano-degree-Camera-iPhone/dp/B01FY8CHIA/ref=sr_1_1?ie=UTF8&qid=1482249856&sr=8-1&keywords=insta360',
    'http://www.amazon.in/dp/B01N7DXQ34/ref=sr_1_5?ie=UTF8&qid=1482249856&sr=8-5&keywords=insta360'
]

first = {}
first['美国'] = 'the first to review this item'
first['加拿大'] = 'the first to review this item'
first['墨西哥'] = 'el primero en calificar este producto'
first['英国'] = 'the first to review this item'
first['德国'] = 'die erste Bewertung für diesen Artikel ab'
first['西班牙'] = 'el primero en opinar sobre este producto'
first['法国'] = 'la première personne à écrire un commentaire sur cet article'
first['意大利'] = 'per primo questo articolo'
first['日本'] = 'カスタマーレビューを書きませんか'
first['印度'] = 'the first to review this item'

review = {}
review['美国'] = ' customer reviews</span>'
review['加拿大'] = ' customer reviews</span>'
review['墨西哥'] = ' opinión de cliente</span>'
review['英国'] = ' customer reviews</a>'
review['德国'] = ' Kundenrezensionen</'
review['西班牙'] = ' opiniones de clientes</span>'
review['法国'] = ' commentaires client</span>'
review['意大利'] = ' recensioni clienti</span>'
review['日本'] = '件のカスタマーレビュー</span>'
review['印度'] = ' customer reviews</span>'
