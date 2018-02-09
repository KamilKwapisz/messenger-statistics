import operator
import argparse

#list of emoticons that are being count
emoticons = [[':d', ';d', 'xd'], [':)', ';)'], [':p', ';p'], [':*', ';*'], ['<3'], [':(', ';(', ';c', ':c', ';<', ':<']]

class Emoticons_dict(object):
    """
    Class containing dictionary with emoticons types as keys and
    number of each group of emoticons types used as a values 
    """
    def __init__(self):
        self.emoticons_counter = {':D' : 0,
                             ':)' : 0,
                             ':P' : 0,
                             ':*' : 0,
                             '<3' : 0,
                             ':(' : 0}
        self.summary = 0

    def count_emoticons_usage(self, message_text : str):
        for emoticon_list in emoticons:
            for emoticon in emoticon_list:
                self.emoticons_counter[emoticon_list[0].upper()] += message_text.count(emoticon)
                self.summary += message_text.count(emoticon)

def parse_arguments():
    """
    Function is parsing arguments from command line
    it takes no arguments itself
    and returns name of messages owner and path to messages dir
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-myName", dest='myName', type=str, help="Your name o Messanger", required=True)
    parser.add_argument("-f", dest='msg_dir_path', help="Path to directory with message files", default='.\messages')
    args = parser.parse_args()
    return args.myName, args.msg_dir_path


def print_dict(emoticons_counter: dict):
        for item in emoticons_counter:
            print(item, ':', "{:,}".format(emoticons_counter[item]))


def print_collected_data(MyEmoticons: object, InterlocutorsEmoticons: object, words_counter: int, chars: int):
    print("My emoticons: ")
    print_dict(MyEmoticons.emoticons_counter)
    print("All emoticons:{:,}".format(MyEmoticons.summary))

    print("My interlocutor's emoticons: ")
    print_dict(InterlocutorsEmoticons.emoticons_counter)
    print("All emoticons: {:,}".format(InterlocutorsEmoticons.summary))

    print("Words: {:,} characters {:,}".format(words_counter, chars))


def save_interlocutors_statistics(interlocutors: dict):
    """
    Function is saving statistics of each interlocutors number of messages
    into a file
    """
    interlocutors_tuple = sorted(interlocutors.items(), key=operator.itemgetter(1))[::-1]  # sort dict by values DESC

    with open("chat_stats.txt", "w") as output_file:
        for key in interlocutors_tuple:
            newstring = str(key[0]) + ": " + "{:,}".format(key[1]) + "\n"
            output_file.write(newstring)

