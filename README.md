# jplearner
 
Draw outline of where you want translations to occur. Then when u click the "Snap" button it auto converts
japanese kanji to kanji plus furigana superscripted. eg: \
![image](https://user-images.githubusercontent.com/7845409/202933194-460bee35-50ca-4151-b4d7-37c4ff9b7920.png)

Made in a few days far from perfect.

TO DOs:
1. Fix Draw button, so you can choose to redraw translate box. 
   1. Done
2. Tl box selection isn't perfectly accurate at times for some reason.
3. Radio Buttons actually do something lol. (japanese to eng using google translate/deepl or w.e )
   1. Changed to horizontal/vertical japanese
4. Add radio button for vertical japanese as that shouldnt be hard to add with tessaract.
   1. See above.
5. Can tesseract OCR accuracy be improved?
6. Maybe add Anki support..
7. Furigana in brackets ain't so visually pleasing should find better way maybe hover but PYQT is a lil tough for that..
   1. Fixed furigana now in web engine superscripted
8. Fix the many flaws due to my 3 days old knowledge of pyqt and desktop guis. Plus other fixes to poor setup.

## Install
Requirements.txt is there

##### Dependecies
furigana fork - https://github.com/itsupera/furigana \
tesseract:- https://github.com/tesseract-ocr/tesseract \
mecab:- https://pypi.org/project/mecabwrap/ \
Microsoft Visual :- https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170
