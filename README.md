# jplearner
 
Draw outline of where you want translations to occur. Then when u click the "Snap" button it auto converts
japanese kanji to kanji plus furigana superscripted. eg: \
![image](https://user-images.githubusercontent.com/7845409/202933194-460bee35-50ca-4151-b4d7-37c4ff9b7920.png)\
Also you can select from a slew of translators to use the Hover for translation now.
![image](https://user-images.githubusercontent.com/7845409/219905005-1e664ae7-6160-47b4-85ee-50927081ecc4.png)

This is what it looks like with kanjidict enabled using googleocr and hovering for translation:
![image](https://user-images.githubusercontent.com/7845409/219905160-c739e96e-93b9-4f4c-b642-355ded517718.png)


Made in a few days far from perfect.

TO DOs:
1. Tl box selection isn't perfectly accurate at times for some reason.
2. Some Kanji have multiple readings and the wrong reading is sometimes selected.
3. Can tesseract OCR accuracy be improved?
   1. Added a few lines (greyscale - black and white, resize). 
   2. Maybe threshold is useful as like a dial on the window? 
   3. Worked on this, done for now- added a preprocess step with a threshold that can be adjusted via settings.
4. Add Anki support..
5. Fix the general flaws due to not the best setup. eg. The current code flow is definitley not straightforward.
6. Furigana in images messes with OCR quite badly at times.. logic to remove furigana from img seems difficult. 
7. Main window janky when resized.


## Install Instructions
Install tesseract, mecab and microsoft visual; links below.
Use Requirements.txt to pip install necessary pacakges. \
Give it a whirl!

##### Dependecies
tesseract:- https://github.com/tesseract-ocr/tesseract \
mecab:- https://pypi.org/project/mecabwrap/ \
Microsoft Visual :- https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170
