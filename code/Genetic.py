#!/usr/bin/env python
# coding: utf-8

# Genetic Assignment
# 
# Ali Pakdel Samadi
# 
# 810198368

# In[4]:


import string
import random
import time


# In[5]:


class Decoder:

    def __init__(self, _global_text, _encoded_text, keyLength):
        self.global_text = _global_text
        self.encoded_text = _encoded_text
        self.key_length = keyLength
        self.answer_length = 0
        self.words = set()
        self.random_keys = []
        self.decoded_text = ""
    
    def clean_global_text(self):
        word = ""
        for char in self.global_text:
            if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <=122):
                word += char.upper()
            else:
                if word != '':
                    self.words.add(word)
                word = ""
                
    def clean_encoded_text(self):
        word = ""
        text = []
        for char in self.encoded_text:
            if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <=122):
                word += char.upper()
            else:
                if word != '':
                    text.append(word)
                word = ""
        self.answer_length = len(text)
                     
    def generate_random_keys(self, length):
        for i in range(100):
            result = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) 
            self.random_keys.append([result, 0])
            
    def get_rank(self, key, print_flag):
        key_index = 0
        temp_word = ""
        temp_text = []
        decoded_text = ""

        for char in self.encoded_text:
            lower_flag = 0
            new_char = 0
            
            if char == '\n' or char == ' ':
                decoded_text += char
                if temp_word != "":
                    temp_text.append(temp_word)
                temp_word = ""
                
            elif (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <=122):
                new_char = ord(key[key_index])
                if ord(char) >= 97 and ord(char) <= 122:
                    lower_flag = 1
                    char = chr(ord(char) - 32)
                decoded_char = (ord(char) - new_char) + 91
                if decoded_char > 90:
                    decoded_char -= 26
                if lower_flag == 1:
                    decoded_text += chr(decoded_char + 32)
                else:
                    decoded_text += chr(decoded_char)
                    
                temp_word += chr(decoded_char)
                key_index += 1
                if key_index == self.key_length:
                    key_index = 0
            else:
                decoded_text += char
                if temp_word != "":
                    temp_text.append(temp_word)
                temp_word = ""
        
        count = 0
        for w in temp_text:
            if w in self.words:
                count += 1
        
        if print_flag:
            self.decoded_text = decoded_text
            
        return count
        
    def decode(self):
        self.clean_global_text()
        self.clean_encoded_text()
        self.generate_random_keys(self.key_length)
        rank = 0
        while(True):
            if self.random_keys[0][1] == self.answer_length:
                self.get_rank(self.random_keys[0][0], True)
                break
            self.mutation()
            self.crossover()
            
        return self.decoded_text
    
    def mutation(self):
        for k in range(len(self.random_keys)):
            for i in range(0, self.key_length):
                rand = random.randrange(100)
                if rand < 10:
                    new_char = random.choice(string.ascii_uppercase)
                    temp_key = list(self.random_keys[k][0])
                    temp_key[i] = new_char
                    new_rank = self.get_rank("".join(temp_key), False)
                    if new_rank > self.random_keys[k][1]:
                        self.random_keys[k][0] = "".join(temp_key)
                        self.random_keys[k][1] = new_rank                 
    
    def crossover(self):
        new_key = []
        i = 0
        while (i < len(self.random_keys) - 1):
            self.cross(i)
            i += 2
            
    def cross(self, i):
        key1 = list(self.random_keys[i][0])
        rank1 = self.random_keys[i][1]
        key2 = list(self.random_keys[i + 1][0])
        rank2 = self.random_keys[i + 1][1]
        
        rand = random.randrange(self.key_length)
        temp = key1
        key1 = key1[:rand + 1] + key2[rand + 1:]
        key2 = key2[:rand + 1] + temp[rand + 1:]
        
        rank1_new = self.get_rank("".join(key1), False)
        rank2_new = self.get_rank("".join(key2), False)
        
        self.random_keys.sort(key=lambda x: int(x[1]), reverse = True)
        if rank1_new > self.random_keys[len(self.random_keys) - 1][1]:
            self.random_keys[len(self.random_keys) - 1][0] = "".join(key1)
            self.random_keys[len(self.random_keys) - 1][1] = rank1_new
            
        if rank2_new > self.random_keys[len(self.random_keys) - 2][1]:
            self.random_keys[len(self.random_keys) - 2][0] = "".join(key2)
            self.random_keys[len(self.random_keys) - 2][1] = rank2_new
 


# In[6]:


encodedText = open('encoded_text.txt').read()
globalText = open('global_text.txt').read()
d = Decoder(globalText, encodedText, keyLength = 14)
decodedText = d.decode()

