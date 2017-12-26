import glob

import piexif



def go():
    for file in sorted(glob.glob('*.jpg')):
        rotation = float('.'.join(file.split('_')[-1].split('.')[:-1]))
        if rotation < 0:
            rotation = 360 + rotation
        rotation = int(round(rotation * 100, 2))

        exif_data = {
            "GPS": {
                piexif.GPSIFD.GPSImgDirectionRef: 'M',
                piexif.GPSIFD.GPSImgDirection: (rotation, 100),
            }
        }

        tags = piexif.load(file)
        tags.update(exif_data)
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, file)


if __name__ == '__main__':
    go()
