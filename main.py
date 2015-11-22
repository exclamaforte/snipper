import socket
from threading import Thread
import re
# in: lines in byte string format
# out: send
puncts = [b']', b'[', b'{', b'}', b'(', b')', b'>', b'<', b'?', b':', b'~']

class ByteStrList:
    def __init__(self, num):
        "Creates a list with a fixed length"
        self.LIMIT = num
        self.l = []
    def split(bstr):
        #TODO prune empty string
        for s in puncts:
            bstr = bstr.replace(s, b' ' + s + b' ')
        return list(filter(None, re.split(b'[^a-zA-Z0-9\]\[\{\}\(\)\>\<\?\:\~]+', bstr)))

    def add_line(self, bytestring):
        "Add a line to the list"
        s = ByteStrList.split(bytestring)
        self.l.append(s)
        if len(self.l) > self.LIMIT:
            self.l.pop(0)
        return s

class ShrubNode:
    def __init__(self, value):
        #list of ShrubNodes
        self.children = []
        self.weight = 0
        self.value = value

    def is_root(self):
        "is root if the value is None"
        return self.value == None

    def next_inc_lookahead1(self, val):
        """Select the child with val == val and increment the weight.
        If it is not found, create a new Shrubnode,
        add it to the list, increment the weight"""
        for child in self.children:
            if child.value == val:
                child.weight += 1
                return child
        h = ShrubNode(val)
        h.weight += 1
        self.children.append(h)
        return h

    def next_inc_lookahead2(self, val1, val2):
        """Select the child with val == val and increment the weight.
        If it is not found, create a new Shrubnode,
        add it to the list, increment the weight"""
        #check for matches
        for child in self.children:
            if child.value == val1:
                child.weight += 1
                return [child, 1]
        for parent_child in self.children:
            for child_child in parent_child.children:
                if val2 == child_child.value:
                    h1 = ShrubNode(val1)

                    h1.weight += 1
                    child_child.weight += 1

                    self.children.append(h1)
                    h1.children.append(child_child)
                    return [child_child, 2]
        h1 = ShrubNode(val1)
        h2 = ShrubNode(val2)

        h1.weight += 1
        h2.weight += 1

        self.children.append(h1)
        h1.children.append(h2)
        return [h2, 2]

    def find(self, val):
        for child in self.children:
            if child.value == val:
                return child

    def __str__(self):
        return self.__str_helper__(0)

    def __str_helper__(self, i):
        ret = "|---" * i + str(self.value) +":" + str(self.weight) + "\n"
        i += 1
        for child in self.children:
            ret += child.__str_helper__(i)
        return ret

    def string_weights(self):
        return self.__weightshelper__(0)

    def __weightshelper__(self, indent):
        ret = "|---" * indent + str(self.weight) + "\n"
        indent += 1
        for child in self.children:
            ret += child.__weightshelper__(indent)
        return ret

class Shrubbery:
    def __init__(self):
        self.root = ShrubNode(None)
        self.bsl = ByteStrList(1000)
        self.num_in = 0

    def add(self, bytestring):
        "adds a byte string to the Shrubbery"
        self.num_in += 1
        value_list = self.bsl.add_line(bytestring)
        self.root.weight += 1
        node = self.root.next_inc_lookahead1(value_list[0])
        i = 1
        while i < len(value_list):
            if i == len(value_list) - 1:
                node.next_inc_lookahead1(value_list[i])
                i += 1
            else:
                tpl = node.next_inc_lookahead2(value_list[i], value_list[i+1])
                node = tpl[0]
                i += tpl[1]

    def get_top(self):
        """there's some black magic in this algorithm
        returns a list of bytestrings, or 0, which denotes a star"""
        top_score = 0
        top_pattern = []
        for ln in self.bsl.l:

            score = 0
            pattern = []
            node = self.root
            for wrd in ln:
                node2 = node.find(wrd)
                if node2.weight > node.weight:
                    #this means that there's a split
                    pattern.append(0)
                    score += 3 * node2.weight
                else:
                    pattern.append(node.value)
                    score += node2.weight
                node = node2
            pattern.append(node.value)
            if score > top_score:
                top_pattern = pattern
                top_score = score
        return [top_pattern[1:], top_score]

    def clear(self):
        del self.root
        self.root = ShrubNode(None)
        del self.bsl
        self.bsl = ByteStrList(1000)
        self.num_in = 0

    def __str__(self):
        return self.root.__str__()

    def weights(self):
        return self.root.string_weights()



HOST = 'localhost'
PORT_OUT = 53706
PORT_IN = 53707

def get_input():
    index = 0
    print('Connected by', addr_in)
    while True:
        index += 1
        data = conn_in.recv(1024) #size?
        if not data:
            break
        print(data)
        shrub.add(data)
        if index % 20 == 0:
            print(shrub.get_top())
        # conn.sendall(data)
        # recieve(data)
    conn_in.close()

def recieve(str_in):
    print(str_in)
    send_result(str_in)

def send_result(str_out):
    # conn_out.sendall(str_out)
    # socket_out.sendall(str_out)
    print("SENT")

if __name__ == "__main__":
    shrub = Shrubbery()


    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.bind((HOST, PORT_IN))
    socket_in.listen(1)
    conn_in, addr_in = socket_in.accept()
    print('asrtars')

    # socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket_out.connect((HOST, PORT_OUT))
    # socket_out.listen(1)
    # conn_out, addr_out = socket_out.accept()
    print('asrtars')

    input_thread = Thread(target = get_input)
    input_thread.start()
    input_thread.join()
    print("done")
