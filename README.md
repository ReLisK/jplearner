# jplearner
 
Draw outline of where you want translations to occur. Then when u click the "Snap" button it auto converts
japanese kanji to kanji plus furigana in brackets. eg: 
![img.png](img.png)
Also you can select from a slew of translators to use the Hover for translation now.

Made in 3 days far from perfect.

TO DOs:
1. Fix Draw button, so you can choose to redraw translate box. 
   1. Done
2. Tl box selection isn't perfectly accurate at times for some reason.
3. Radio Buttons actually do something lol. (japanese to eng using google translate/deepl or w.e )
   1. Changed to horizontal/vertical japanese
4. Add radio button for vertical japanese as that shouldnt be hard to add with tessaract.
   1. See above.
5. Can tesseract OCR accuracy be improved?
   1. Added a few lines (greyscale - black and white, resize). Doing some testing..
   2. Maybe threshold is useful as like a dial on the window? Maybe.
6. Maybe add Anki support..
7. Furigana in brackets ain't so visually pleasing should find better way maybe hover but PYQT is a lil tough for that..
   1. Fixed furigana now in web engine superscripted
8. Fix the many flaws due to my 3 days old knowledge of pyqt and desktop guis. Plus other fixes to poor setup.
9. Furigana in images messes with OCR quite badly at times.. logic to remove furigan from img seems difficult. 
10. Main window janky when resized.

## Install
Requirements.txt is there
Download and install Dependencies
run pip install for requirements 
Give it a whirl!

##### Dependecies

tesseract:- https://github.com/tesseract-ocr/tesseract \
mecab:- https://pypi.org/project/mecabwrap/ \
Microsoft Visual :- https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170