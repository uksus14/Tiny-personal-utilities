from math import exp
SIGMA = lambda x:(exp(x))/(1+exp(x))
ligit_letters = "йцукенгшщзхъфывапролджэячсмитьбю"
with open("frequency.txt", "r", encoding="utf-8") as file:
  letters_frequency = dict([(pair.split()[0], int(pair.split()[1])) for pair in file.read().split("\n")])
# а 40487008
# б 8051767
# в 22930719

expanding = 7
repeating_penalty = 2
display_offset = 5

def spreading(arr, expanding):
  arr_max, arr_min = max(arr.values()), min(arr.values())
  answer = {}
  for index, value in arr.items():
    transformation = SIGMA(expanding*(2*value-arr_max-arr_min)/(arr_max-arr_min))
    answer[index] = value*transformation
  return answer

spreading(letters_frequency, expanding)

with open("words.txt", "r", encoding="utf-8") as file:
  ligit_words = file.read().split()

def find_word():
  words = ligit_words
  absent = ""
  present = {letter: [] for letter in ligit_letters}
  while True:
    mask = input("Input mask:    ") # *с**а
    new_absent = input("Input absent:  ") # и
    new_present = input("Input present: ") # о**н
    if mask + new_absent + new_present == "":
      print("Reseted")
      break

    absent += new_absent
    mask = [(index, letter) for index, letter in enumerate(mask) if letter in ligit_letters] # *с**а -> [(1, c), (4, а)]
    new_present = [(letter, index) for index, letter in enumerate(new_present) if letter in ligit_letters]
    for letter, index in new_present:
      present[letter]+=[index]

    words = list(filter(lambda word: all([word[letter[0]] == letter[1] for letter in mask]), words)) # [(1, c), (4, а)]
    
    words = list(filter(lambda word: all([letter not in word for letter in absent]), words)) # и

    words = list(filter(lambda word: all([letter in word and word.find(letter) not in indexes for letter, indexes in present.items() if indexes]), words)) # {о:[0], н:[3]} 
    
    answers = []
    for word in words:
      efficiency = sum([letters_frequency[letter] for letter in word]) # more the sum -> more efficient the word is
      if len(word) != len(set(word)): efficiency /= repeating_penalty # repeating is not efficent
      answers.append((word, efficiency))

    answers = sorted(answers, key=lambda x: x[1])
    answers = [word for word, efficiency in answers]
    print((" "*display_offset).join(answers))

def main():
  print("mask - o**** means o is the first one")
  print("absent - ина means there is no и, н and а")
  print("present - *c*** means there is a c, but it's not second")
  print("Triple enter for new game")
  while True:
    find_word()

if __name__ == "__main__":
  main()