import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud
import pandas as pd
import re

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

print('Creating wordcloud...')
d = path.dirname(__file__)

# read the mask image - messenger logo
mask = np.array(Image.open(path.join(d, "messenger.png")))

df = pd.DataFrame()
try:
    df = pd.concat([df, pd.read_pickle('all_messages.pkl')])
except FileNotFoundError:
    print("There is no pickle file. Please try again")
    exit()

df.columns = ['timestamp', 'interlocutorname', 'text']
text = df['text'].str.lower()
text = ' '.join(text)

wc = WordCloud(max_words=100000, mask=mask, margin=10,
               random_state=1, background_color="black").generate(text)
default_colors = wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
          interpolation="bilinear")
wc.to_file("wordcloud.png")
plt.axis("off")
plt.show()
print('Wordcloud is ready!')
