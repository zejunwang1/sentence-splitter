import os
import re
import regex
import warnings
from enum import Enum
from typing import List, Tuple, Union

def split_text_into_sentences(
    text: str, fast: bool = True, merge_and_split: bool = False, return_loc: bool = False, min_length: int = 16, max_length: int = 256
) -> Union[List[str], Tuple[List[str], List[int]]]:
    """
    Split Chinese text into sentences.
    
    Parameters:
        text (`str`):
            Text to be split into individual sentences.
        fast (`bool`, *optional*, defaults to `True`):
            Whether to enable fast mode.
        merge_and_split (`bool`, *optional*, defaults to `False`):
            Whether to merge short sentences and split long sentences.
        return_loc (`bool`, *optional*, defaults to `False`):
            Whether to return the character position of the sentence in the original text string.
        min_length (`int`, *optional*, defaults to 16):
            Minimum sentence length within a paragraph. When the length of a sentence is less than min_length, 
            the short sentences in the paragraph are merged. Sentences in different paragraphs are not merged.
        max_length (`int`, *optional*, defaults to 256):
            Maximum sentence length within a paragraph. When the length of a sentence is greater than max_length, 
            the long sentence is further segmented based on punctuation marks.
    """

    if text is None or not text:
        warnings.warn("Text is None or empty.")
        return ([], []) if return_loc else []
    
    locations, sentences = [], []

    # Current character position
    cur = 0

    # Maximum backtracking length
    maxMove = max_length - min_length

    # Paragraphs
    paragraphs = text.split('\n')

    for paragraph in paragraphs:
        n = len(paragraph)
        if not paragraph.strip():
            cur += n
            cur += 1
            continue
        
        # Split by punctuation
        if fast:
            paragraph = re.sub(pattern=r'([。！？!?]+[”’]*)(.)', repl='\\1\n\\2', string=paragraph)
        else:
            paragraph = re.sub(pattern=r'([。！？]+[”’]*)(.)', repl='\\1\n\\2', string=paragraph)
            # Chinese character ending with !/?
            paragraph = re.sub(pattern=r'([\u4e00-\u9fa5][\ ]*[!?]+[”’]*)(.)', repl='\\1\n\\2', string=paragraph)
            paragraph = re.sub(pattern=r'([!?][\ ]*)([\u4e00-\u9fa5])', repl='\\1\n\\2', string=paragraph)

        if n > max_length and not re.findall(pattern=r'[。！？]', string=paragraph):
            # Chinese character ending with ./;/；
            paragraph = re.sub(pattern=r'([\u4e00-\u9fa5][\ ]*[\.;；]+)(.)', repl='\\1\n\\2', string=paragraph)
            paragraph = re.sub(pattern=r'([\.;；][\ ]*)([\u4e00-\u9fa5])', repl='\\1\n\\2', string=paragraph)

        sentence_list = paragraph.split('\n')

        if not merge_and_split:
            for sentence in sentence_list:
                sentences.append(sentence)
                locations.append(cur)
                cur += len(sentence)
            cur += 1
            continue

        # Merge short sentences and split long sentences
        start = 0
        end = len(sentence_list)
        before = len(sentences)
        while start < end:
            sentence = sentence_list[start]
            l = len(sentence)
            if l >= min_length and l <= max_length:
                locations.append(cur)
                sentences.append(sentence)
                start += 1
                cur += l
                continue

            while l < min_length and start < end - 1:
                start += 1
                sentence += sentence_list[start]
                l = len(sentence)
            if l <= max_length:
                locations.append(cur)
                sentences.append(sentence)
                start += 1
                cur += l
                continue

            # Backtracking segmentation
            while l > max_length:
                move = 1
                while move < maxMove:
                    if sentence[max_length - move] in [',', '，', ';', '；', '\t']:
                        break
                    move += 1
                if move == maxMove:
                    move = 1
                    while move < maxMove:
                        if sentence[max_length - move] in ['、', ' ']:
                            break
                        move += 1
                if move == maxMove:
                    locations.append(cur)
                    sentences.append(sentence[ : max_length])
                    sentence = sentence[max_length : ]
                    cur += max_length
                else:
                    p = max_length - move + 1
                    locations.append(cur)
                    sentences.append(sentence[ : p])
                    sentence = sentence[p : ]
                    cur += p
                l = len(sentence)

            if l < min_length:
                sentences[-1] += sentence
            else:
                locations.append(cur)
                sentences.append(sentence)
            start += 1
            cur += l

        after = len(sentences)
        if after - before > 1 and len(sentences[-1]) < min_length:
            sentences[-2] += sentences[-1]
            locations.pop()
            sentences.pop()
        cur += 1

    return (sentences, locations) if return_loc else sentences


