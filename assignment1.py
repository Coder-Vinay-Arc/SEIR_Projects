import sys
import requests
from bs4 import BeautifulSoup

# Get title, body and links
def get_page_data(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    
    if soup.title:
        title = soup.title.text
    else:
        title = ""
        
    body = soup.get_text()
    
    links = []
    tags = soup.find_all("a")
    for tag in tags:
        link = tag.get("href")
        if link:
            links.append(link)
    return title, body, links

# Convert text into words
def count_frequency_from_text(text):

    text = text.lower()
    freq = {}
    word = ""
    for ch in text:
        if (ch >= 'a' and ch <= 'z') or (ch >= '0' and ch <= '9'):
            word = word + ch

        else:
            if word != "":
                if word in freq:
                    freq[word] = freq[word] + 1
                else:
                    freq[word] = 1
                word = ""
    if word != "":
        if word in freq:
            freq[word] = freq[word] + 1
        else:
            freq[word] = 1

    return freq

def rolling_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    for i in range(len(word)):
        s_i = ord(word[i])
        power_value = p ** i
        hash_value = hash_value + (s_i * power_value)%m
    return hash_value

# Convert integer to 64-bit binary
def to_64bit_binary(number):
    return format(number, '064b')

# Create 64-bit Simhash
def make_simhash(freq):
    V = []

    for i in range(64):
        V.append(0)
    for word in freq:
        weight = freq[word]
        h = rolling_hash(word)
        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                V[i] = V[i] + weight
            else:
                V[i] = V[i] - weight
    simhash_binary = ""

    for i in range(63, -1, -1):

        if V[i] > 0:
            simhash_binary = simhash_binary + "1"
        else:
            simhash_binary = simhash_binary + "0"
    return simhash_binary

# Count common bits
def count_common_bits(b1, b2):
    count = 0
    for i in range(64):
        if b1[i] == b2[i]:
            count = count + 1
    return count

# MAIN
url1 = sys.argv[1]
url2 = sys.argv[2]

# PROCESS URL 1
title1, body1, links1 = get_page_data(url1)

print("URL 1 Title:",title1)
print("URL 1 Body:",body1)

print("URL 1 Links:")
for link in links1:
    print(link)

freq1 = count_frequency_from_text(body1)

print("URL 1 Word Frequency Dictionary:",freq1)

print("URL 1 Word Hashcodes (64-bit binary):")
for word in freq1:
    h = rolling_hash(word)
    binary_hash = to_64bit_binary(h)
    print(word, ":", binary_hash)
simhash1 = make_simhash(freq1)

# PROCESS URL 2
title2, body2, links2 = get_page_data(url2)

print("URL 2 Title:",title2)
print("URL 2 Body:",body2)

print("URL 2 Links:")
for link in links2:
    print(link)

freq2 = count_frequency_from_text(body2)

print("URL 2 Word Frequency Dictionary:",freq2)

print("URL 2 Word Hashcodes (64-bit binary):")
for word in freq2:
    h = rolling_hash(word)
    binary_hash = to_64bit_binary(h)
    print(word, ":", binary_hash)
simhash2 = make_simhash(freq2)

# FINAL OUTPUT
common_bits = count_common_bits(simhash1, simhash2)
print("Simhash 1 (64-bit binary):", simhash1)
print("Simhash 2 (64-bit binary):", simhash2)
print("Common bits:", common_bits)