from pygame import image

fonts ={}
images={}

#Getting integer values
def convert_to_int(*args):
    return_value=[]

    for arg in args:
        return_value.append(int(arg))

    return return_value

#loading the image for optimization of rendering
