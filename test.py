import main
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
