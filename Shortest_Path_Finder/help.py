from flask import*
import pyttsx3 as pyttsx
from playsound import playsound
from funny_morse import*
import time

app=Flask(__name__)

#file names for text and mp3 and wav....
import string
import random
filename1 = ''.join(random.choices(string.ascii_uppercase+string.digits,k=8))+"_cipher"
filename2 = ''.join(random.choices(string.ascii_uppercase+string.digits,k=8))+"_decipher"
#routings......

@app.route('/')
def main():
    return render_template("index.html")#main page or index

@app.route('/home', methods=['GET'])
def home():
    return render_template("index.html")#index 
    
@app.route('/encryption', methods=['GET'])
def encryption():
   return render_template("encryption.html")#encryption page

@app.route('/decryption', methods=['GET'])
def decryption():
   return render_template("decryption.html")#decryption page

@app.route('/moreabout',methods=['GET'])
def moreabout():
    return render_template("moredetails.html")#more details about morsecode page


@app.route('/downloaddecryption', methods=['GET','POST'])
def downloaddecryption():
    return render_template("downloaddecryption.html")# encrypted text and wav files download page


@app.route('/downloadencryption',methods=['GET','POST'])
def downloadencryption():
    return render_template("downloadencryption.html") #decrypted text and mp3 files download page

# -------------------------------------------------------------------------
#morse code dictionary

MORSE_CODEALPHABET_DICTIONARY = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.','O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-', 'W':'.--','X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--','4':'....-', '5':'.....', '6':'-....','7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ',':'--..--', '.':'.-.-.-','?':'..--..', '/':'-..-.', '-':'-....-','(':'-.--.', ')':'-.--.-',' ':' '
                    }
 

 

 #Encryption Process....

def text_to_morse_code(input_text): #text to morse code  generator
    final_text=str(input_text)
    final_morse_code=code(final_text)
    return final_morse_code

def text_to_morse_code_sound(input_text_sound): # text  to morse code along with background sound  of morse code dit and dah
     input_text_sound_final = str(input_text_sound)
     morse_code = [MORSE_CODEALPHABET_DICTIONARY[i.upper()] + ' ' for i in input_text_sound_final if i.upper() in MORSE_CODEALPHABET_DICTIONARY.keys()]
     final_morse_code=''.join(morse_code)
     for symbol in final_morse_code:
        if symbol=='.':
            playsound('dit.wav')
            time.sleep(0.5)
        elif symbol=='-':
            playsound('dah.wav')
            time.sleep(0.5)
        else:
            time.sleep(0.5)
     return final_morse_code

def download_morsecode_sound_file(a):  #morse code sound wav file generation
    name=filename1+".wav"
    audio_file(name, a, sps=44100, freq=800)


@app.route('/downloadmorsesoundfile',methods=['GET','POST']) #morce code sound wav file downloader
def downloadmorsesoundfile():
    name=filename1+".wav"
    return send_file(name,as_attachment=True,cache_timeout=0)

def textfileofmorsecode(input_engl_text):
    final_engl_text = str(input_engl_text)
    code = [MORSE_CODEALPHABET_DICTIONARY[i.upper()] + ' ' for i in final_engl_text if i.upper() in MORSE_CODEALPHABET_DICTIONARY.keys()]
    morse_code_final=''.join(code)
    B=str(morse_code_final)
    final=final_engl_text+":"+B
    file1 = open(filename1+".txt","w")
    file1.write(final)
    file1.close()

@app.route('/downloadmorsecodetextfile',methods=['GET','POST'])
def downloadmorsecodetextfile():
    name=filename1+".txt"
    return send_file(name,as_attachment=True,cache_timeout=0)




# decryption Processs....


def morse_code_to_text(input_morse_code): #morse code  to english text
    final_input_morse_code=str(input_morse_code)
    english_text = [k for i in final_input_morse_code.split() for k,v in MORSE_CODEALPHABET_DICTIONARY.items() if i==v]
    final_english_text = ''.join(english_text)
    return final_english_text