# Copied and modified from 
# https://github.com/mediacloud/sentence-splitter/blob/develop/sentence_splitter/__init__.py
class PrefixType(Enum):
    DEFAULT = 1
    NUMERIC_ONLY = 2

def load_non_breaking_prefix(non_breaking_prefix_file: str = None):
    non_breaking_prefixes = dict()
    if non_breaking_prefix_file is None:
        pwd = os.path.dirname(os.path.abspath(__file__))
        prefix_dir = os.path.join(pwd, 'non_breaking_prefixes')
        non_breaking_prefix_file = os.path.join(prefix_dir, 'en.txt')

    if not os.path.isfile(non_breaking_prefix_file):
        raise Exception(
            "Non-breaking prefix file for language en was not found at path '{}'".format(
                non_breaking_prefix_file)
            )

    with open(non_breaking_prefix_file, mode='r', encoding='utf-8') as prefix_file:
        for line in prefix_file.readlines():

            if '#NUMERIC_ONLY#' in line:
                prefix_type = PrefixType.NUMERIC_ONLY
            else:
                prefix_type = PrefixType.DEFAULT
            
            # Remove comments
            line = regex.sub(pattern=r'#.*', repl='', string=line, flags=regex.DOTALL | regex.UNICODE)

            line = line.strip()
            if not line:
                continue

            non_breaking_prefixes[line] = prefix_type

    return non_breaking_prefixes


__non_breaking_prefixes = load_non_breaking_prefix()


