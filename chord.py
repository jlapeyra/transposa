class ChordException(Exception):
    pass

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
        self.num = []
        self.suffix = []
        for text_i in text.split('/'):
            if text_i:
                self.__init_i(text_i)
        self.n_slashes = len(self.num)

    def __init_i(self, text:str):
        if not text[0] in Chord.note2num: 
            raise ChordException(f'Note {text[0]} does not exist')
        num = Chord.note2num[text[0]]
        if (len(text) > 1 and text[1] in ('b', '#')):
            if text[1] == 'b':
                num = (num - 1)%Chord.MAX_NUM
            elif text[1] == '#':
                num = (num + 1)%Chord.MAX_NUM
            suffix = text[2:]
        else:
            suffix = text[1:]
        self.num.append(num)
        self.suffix.append(suffix)

    def plus(self, semitones, alt='#'):
        return '/'.join(
            Chord.num2note[alt][(self.num[i] + semitones)%Chord.MAX_NUM] + self.suffix[i] \
            for i in range(self.n_slashes)
        )
