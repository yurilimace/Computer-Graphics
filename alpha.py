from PIL import Image

img = Image.open("bp.jpeg")
img2 = Image.open("bp.jpeg")

mas = Image.open("ac.png")
dart = Image.open("fp.png")

px = img.load()
px1 = mas.load()
px2 = dart.load()

#gamma=1

tamX = img.size[0]
tamY = img.size[1]

for i in range(0,tamX,1):
    for j in range(0,tamY,1):

##        #red
##        nvr = (px[i,j][0]/255)**gamma
##        red = int( 255 * nvr )
##        #green
##        nvg = (px[i,j][1]/255)**gamma
##        green = int(255 * nvg)
##        #blue
##        nvb = (px[i,j][2]/255)**gamma
##        blue = int(255 * nvb)

        red = int(px1[i,j][0]/255) * px2[i,j][0]
        green = int(px1[i,j][1]/255) * px2[i,j][1]
        blue = int(px1[i,j][2]/255) * px2[i,j][2]

        px2[i,j] = (red,green,blue)

        alpha = 0.25

        red2 = int((alpha*px2[i,j][0]) + ((1-alpha)*px[i,j][0]))
        green2 = int((alpha*px2[i,j][1]) + ((1-alpha)*px[i,j][1]))
        blue2 = int((alpha*px2[i,j][2]) + ((1-alpha)*px[i,j][2]))

        px[i,j] = (red2,green2,blue2)

#dart.show()
img.show()

#img2.show()
#img.show()