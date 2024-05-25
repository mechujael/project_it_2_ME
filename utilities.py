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
def load_image(path_to_image):
    if images.get(path_to_image)==None:
        images[path_to_image]= image.load()