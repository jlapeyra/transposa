from chord import Chord

class Song:
    sep = (' ', '\t', '\n', '\v', '\f', '\r',
            '/', '.', ',', ':', '(', ')', '[', ']', '{', '}',)
    WORDS = 0
    CHORD = 1

    def __init__(self, song:str):
        self.list = []
        ini_fragment_words = True
        i = 0
        while i<len(song):
            word = ''
            while i<len(song) and song[i] in self.sep:
                word += song[i]
                i += 1
            if ini_fragment_words: 
                ini_fragment_words = False
                self.list.append([word, Chord('')])
            else:
                self.list[-1][Song.WORDS] += word

            word = ''
            while i<len(song) and not song[i] in self.sep:
                word += song[i]
                i += 1
            chord = Chord(word)
            if chord.good_structure():
                ini_fragment_words = True
                self.list[-1][Song.CHORD] = chord
            else: 
                self.list[-1][Song.WORDS] += word


    def smart_alt(self, semitones):
        collisions = {
            '#' : {
                    'A' : {'nat':0, 'alt':0}, 
                    'B' : {'nat':0, 'alt':0}, 
                    'C' : {'nat':0, 'alt':0}, 
                    'D' : {'nat':0, 'alt':0}, 
                    'E' : {'nat':0, 'alt':0}, 
                    'F' : {'nat':0, 'alt':0}, 
                    'G' : {'nat':0, 'alt':0}, 
            },
            'b' : {
                    'A' : {'nat':0, 'alt':0}, 
                    'B' : {'nat':0, 'alt':0}, 
                    'C' : {'nat':0, 'alt':0}, 
                    'D' : {'nat':0, 'alt':0}, 
                    'E' : {'nat':0, 'alt':0}, 
                    'F' : {'nat':0, 'alt':0}, 
                    'G' : {'nat':0, 'alt':0}, 
            },
        }
        for words,chord in self.list:
            if chord.num != None:
                for alt in ('b', '#'):
                    chord_str = chord.plus(semitones, alt)
                    note = chord_str[0]
                    if len(chord_str) > 1 and chord_str[1] == alt:
                        alt_nat = 'alt'
                    else:
                        alt_nat = 'nat'
                    collisions[alt][note][alt_nat] += 1
        collisions
        count = {'b':0,'#':0} #count collisions
        for alt in ('b', '#'):
            for note in collisions[alt]:
                if collisions[alt][note]['alt'] and collisions[alt][note]['nat']:
                    count[alt] += collisions[alt][note]['alt'] + collisions[alt][note]['nat']
        if count['#'] < count['b']:
            return '#'
        else:
            return 'b'



    def plus(self, semitones, alt='smart'):
        if alt == 'smart':
            alt = self.smart_alt(semitones)
        return ''.join(
            words + chord.plus(semitones,alt) for words, chord in self.list
        )

    def __str__(self):
        return self.plus(semitones=0, alt='#')

if __name__ == '__main__':
    song_str = '''
[Verse 1] (slow)
 G
I don't want a lot for Christmas
G/B
   There's just one thing I need
C
   I don't care about the presents
Cm/Eb
   Underneath the Christmas tree
G/B                      B7
I just want you for my own
Em                       Cm/Eb
More than you could ever know
G/D                  E7
   Make my wish come true
Am7            Cm6/D
All I want for Christmas is...
      G  Em  C       D
You  (up tempo) yeah
    '''
    song = Song(song_str)
    song_plus = song.plus(-1, alt='smart')
    print(song_plus)