def split_en_text_into_sentences(
    text: str, split_long: bool = False, return_loc: bool = False, max_length: int = 1024
) -> Union[List[str], Tuple[List[str], List[int]]]:
    """
    Split English text into sentences.
    
    Parameters:
        text (`str`):
            Text to be split into individual sentences.
        split_long (`bool`, *optional*, defaults to `False`):
            Whether to split long sentences.
        return_loc (`bool`, *optional*, defaults to `False`):
            Whether to return the character position of the sentence in the original text string.
        max_length (`int`, *optional*, defaults to 1024):
            Maximum sentence length within a paragraph. When the length of a sentence is greater than max_length,
            the long sentence is further segmented based on punctuation marks.
    """
    if not text:
        warnings.warn("Text is None or empty.")
        return ([], []) if return_loc else []
       
    source = text

    # Non-period end of sentence markers (?!) followed by sentence starters
    text = regex.sub(
        pattern=r'([?!]) +([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',
        repl='\\1\n\\2',
        string=text,
        flags=regex.UNICODE
    )

    # Multi-dots followed by sentence starters
    text = regex.sub(
        pattern=r'(\.[\.]+) +([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',
        repl='\\1\n\\2',
        string=text,
        flags=regex.UNICODE
    )

    # Add breaks for sentences that end with some sort of punctuation inside a quote or parenthetical and are 
    # followed by a possible sentence starter punctuation and upper case
    text = regex.sub(
        pattern=(
            r'([?!\.][\ ]*[\'")\]\p{Final_Punctuation}]+) +([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\ ]*'
            r'[\p{Uppercase_Letter}\p{Other_Letter}])'
        ),
        repl='\\1\n\\2',
        string=text,
        flags=regex.UNICODE
    )

    # Add breaks for sentences that end with some sort of punctuation and are followed by a possible sentence 
    # starter punctuation and upper case
    text = regex.sub(
        pattern=(
            r'([?!\.]) +([\'"([\u00bf\u00A1\p{Initial_Punctuation}]+[\ ]*[\p{Uppercase_Letter}\p{Other_Letter}])'
        ),
        repl='\\1\n\\2',
        string=text,
        flags=regex.UNICODE
    )

    # Special punctuation cases are covered. Check all remaining periods
    words = text.split(' ')
    i, n = 0, len(words)
    while i < n - 1:
        word = words[i]
        if not word.endswith('.'):
            i += 1
            continue

        # Not breaking - 2017 . 12
        if word == '.' and i > 0 and words[i - 1].isdigit() and words[i + 1].isdigit():
            i += 2
            continue

        j = i + 1
        while j < n - 1 and not words[j]:
            j += 1

        match = regex.search(pattern=r'([\w\.\-]*)([\'"\)\]%\p{Final_Punctuation}]*)(\.+)$',
                             string=word,
                             flags=regex.UNICODE)
        if match:

            prefix = match.group(1)
            starting_punct = match.group(2)

            def is_prefix_honorific(prefix_: str, starting_punct_: str) -> bool:
                """Check if \\1 is a known honorific and \\2 is empty."""
                if prefix_:
                    if prefix_ in __non_breaking_prefixes:
                        if __non_breaking_prefixes[prefix_] == PrefixType.DEFAULT:
                            if not starting_punct_:
                                return True
                return False

            if is_prefix_honorific(prefix_=prefix, starting_punct_=starting_punct):
                # Not breaking
                pass

            elif regex.search(pattern=r'(\.)[\p{Uppercase_Letter}\p{Other_Letter}\-]+(\.+)$',
                              string=word,
                              flags=regex.UNICODE):
                # Not breaking - upper case acronym
                pass

            elif regex.search(
                    pattern=(
                        r'^([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}0-9])'
                    ),
                    string=words[j],
                    flags=regex.UNICODE
            ):

                def is_numeric(prefix_: str, starting_punct_: str, next_word: str):
                    """The next word may have a bunch of initial quotes, then either upper case or a number."""
                    if starting_punct_:
                        return False
                    if prefix_:
                        if regex.search(pattern=r'[0-9]+$', string=prefix_, flags=regex.UNICODE) or (
                            prefix_ in __non_breaking_prefixes and 
                            __non_breaking_prefixes[prefix_] == PrefixType.NUMERIC_ONLY
                        ):
                            if regex.search(pattern='^[0-9]+', string=next_word, flags=regex.UNICODE):
                                return True
                    return False

                if not is_numeric(prefix_=prefix, starting_punct_=starting_punct, next_word=words[j]):
                    words[i] += '\n'

        # Move to the next non-empty position
        i = j

    text = ' '.join(words)
    """
    locations, sentences = [], []
    # Starting search position
    start = 0
    for sentence in text.split('\n'):
        sentence = sentence.strip()
        if not sentence:
            continue
        # Get the position of the sentence in the original text
        p = source.find(sentence[0], start)
        start = p + len(sentence)
        locations.append(p)
        sentences.append(sentence)
    """
    locations, sentences = [], []
    sentence_list = text.split('\n')
    i, n = 0, len(sentence_list)

    # Starting position for search
    start = 0

    # Maximum backtracking length
    maxMove = int(max_length * 3 / 4)

    while i < n:
        sentence = sentence_list[i].strip()
        if not sentence:
            i += 1
            continue
        l = len(sentence)
        p = source.find(sentence[0], start)
        start = p + l
        #if l <= 4 and sentence.find(' ') < 0 and sentence[-1] == '.' and i < n - 1:
        if l <= 16 and sentence.find(' ') < 0 and i < n - 1:
            next_sentence = sentence_list[i + 1].strip()
            if not next_sentence:
                locations.append(p)
                sentences.append(sentence)
                i += 2
                continue
            next_p = source.find(next_sentence[0], start)
            interval = next_p - start
            space = ' ' * interval
            if interval <= 4 and source[start : next_p] == space:
                # Merge with the next sentence
                next_l = len(next_sentence)
                sentence = source[p : next_p + next_l]
                start = next_p + next_l
                l = len(sentence)
                i += 1

        if not split_long or l <= max_length:
            locations.append(p)
            sentences.append(sentence)
            i += 1
            continue

        # Backtracking segmentation
        while l > max_length:
            move = 1
            while move < maxMove:
                if sentence[max_length - move] in [',', ';', '\t']:
                    break
                move += 1
            if move == maxMove:
                move = 1
                while move < maxMove:
                    if sentence[max_length - move] == ' ':
                        break
                    move += 1
            if move == maxMove:
                origin = sentence[ : max_length]
                strip  = origin.strip()
                offset = origin.index(strip[0])
                locations.append(p + offset)
                sentences.append(strip)
                sentence = sentence[max_length : ]
                p += max_length
            else:
                end = max_length - move + 1
                origin = sentence[ : end]
                strip  = origin.strip()
                if strip:
                    offset = origin.index(strip[0])
                    locations.append(p + offset)
                    sentences.append(strip)
                sentence = sentence[end : ]
                p += end
            l = len(sentence)
        
        strip = sentence.strip()
        offset = sentence.index(strip[0])
        locations.append(p + offset)
        sentences.append(strip)
        i += 1

    return (sentences, locations) if return_loc else sentences