def text_sound_english(input_morse_code_sound): #morse code to english with background sound 
    final_input_morse_code_sound = str(input_morse_code_sound).strip()
    engl_text = [k for i in final_input_morse_code_sound.split() for k,v in MORSE_CODEALPHABET_DICTIONARY.items() if i==v]
    final_english_text_with_sound = ''.join(engl_text)
    engine = pyttsx.init("sapi5")
    engine.say(final_english_text_with_sound.strip())
    engine.runAndWait()
    return final_english_text_with_sound.strip()



def downloadenglishsound(input_morse_code_sound): # morse code to english speech generation 
    final_input_morse_code_sound = str(input_morse_code_sound).strip()
    engl_text = [k for i in final_input_morse_code_sound.split() for k,v in MORSE_CODEALPHABET_DICTIONARY.items() if i==v]
    final_english_text_with_sound = ''.join(engl_text)
    engine = pyttsx.init()
    engine.save_to_file(final_english_text_with_sound, filename2+'.mp3')
    engine.runAndWait()
    return final_english_text_with_sound

@app.route('/downloadenglishaudio',methods=['GET','POST']) #english speech downloader
def downloadenglishaudio():
    name=filename2+".mp3"
    return send_file(name, as_attachment=True,cache_timeout=0)

    
def downloadenglishttextfile(input_morse_code_text):  #morse code to english text file generation
    final_input_morse_code_text= str(input_morse_code_text).strip()
    code = [k for i in final_input_morse_code_text.split() for k,v in MORSE_CODEALPHABET_DICTIONARY.items() if i==v]
    new_input_morse_code_text = ''.join(code)
    B=str(new_input_morse_code_text)
    final=final_input_morse_code_text+":"+B
    file1 = open(filename2+".txt","w")
    file1.write(final)
    file1.close()

@app.route('/downloadenglishtext',methods=['GET','POST']) #morse code to english text file downloader
def downloadenglishtext():
    name=filename2+".txt"
    return send_file(name, as_attachment=True,cache_timeout=0)


#Paths and Functions....    

# ---------------------------------------------------------------------
@app.route('/encryption/',methods=['GET','POST'])
def calencry():
    if request.method=='POST':
        inp_from_form=request.form['input-text-eng']
        final_inp_from_form=str(inp_from_form)

        if request.form['button_final']=='encrypt-without-audio':
            encryptor=text_to_morse_code(final_inp_from_form)
            return render_template("encryption.html",abc=encryptor,input=final_inp_from_form)
            
        elif request.form['button_final']=='audio':
            encryptor=text_to_morse_code(final_inp_from_form)
            encryptor_sound=text_to_morse_code_sound(final_inp_from_form)
            return render_template("encryption.html",abc=encryptor,input=final_inp_from_form)

        elif request.form['button_final']=='download_morsecode':
            encryptor=text_to_morse_code(final_inp_from_form)
            textfileofmorsecode(final_inp_from_form)
            download_morsecode_sound_file(final_inp_from_form)
            return redirect(url_for("downloadencryption"))
        else:
            return render_template("index.html")

    else:
        return render_template("index.html")



@app.route('/decryption/',methods=['GET','POST'])
def decrypt():
    if request.method=='POST':
        input_morse_code=request.form.get('input-morse-code')
        final_input_morse_code=str(input_morse_code)
        if request.form.get('button')=='decode':
            decoder=morse_code_to_text(final_input_morse_code)
            return render_template("decryption.html",xyz=decoder,input=final_input_morse_code)

        elif request.form.get('button')=='sound':
            decoder=morse_code_to_text(final_input_morse_code)
            decoder_sound=text_sound_english(final_input_morse_code)
            return render_template("decryption.html",xyz=decoder,input=final_input_morse_code)

        elif request.form.get('button')=='downloadsound':
            decoder=morse_code_to_text(final_input_morse_code)
            downloadenglishsound(final_input_morse_code)
            downloadenglishttextfile(final_input_morse_code)
            return redirect(url_for("downloaddecryption"))
        else:
            return render_template("index.html")     
    else:
        return render_template("index.html")

@app.route("/facebook")
def facebook():
    return redirect("http://www.facebook.com")
@app.route("/twitter")
def twitter():
    return redirect("https://www.twitter.com")
@app.route("/youtube")
def youtube():
    return redirect("https://www.youtube.com")
@app.route("/instagram")
def instagram():
    return redirect("https://www.instagram.com")







if __name__ == '__main__':
  app.run(debug = True)