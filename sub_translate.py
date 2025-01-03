
import sys

from googletrans import Translator

from sub_delay import read_srt, write_srt

# Create a Translator object
translator = Translator()

def translate_text(text, dest_language='en'):
    translation = translator.translate(text, dest=dest_language)
    return translation.text

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("USAGE python {sys.argv[0]} LANGUAGE in.srt out.srt")
        exit(1)

    destination_language = sys.argv[1]  # example: 'en'
    sublines = read_srt(sys.argv[2])

    print("translating text:", end="\n", flush=True)
    translines = []

    pos = 0
    for sl in sublines:
        sl['text'] = translate_text(sl['text'], destination_language)
        translines.append(sl)
        pos += 1
        progress = round(pos/len(sublines) * 100,1)

        print("\033[F\033[K", end="", flush=True)  # Move up and clear the line
        print(f"{progress} ")

    print("done.")

    write_srt(sys.argv[3], translines)
   
