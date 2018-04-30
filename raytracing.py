###### modificar os valores de d_U e d_V pois eles estão em zero

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
    d_U = (left +  (right - left) * (Nx + 0.5)/Nx)     ##### d_U,d_V values ​​of how much the pixel should move to the point (0,0) #######
    d_V = (bottom + (top - bottom) * ( Ny + 0.5)/Ny)
    #d_U = 0
    #d_V = 0
    for i in range(0,Nx-1,1):
        for j in range(0,Ny-1,1):
            U = (left +  (right - left) * (i + 0.5)/Nx) + d_U
            V = (bottom + (top - bottom) * ( j + 0.5)/Ny) + d_V
            Matrix[i][j] = (U,V)
    Transformation(T_matrix,Matrix,d_U,d_V)


##### make the linear transformation of the matrix 2D ####################
def Transformation(T_matrix,Matrix,d_U,d_V):
    for i in range(0,Nx-1,1):
        for j in range(0,Ny-1,1):
            aux1 = (Matrix[i][j][0] * T_matrix[0][0]) + (Matrix[i][j][0] * T_matrix[0][1])
            aux2 = (Matrix[i][j][1] * T_matrix[1][0]) + (Matrix[i][j][1] * T_matrix[1][1])
            print(d_U)
            print(d_V)
            Matrix[i][j] = (aux1- d_U ,aux2 - d_V)



#####Calculate ray in ortographic case ##############
def Orto(Vector_e,Vector_u,Vector_v,Vector_w,Nx,Ny,Matrix):
   direct = np.dot(Vector_w,-1)
   for i in range(0,Nx-1):
           for j in range(0,Ny-1):
               scalar_u = np.dot(Vector_u,Matrix[i][j][0])
               scalar_v = np.dot(Vector_v,Matrix[i][j][1])
               origin = Vector_e + scalar_u + scalar_v
               Matrix[i][j] = (origin,direct)


####Calculate light rays in ortographic case ###########
def Orto_Lamp(lamp,Vector_lamp_u,Vector_lamp_v,Vector_lamp_w,Nx,Ny,Matrix,Matrix_lamp):
   direct = np.dot(Vector_lamp_w,-1)
   for i in range(0,Nx-1):
           for j in range(0,Ny-1):
               scalar_u = np.dot(Vector_lamp_u,Matrix[i][j][0])
               scalar_v = np.dot(Vector_lamp_v,Matrix[i][j][1])
               origin = Vector_e + scalar_u + scalar_v
               Matrix_lamp[i][j] = (origin,direct)




###calculates whether the ray touches the sphere#########
def Delta(Matrix, spheres, nx, ny, image,lamp,lamp_intense,Matrix_lamp):
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
                             point = e_origin + (direct* menor)      ##### calculate p(t) and append in a list of points ######
                             vector_n =  point -sphere[0] / Norma(point-sphere[0])
                             vector_l = lamp - point / Norma(lamp - point)
                             vector_h = Matrix_lamp[i,j][1] + vector_l  / Norma(Matrix_lamp[i,j][1] + vector_l)
                             list_aux.append([menor, sphere[2]])
                        else:
                            list_aux.append(["black","black"])



                    minor_2 = 50000000000000000;
                    color = [0,0,0]
                    La = [0,0,0]
                    Ba = [0,0,0]
                    for elem in list_aux:
                        if(elem[0]!="black"):
                            if(elem[0]<minor_2):
                                minor_2 = elem[0]
                                color = elem[1]
                                #print(color)
                                La = Lambert(vector_n,vector_l,color,lamp_intense)
                                #print(La)
                                Ba = Blinpong(La,vector_h,vector_n)

                    image[i][j] = Ba




#function that calculates lambert shading
def Lambert(Vector_n,Vector_l,color,l_intense):
   Lred = int(color[0] * l_intense * max(0,np.dot(Vector_n,Vector_l)) + (environment_color[0] * environment_intense))
   Lgreen = int(color[1] * l_intense * max(0,np.dot(Vector_n,Vector_l))+ (environment_color[1] * environment_intense))
   Lblue  = int(color[2] * l_intense * max(0,np.dot(Vector_n,Vector_l))+ (environment_color[2] * environment_intense))
   return [Lred,Lgreen,Lblue]


#function that calculates Blinn Phong shading with environment lighting
def Blinpong(La,vector_h,vector_n):
    Bred = int(La[0] + (environment_color[0] * environment_intense) * max(0,np.dot(vector_n,vector_h))**pot)
    Bgreen = int(La[1] + (environment_color[1] * environment_intense) * max(0, np.dot(vector_n, vector_h))**pot)
    Bblue = int(La[2]  + (environment_color[2] * environment_intense) * max(0, np.dot(vector_n, vector_h))**pot)
    return [Bred,Bgreen,Bblue]




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
spheres = [[(-4, 0, 0), 2, (90, 250, 250)], [(2,-1,2), 3, (100,250,100)]]

###### lighting variables #######
Matrix_lamp = Building_Matrix(Nx,Ny)
lamp = [-10,20,30]
lamp_intense = 0.02
lamp = np.asarray(lamp)
lamp_vector_w = [0,0,0]
norma_lamp = Norma(lamp)
Building_Vector_w(lamp_vector_w,lamp,norma_lamp)
lamp_vector_t = Building_Vector_T(lamp_vector_w)
lamp_vector_u = Building_Vector_U(lamp_vector_t,lamp_vector_w)
lamp_vector_v = np.cross(lamp_vector_u,lamp_vector_w)

###### environment variables #####
environment_color = [255,0,0]
environment_intense = 0.09
pot = 0.15


######Transformation Matrix variables ########
T_matrix = [(0.5,0),(0,0.5)]


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
Orto_Lamp(lamp,lamp_vector_u,lamp_vector_v,lamp_vector_w,Nx,Ny,Matrix,Matrix_lamp)
#####transfor into a numpy Matrix ########
Matrix = Transform_into_npMatrix(Matrix)
Matrix_lamp = Transform_into_npMatrix(Matrix_lamp)

Delta(Matrix, spheres, Nx, Ny, image,lamp,lamp_intense,Matrix_lamp)

#mout the image
Mount_image(Nx,Ny,image)







