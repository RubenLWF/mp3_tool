from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1

audio = MP3('audio/' + input('Enter .mp3 file name: '), ID3=ID3)

audio.tags['TIT2'] = TIT2(encoding=3, text=[input('Enter the title: ')])
audio.tags['TPE1'] = TPE1(encoding=3, text=[input('Enter the artist: ')])
audio.tags.add(APIC(encoding=3, mime='image/png', type=3, data=open('img/' + input('Enter .png file name: '), 'rb').read()))

audio.save()
print('Metadata added succesfully!')