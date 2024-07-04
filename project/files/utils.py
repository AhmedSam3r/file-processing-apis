from project.settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import os
from typing import IO, Union
import random
from datetime import datetime


def validate_directory_path(path: str) -> None:
    # make method  to check or create 'static'' folder
    if not os.path.exists(path):
        os.mkdir(UPLOAD_FOLDER)


def upload_file(file_obj: IO, file_name: str) -> bool:
    try:
        validate_directory_path(UPLOAD_FOLDER)
        file_obj.save(f"{UPLOAD_FOLDER}/{file_name}")
        return True, UPLOAD_FOLDER
    except Exception as ex:
        print("LOG Err = ", ex)
        return False, UPLOAD_FOLDER


def get_blob_size(blob: IO) -> float:
    '''file size in KB'''
    return blob.seek(0, os.SEEK_END)


def valid_blob_size(blob: IO) -> bool:
    try:
        blob_length = get_blob_size(blob)
        print("blob length ", blob_length)
        MAX_SIZE = 50 * 1024 * 1024  # 50 MB
        if blob_length > MAX_SIZE:
            return False, blob_length
        # seek back to start position of stream,
        # otherwise save() will write a 0 byte blob
        # os.SEEK_END == 0
        blob.seek(0, os.SEEK_SET)
    except Exception as ex:
        print(f"valid_blob_size err {ex}")
        return False, blob_length

    return True, blob_length


def retrieve_file(blob_id: IO) -> Union[IO, None]:
    try:
        blob = open(f"{UPLOAD_FOLDER}/{blob_id}")
        return blob
    except Exception as ex:
        print("retrieve_file ", ex)
        pass
    return None


def most_common_character(word: str):
    words_count = {}
    if not word:
        print("NOT WORD ==> ", word)
        return ''
    # this working
    for letter in word:
        words_count[letter] = words_count.get(letter, 0) + 1
    # not working check why
    # words_count = {letter: words_count.get(letter, 0) + 1 for letter in word}
    # print(words_count)
    frequencies = {v: k for k, v in words_count.items()}
    max_count = max(frequencies)
    return frequencies[max_count]

    # max_count = {}
    # for letter in word:
    #     letter_count = words_count.get(letter, 0)
    #     words_count[letter] =  letter_count + 1
    #     max_count = letter_count if letter_count > max_count else


def read_in_chunks(id: str, chunk_size: int = 1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    file_object = retrieve_file(id)
    # file_size = os.path.getsize(file_object)
    # while chunk := file_object.readlines(chunk_size):
    while chunk := file_object.readline():
        # print(f"tell() ={file_object.tell()}")
        yield chunk

    file_object.close()


def get_random_line(id: str, max_count, reverse=False) -> str:
    result = {
        "line_number": -1,
        "line_text": ""
    }
    try:
        text = ""
        random.seed(int(datetime.now().timestamp()))
        # TODO make it the max file size
        n = 100
        line_number = random.randint(0, max_count)
        # print("line_number=", line_number)
        blob_generator = read_in_chunks(id)
        line_by_line = ""
        count = 0
        for count, piece in enumerate(blob_generator):
            line_by_line = piece
            if count == line_number:
                print(f"HERE count={count} == line_number={line_number}")
                break
            text += line_by_line

        result["line_text"] = line_by_line.split("\n")[0] \
            if reverse is False \
            else reverse_string(line_by_line.split("\n")[0])
        result["line_number"] = count
        result["common_char"] = most_common_character(result["line_text"])
        return result
    except Exception as ex:
        print("EX = ", ex)
        return {}


'''
        # with open(f"{UPLOAD_FOLDER}/{id}") as blob:

            # while chunk := blob.read(chunk_size):
            #     print("@@@@@@@@@@@@@@@")
            #     print("chunk", chunk)
            #     text += chunk
            #     print("@@@@@@@@@@@@@@@")
            # for chunk in iter(lambda: blob.read(chunk_size), b''):
            #     print("blob ", bl)
            #     print("chunk = ", chunk)
'''


def reverse_string(string):
    return string[::-1]


def strtobool(val: str):
    """
    Manual copying, Since the method is deprecated
    Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return bool(1)
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return bool(0)
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_most_longest_x_lines(id, lines_count=20, reverse=True):
    try:
        blob_generator = read_in_chunks(id)
        list_of_line_sizes = []
        for index, content in enumerate(blob_generator):
            list_of_line_sizes.append((index, content, len(content)))
        blob_generator.close()
        # if lines_count > len(list_of_line_sizes):
        #     return []

        list_of_line_sizes.sort(key=lambda x: x[1], reverse=reverse)
        # final_result = {}
        final_result_list = []
        for index, content, size in list_of_line_sizes[:lines_count]:
            # final_result[line] = count
            final_result_list.append({
                "index": index,
                "content": content,
                "size": size
            })

        return final_result_list
    except Exception as ex:
        print("get_most_longest_x_lines() err", ex)


def allowed_file(filename):
    return (
        '.' in filename and filename.rsplit('.', 1)[1].lower() 
        in ALLOWED_EXTENSIONS
    )


def count_lines_number(path, file_name):
    file_path = os.path.join(path + '/' + file_name)
    with open(file_path, 'r') as f:
        number_of_lines = sum(1 for line in f)

    return number_of_lines
