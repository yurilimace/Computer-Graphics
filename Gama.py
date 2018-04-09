from PIL import Image
im_filename ="Yuri.jpg" 
im = Image.open(im_filename)
im2 = Image.open(im_filename)
imH = im.size[0]
imW = im.size[1]
gama = 1

#easyway
#list_matrix = list(im.getdata())

list_matrix = im.load()

new_image_matrix =[]

'''for i in range(len(list_matrix)):
    r = int(((i[0]/255)**gama)*255)
    g = int(((i[1]/255)**gama)*255)
    b = int(((i[2]/255)**gama)*255)
    new_image_matrix.append((r,g,b))
'''
for i in range(0,imH,1):
    for k in range(0,imW,1):
        r = int (((list_matrix[i,k][0]/255)**gama)*255)
        g = int (((list_matrix[i,k][1]/255)**gama)*255)
        b = int (((list_matrix[i,k][2]/255)**gama)*255)
        list_matrix[i,k] = (r,g,b)

   


#new_image = Image.new(im.mode,im.size)
#new_image.putdata(result_image)

#new_image.show()
im2.show()
im.show()
