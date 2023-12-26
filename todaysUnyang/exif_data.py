from datetime import datetime
from todaysUnyang import env

COORDINATE= {
    1: b"N",
    2: ((37, 1), (38, 1), (41343360, 1000000)),
    3: b"E",
    4: ((126, 1), (41, 1), (21517080, 1000000)),
    5: 0,
    6: (42, 1),
}

IMAGE_DESCRIPTION = env.special_message

def encoder(string):
    return string.encode('utf-8')

def timeNow():
    return encoder(str(datetime.now().strftime('%Y:%m:%d %H:%M:%S')))

exif_data_changed = {
    "0th": {
        # ImageWidth
        256: 1000,
        # ImageLength
        257: 3000,
        # Make
        271: encoder('2023 UYHS Algorithm'),
        # Model
        272: encoder("'unyang4cut'"),
        # ImageDescription
        270: encoder(IMAGE_DESCRIPTION),
        # Artist
        315: encoder("김도현"),
        # Orientation
        274: 1,
        # Software
        305: encoder("2023 운양고등학교 알고리즘 동아리"),
        # DateTime
        306: timeNow(),
        # GPSTag
        34853: 732,
    },
    "Exif": {
        36864: b"0220",
        36867: timeNow(),
        36868: timeNow(),
    },
    "GPS": COORDINATE,
    "Interop": {},
}