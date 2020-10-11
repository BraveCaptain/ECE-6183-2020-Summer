import speech_recognition as sr

class SpeechRecognition(object):
    r = sr.Recognizer()

    def __SphinxHandler(self, audio):
        try:
            print('Sphinx thinks you said: "' + self.r.recognize_sphinx(audio) + '"')
            return self.r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    def getStringFromMicrophone(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print("Please speak...")
            audio = self.r.listen(source)
            print("End of speech detected...")
            return self.__SphinxHandler(audio)
    
    def getStringFromFile(self, file):
        with sr.AudioFile(file) as source:
            audio = self.r.record(source)
            return self.__SphinxHandler(audio)

    def getStringFromBin(self, data, rate, width):
        audio = sr.AudioData(data, rate, width)
        return self.__SphinxHandler(audio)
            
