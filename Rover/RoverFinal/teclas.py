

"""

def pressON(key):
    print("presiono: {}".format(key))
def pressOFF(key):
    print(key)
    try:
        if key == key.esc:
            print("algo")

    except:
        if key == 31:
            print("millos")

with Listener(on_press=pressON, on_release = pressOFF) as listener:
    listener.join()
    
    """

