import numpy as np
from PIL import Image as PilImage
import copy

##### function that mount the matrix w
def Building_Matrix(Nx,Ny):
    Line = []
    Colunm = []
    for i in range(0,Nx,1): #colunas
      for j in range(0,Ny,1): #linhas
        Line.append(0);
      Colunm.append(Line)
      Line =[]
    return Colunm


def Transform_into_npMatrix(Matrix):
     aux = np.asmatrix(Matrix)
     return aux



##### function that build the image matrix ##########
def Building_Image(Nx,Ny):
    Line = []
    Colunm = []
    for i in range(0,Nx,1): #colunas
      for j in range(0,Ny,1): #linhas
        Line.append([0,0,0]);
      Colunm.append(Line)
      Line =[]
    return Colunm

#### function that calculate the module of vector #############
def Norma(Vector):
    norma = 0
    root = np.power(Vector,2)
    for i in root:
        norma += i
    return norma**0.5


#### calculate and build vector w #########
def Building_Vector_w(New_Vector,Vector_e,Norma_e):
    for i in range(0,len(Vector_e)):
        New_Vector[i] = Vector_e[i]/Norma_e

#### calculate and build vector t #########
def Building_Vector_T(Vector_w):
    Vector_t = Vector_w[:]
    minor = 0
    for i in range(0,len(Vector_t)-1):
        if (Vector_t[i] < Vector_t[i+1]):
            minor = i
        elif(Vector_t[i] == Vector_t[i+1]):
            minor = i
    Vector_t[minor] = 1
    return Vector_t
#### calculate and build vector u #########
def Building_Vector_U(Vector_t,Vector_w):
    aux = np.cross(Vector_t,Vector_w)
    return  np.cross(Vector_t,Vector_w)/Norma(aux)


###### Calculate the U and V vectors that build the ray ################
def Calculate_U_and_V(Matrix,left,right,bottom,top,Nx,Ny):
    for i in range(0,Nx-1,1):
        for j in range(0,Ny-1,1):
            U = left +  (right - left) * (i + 0.5)/Nx
            V = bottom + (top - bottom) * ( j + 0.5)/Ny
            Matrix[i][j] = (U,V)
    print(Matrix)

#####Calculate ray in ortographic case ##############
def Orto(Vector_e,Vector_u,Vector_v,Vector_w,Nx,Ny,Matrix):
   direct = np.dot(Vector_w,-1)
   for i in range(0,Nx-1):
           for j in range(0,Ny-1):
               scalar_u = np.dot(Vector_u,Matrix[i][j][0])
               scalar_v = np.dot(Vector_v,Matrix[i][j][1])
               origin = Vector_e + scalar_u + scalar_v
               Matrix[i][j] = (origin,direct)




###calculates whether the ray touches the sphere#########
def Delta(Matrix, spheres, nx, ny, image, list_point):
     for i in range(0,nx-1):
                for j in range(0,ny-1):
                    list_aux=[]
                    for sphere in spheres:
                        e_origin = Matrix[i,j][0]
                        direct = Matrix[i,j][1]
                        A = np.dot(direct,direct)
                        B = 2 * np.dot(direct, (e_origin - sphere[0]))
                        C = np.dot((e_origin - sphere[0]), (e_origin - sphere[0])) - sphere[1]
                        delta = (B**2) - 4*A*C
                        if(delta >= 0):
                             t1 = ((B*(-1))+(delta**(1/2)))/(2*A)
                             t2 = ((B*(-1))-(delta**(1/2)))/(2*A)
                             t1 = abs(t1)
                             t2 = abs(t2)
                             menor = min(t1,t2)
                             point = e_origin + (direct*menor)      ##### calculate p(t) and append in a list of points ######
                             list_point.append(point - sphere[0])
                             list_aux.append([menor, sphere[2]])
                        else:
                            list_aux.append(["black","black"])

                    minor_2 = 50000000000000000;
                    color = [0,0,0]
                    for elem in list_aux:
                        if(elem[0]!="black"):
                            if(elem[0]<minor_2):
                                minor_2 = elem[0]
                                color = elem[1]
                                print(color)
                    image[i][j] = color




####Calculate the vector l for the ilumination ################
def Calculate_Vetor_L(lamp, spheres):
    vector_l =[]
    for sphere in spheres:
        aux = lamp - sphere[0]
        vector_l.append(aux)
    return vector_l

###### mount and shows the image with drawn object ##########
def Mount_image(Nx,Ny,Image):
    img = PilImage.new('RGB', (Nx, Ny))
    px = img.load()
    for i in range(0,Nx):
        for j in range(0,Ny):
           px[i,j] = (image[i][j][0],image[i][j][1],image[i][j][2])
    img.show()




####  global variables ##########
Nx = 640
Ny =480
left = -13
right = 13
top = 10
bottom = -10
Vector_e = [10,10,10]
Vector_w=[0,0,0]
Matrix = Building_Matrix(Nx,Ny)
image = Building_Image(Nx,Ny)
spheres = [[(0, 0, 0), 1, (100, 150, 100)], [(-1, 0, -2), 2, (250, 250, 250)]]

###### ilumination variables #######
lamp = [5,10,-10]
lamp = np.asarray(lamp)
Vector_l = Calculate_Vetor_L(lamp, spheres)
list_n=[]

#building vectors
norma_Vector_e = Norma(Vector_e)
Building_Vector_w(Vector_w,Vector_e,norma_Vector_e)
Vector_t = Building_Vector_T(Vector_w)
Vector_u = Building_Vector_U(Vector_t,Vector_w)
Vector_v = np.cross(Vector_u,Vector_w)

#calculate U and V to build rays
Calculate_U_and_V(Matrix,left,right,bottom,top,Nx,Ny)
#calculate in ortographic case
Orto(Vector_e,Vector_u,Vector_v,Vector_w,Nx,Ny,Matrix)
#####transfor into a numpy Matrix ########
Matrix = Transform_into_npMatrix(Matrix)

Delta(Matrix, spheres, Nx, Ny, image, list_n)

#mout the image
Mount_image(Nx,Ny,image)







