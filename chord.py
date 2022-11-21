class Chord:
    note2num = {
        'C' : 0,
        'D' : 2,
        'E' : 4,
        'F' : 5,
        'G' : 7,
        'A' : 9,
        'B' : 11
    }
    MAX_NUM = 12
    num2note = {
        '#' : ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'],
        'b' : ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    }

    def __init__(self, text:str):
        if text == '' or not text[0] in Chord.note2num: 
            self.num = None
            self.suffix = text
        else:
            self.num = Chord.note2num[text[0]]
            if (len(text) > 1 and text[1] in ('b', '#')):
                if text[1] == 'b':
                    self.num = (self.num - 1)%Chord.MAX_NUM
                elif text[1] == '#':
                    self.num = (self.num + 1)%Chord.MAX_NUM
                self.suffix = text[2:]
            else:
                self.suffix = text[1:]

    def plus(self, semitones, alt='#'):
        return (
            Chord.num2note[alt][(self.num + semitones)%Chord.MAX_NUM] \
            if self.num != None else ''
        ) + self.suffix

    def __str__(self) -> str:
        return self.plus(0)

    def __repr__(self) -> str:
        return f'Chord({self.__str__()})'

    def good_structure(self):
        return self.num != None and Chord.is_good_suffix(self.suffix)

    def is_good_suffix(suffix:str):
        starts = True
        while suffix and starts:
            for part in Chord.suffix_parts:
                starts = suffix.startswith(part)
                if starts:
                    suffix = suffix[len(part):]
                    break
        return suffix == ''

    suffix_parts = ['b', '#', 'sus', 'add', 'aug', 'dim', 'maj', 'm',
                    '1','2','3','4','5','6','7','8','9','0',
                    '(', ')', '+', '-', 'M', 's4', 's2',
                    'ø', '°', '△']


if __name__ == '__main__':
    song = ''
    words = []
    chords = []
    for string in song.split():
        if Chord(string).good_structure():
            chords.append(Chord(string).plus(0))
        else:
            words.append(string)
    print(', '.join(chords))
    print(' '.join(words))
