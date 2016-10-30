import prefpy
from prefpy import preference
from prefpy import profile
from prefpy.profile import Profile

if __name__ == '__main__' :

    data=Profile({},[])
    print(type(data))

    data.importPreflibFile("input")
    #data
    print(data.getWmg())
