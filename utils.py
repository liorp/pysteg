def str2bin(string):
    # Returns binary representation of a string
    return ''.join((bin(ord(i))[2:]).zfill(7) for i in string)


def bin2str(string):
    # Returns text representation of a binary string
    return ''.join(chr(int(string[i:i+7], 2)) for i in range(len(string))[::7])
