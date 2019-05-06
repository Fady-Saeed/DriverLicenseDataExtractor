import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract
import base64
from split_and_get_no import split, arabic_to_english

DIGITS = "DIGITS"
DIGITS2 = "DIGITS2"
LETTERS = "LETTERS"

f = lambda text ,number : text if not number else number 
arabic_numbers = ['٠' ,'١' , '٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]

f = lambda text ,number : text if not number else number 
arabic_numbers = ['٠' ,'١' , '٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]

def check_plate_text_and_no(plate_text , plate_no) : 
    if ( not plate_text or not plate_no ) : 
        print('One is empty ....')
        plate = f(plate_text,plate_no)
        print(plate[0] , plate[5])
        plate = plate.replace(' ','')
        #no =   [x for x in plate if x in arabic_numbers]
        #text = [x for x in plate if not(x in arabic_numbers)]
        text = list(plate[0:3])
        no = plate[3:]
        if '٤' in text : 
            #print('Found')
            text[index('٤')]  = \
            'ع'
        return int(1),text,no
    else :
        plate_text = plate_text.replace(' ','')
        plate_no = plate_no.replace(' ','')
        plate_text = list(plate_text[0:3])
        plate_no   = plate_no[0:3]
        #print(plate_text)
        if '٤' in plate_text : 
            #print('Found')
            plate_text[plate_text.index('٤')]  = \
            'ع'
        return 2,plate_text,plate_no
        
        







def isValidPlateDigits(digits):
    result = ""
    arabic_numbers = ['٠' ,'١' , '٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]
    english_numbers=['0','1','2','3','4','5','6','7','8','9']
    for digit in digits:
        if (digit in arabic_numbers) or (digit in english_numbers):
            result = result + digit
    if len(result) != 3:
        return False, result
    return True, result

def isValidPlateLetters(letters, fixOCRSpaceDigitLetterConflict):
    result = ""
    arabic_alpha = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی','أ','ء','ئ']
    for letter in letters:
        if letter in arabic_alpha:
            result = result + letter
        elif letter == '٤' and fixOCRSpaceDigitLetterConflict:
            result = result + 'ع'
    if len(result) != 3:
        return False, result
    return True, result

def getCleanedData(proposals, type, fixOCRSpaceDigitLetterConflict):
    global LETTERS, DIGITS

    result = []
    for proposal in proposals:
        if type == LETTERS:
            isValid, cleaned = isValidPlateLetters(proposal, fixOCRSpaceDigitLetterConflict)
        elif type == DIGITS:
            isValid, cleaned = isValidPlateDigits(proposal)
        if isValid:
            result.append(cleaned)
        print("proposal : " + proposal + " isValid : " + str(isValid) + " cleaned : " + cleaned)
    return result

def ocrspace(image, type):
    global LETTERS, DIGITS

    _, image = cv2.imencode('.jpg', image)
    base64Image = base64.b64encode(image).decode()
    base64Image = 'data:image/jpg;base64,{}'.format(base64Image)
    # print("#########################################################################")
    # print("Image : ")
    # print(base64Image)
    # print("#########################################################################")
    payload = {'apikey': '310081fb4188957' ,
               'isOverlayRequired' : 'True' ,
               'language': 'ara' , 
               'detectOrientation' : 'True' , 
               'scale':'False',
               'base64Image': base64Image
              } 
    r = rqs.post('https://api.ocr.space/parse/image',
                    data=payload
                )
    d = r.json()
    result = d['ParsedResults'][0]['ParsedText']
    result = result.replace(" ", "")
    result = result.replace("\r", "")
    result = result.replace("\n", "")
    if type == DIGITS:
        result = result.replace('٤','')
        result = arabic_to_english(result)
    elif type == DIGITS2:
        result = result.replace('٤','ع')
        result = arabic_to_english(result)
    return result

def tesseract_ocr(image, type):
    global LETTERS, DIGITS, DIGITS2

    if type == LETTERS:
        result = pytesseract.image_to_string(image, lang='Arabic')
        result = result.replace(" ", "")
    elif type == DIGITS:
        result = pytesseract.image_to_string(image, lang='Arabic')
        result = arabic_to_english(result.replace(" ", ""))
    elif type == DIGITS2:
        result = pytesseract.image_to_string(image, lang='ara_number')
        result = arabic_to_english(result.replace(" ", ""))
    return result

def get_no_and_text(image) : 
    global LETTERS, DIGITS, DIGITS2

    numImg, lettersImg = split(image)

    pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'
    
    proposed_digits = [ocrspace(image, DIGITS), ocrspace(numImg, DIGITS), tesseract_ocr(image, DIGITS), tesseract_ocr(numImg, DIGITS), tesseract_ocr(image, DIGITS2), tesseract_ocr(numImg, DIGITS2)]
    proposed_letters = [ocrspace(image, LETTERS), ocrspace(lettersImg, LETTERS), tesseract_ocr(image, LETTERS), tesseract_ocr(lettersImg, LETTERS)]
    print("proposed_digits : ")
    print(proposed_digits)
    digits = getCleanedData(proposed_digits, DIGITS, False)
    letters = getCleanedData(proposed_letters, LETTERS, True)

    print("Letters : ")
    print(letters)
    print("Digits : ")
    print(digits)

    return list(set(letters)), list(set(digits))
