digit_map:dict[str, str] = {
      '0':'ສູນ','1':'ຫນຶ່ງ', '2':'ສອງ', '3': 'ສາມ', '4': 'ສີ່',
      '5': 'ຫ້າ', '6': 'ຫົກ', '7': 'ເຈັດ', '8': 'ແປດ', '9': 'ເກົ້າ'
}

digit_map_no_zero = { k:v for k,v in digit_map.items() if k != '0'}

def lao_number_sounds(text:str, number_sound:str='') -> str:
   print(len(text))

   # At the first recursion, this number_sound_copy is empty
   number_sound_copy = number_sound
   
   # Process at each digit from high to low:

   if len(text) > 11 or len(text) == 1:
      for number in text:
         number = digit_map[number]
         number_sound_copy += number

      return number_sound_copy 
   
   if len(text) == 11:
      if text[0] == '0':
         number_sound_copy = number_sound_copy 
      elif text[0] == '1':
         number_sound_copy += 'ສີບ'
      elif text[0] == '2':
         number_sound_copy += 'ຊາວ'
      else:
         number_sound_copy += digit_map[text[0]] + 'ສິບ' 
      
   
   if len(text) == 10:
      if text[0] == '0':
         number_sound_copy = number_sound_copy + 'ຕື້'
      if text[0] == '1':
         number_sound_copy = number_sound_copy + 'ເອັດຕື້'
      else:
         number_sound_copy += digit_map[text[0]] + 'ຕື້'
   
   if len(text) == 9:
      if text[0] == '0':
         number_sound_copy = number_sound_copy
      else:
         number_sound_copy += digit_map[text[0]] + 'ຮ້ອຍ'
   
   if len(text) == 8:
      if text[0] == '0':
         number_sound_copy = number_sound_copy + 'ລ້ານ'
      elif text[0] == '1':
         number_sound_copy += 'ສີບ'
      elif text[0] == '2':
         number_sound_copy += 'ຊາວ'
      else:
         number_sound_copy += digit_map[text[0]] + 'ສິບ'
   
   if len(text) == 7:
      if text[0] == '0':
         number_sound_copy = number_sound_copy + 'ລ້ານ'
      if text[0] == '1':
         number_sound_copy += 'ເອັດລ້ານ'
      else:
         number_sound_copy += digit_map[text[0]] + 'ລ້ານ' 
   
   if len(text) == 6: 
      if text[0] == '0':
         number_sound_copy = number_sound_copy
      else:
         number_sound_copy += digit_map[text[0]] + 'ແສນ'
         
   if len(text) == 5:
      if text[0] == '0':
         number_sound_copy = number_sound_copy
      else:
         number_sound_copy += digit_map[text[0]] + 'ຫມື່ນ'
         
   
   if len(text) == 4:
      if text[0] == '0':
         number_sound_copy = number_sound_copy
      else:
         number_sound_copy += digit_map[text[0]] + 'ພັນ'
         
   
   if len(text) == 3:
      if text[0] == '0':
         number_sound_copy = number_sound_copy
      else:
         number_sound_copy += digit_map[text[0]] + 'ຮ້ອຍ'
      
   if len(text) == 2:  
      if text[0] == '0':
         number_sound_copy = number_sound_copy       
      elif text[0] == '1': 
         number_sound_copy += 'ສິບ'
      elif text[0] == '2':
         number_sound_copy += 'ຊາວ'
      else:
         number_sound_copy += digit_map[text[0]] + 'ສິບ'
         
      if text[1] == '1':
         number_sound_copy += 'ເອັດ'
         return number_sound_copy
      elif text[1] != '0':
         number = digit_map_no_zero[text[1]]
         return number_sound_copy + number
      elif text[1] == '0':
         return number_sound_copy

   return lao_number_sounds(text[1:], number_sound_copy)


def extract_numbers(text:str)->list[str]:
   current_number:str = ''
   extracted_numbers:list[str] = []
   
   
   # Extract numbers from input text
   for char in text:
      if char.isdigit():
         current_number += char
      elif not char.isdigit() and current_number != "":
         extracted_numbers.append(current_number)
         current_number = ''

   if current_number != '':
      extracted_numbers.append(current_number)
      current_number = ''
   
   return extracted_numbers


def preprocess_numbers(text:str) -> str:
   '''
      Replace all the numbers with text-numbers
   '''
   extracted_numbers = extract_numbers(text)
   
   for number in extracted_numbers:
      text = text.replace(number, lao_number_sounds(number))
   
   return text
         