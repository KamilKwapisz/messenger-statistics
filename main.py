"""
Author: Kamil Kwapisz
Inspiration: https://github.com/MasterScrat/Chatistics, https://github.com/prokulski/
"""

from counting_emoticons import *
import os
from lxml import etree
from time import time, gmtime, strftime
import pandas as pd
import collections
import re
import logging

logging.basicConfig(filename = "exceptions.log",
                    level = logging.DEBUG,
                    format = '%(asctime)s %(message)s')
logger = logging.getLogger()


def main():

    #parsing arguments from command line
    myName, msg_dir_path = parse_arguments()

    # creating objects with dicts inside
    MyEmoticons = Emoticons_dict()
    InterlocutorsEmoticons = Emoticons_dict()

    # initializing counting variables and lists
    data = []
    words = []
    chars = 0
    timestamp = ''
    interlocutors = {} #initiliazing dict of interlocutors. Key = interlocutor name, value = number of msgs

    # setting a XML parser
    etree.set_default_parser(etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True))

    before = time() # variable for timing whole process
    for filename in os.listdir(msg_dir_path):

        if not filename.endswith('.html'):
            continue

        message_file = etree.parse(msg_dir_path + "/" + filename)

        senderName = ''
        interlocutorName = ""

        for element in message_file.iter():
            try:
                tag = element.tag
                className = element.get('class')
                content = element.text

                if tag == 'p':
                    text = content.lower()
                    tokens = re.findall(r'\w+', text)
                    words += tokens
                    chars += len(text)

                    if senderName is not "" and senderName == myName:
                        MyEmoticons.count_emoticons_usage(text)

                        # add new key to interlocutor's dict if a key doesn't exist
                        if interlocutorName not in interlocutors:
                            interlocutors[interlocutorName] = 0
                        interlocutors[interlocutorName] += 1 # increment number of messages with this interlocutor


                    elif senderName is not "" and senderName != myName:
                        interlocutorName = senderName
                        InterlocutorsEmoticons.count_emoticons_usage(text)

                        # add new key to interlocutor's dict if a key doesn't exist
                        if interlocutorName not in interlocutors:
                            interlocutors[interlocutorName] = 0
                        interlocutors[interlocutorName] += 1  # increment number of messages with this interlocutor


                    data += [[timestamp, interlocutorName, text]]

                elif tag == 'span':
                    if className == 'user':
                        senderName = content
                    elif className == 'meta':
                        timestamp = time.mktime(
                           pd.to_datetime(content, format='%A, %B %d, %Y at %H:%M%p', exact=False).timetuple())

                elif tag == 'h3':
                    content = content.replace('Conversation with ', '')
                    interlocutorName = content

            except Exception as e:
                logger.info("Exception {} was raised.".format(e))

    after = time()

    print_collected_data(MyEmoticons, InterlocutorsEmoticons, len(words), chars)

    print("Whole process took {:.2f} seconds".format(after-before))

    """
    counter = collections.Counter(words)
    print("10 most common words: ")
    print(counter.most_common(10))
    """

    df = pd.DataFrame(data)
    df.columns = ['timestamp', 'interlocutorname', 'text']
    df.to_pickle('all_messages.pkl')
    save_interlocutors_statistics(interlocutors)
    print("Statistics of messages was saved to file 'chat_stats.txt'")

if __name__ == "__main__":
    main()
