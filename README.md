# jplearner
 
Draw outline of where you want translations to occur. Then when u click the "Snap" button it auto converts
japanese kanji to kanji plus furigana superscripted. eg: \
![image](https://user-images.githubusercontent.com/7845409/202933194-460bee35-50ca-4151-b4d7-37c4ff9b7920.png)\
Also you can select from a slew of translators to use the Hover for translation now.
![jplpic](https://user-images.githubusercontent.com/7845409/203462643-2d2215e9-de3d-4e15-a382-8aec3ff49c33.PNG)

Made in a few days far from perfect.

TO DOs:
1. Tl box selection isn't perfectly accurate at times for some reason.
2. Can tesseract OCR accuracy be improved?
   1. Added a few lines (greyscale - black and white, resize). 
   2. Maybe threshold is useful as like a dial on the window? 
   3. Worked on this, done for now- added a preprocess step with a threshold that can be adjusted via settings.
3. Add Anki support..
4. Fix the flaws due to my few days old knowledge of pyqt and desktop guis. Plus other fixes to poor setup.
5. Furigana in images messes with OCR quite badly at times.. logic to remove furigana from img seems difficult. 
6. Main window janky when resized.
7. Show definitions for each mecab parsed 'word', Problem is to figure out how best to show this...
   1. now a part of view menu
8. Fix how Kanji dict displays kanji - definition.

## Install
Requirements.txt is there \
Download and install Dependencies \
run pip install for requirements  \
Give it a whirl!

##### Dependecies
furigana fork - https://github.com/itsupera/furigana \
tesseract:- https://github.com/tesseract-ocr/tesseract \
mecab:- https://pypi.org/project/mecabwrap/ \
Microsoft Visual :- https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170
