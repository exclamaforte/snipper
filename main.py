import re
import pdb
# in: lines in byte string format
# out: send
class ByteStrList:
    def __init__(self, num):
        "Creates a list with a fixed length"
        self.LIMIT = num
        self.l = []
    def split(bstr):
        print(bstr)
        return re.split('[^a-zA-Z0-9]+', bstr)
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

def test1():
    s = Shrubbery()
    s.add("hi there man with b plan")
    s.add("hi george man with a plan")
    s.add("hi there mate")
    s.add("why make software")
    s.add("why make cranberries")
    print(str(s))
    print(s.weights())

def test2():
    s = Shrubbery()
    s.add("hi there man")
    s.add("bye there man")
    print(str(s))
    print(s.weights())

def test3():
    s = Shrubbery()
    s.add("hi there man")
    s.add("hi bye man")
    s.add("hi sigh man")
    print(str(s))
    print(s.weights())

def test4():
    s = Shrubbery()
    s.add("hi there man with b plan")
    s.add("hi george man with a plan")
    s.add("hi there mate")
    s.add("why make software")
    s.add("why make cranberries")
    print(str(s))
    print(s.weights())
    print(s.get_top())
