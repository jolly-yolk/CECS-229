#Name: Joshua Correa
#ID: 029196984
#Date: 04/02/2023

import image
import cv2
import os

class Vec:
    def __init__(self, contents = []):
        """
        Constructor defaults to empty vector
        INPUT: list of elements to initialize a vector object, defaults to empty list
        """
        self.elements = contents
        return
    
    def __abs__(self):
        """
        Overloads the built-in function abs(v)
        returns the Euclidean norm of vector v
        """
        
        return (self * self) ** (1/2)
        
    def __add__(self, other):
        """Overloads the + operator to support Vec + Vec
         raises ValueError if vectors are not same length
        """
        new_vector = []
        if len(self.elements) != len(other.elements):
            raise ValueError('vectors are not the same length')
            
        for element in range(len(self.elements)):
            new_vector.append(self.elements[element] + other.elements[element])
        
        return new_vector
    
    def __sub__(self, other):
        """
        Overloads the - operator to support Vec - Vec
        Raises a ValueError if the lengths of both Vec objects are not the same
        """
        new_vector = []
        if len(self.elements) != len(other.elements):
            raise ValueError('vectors are not the same length')
            
        for element in range(len(self.elements)):
            new_vector.append(self.elements[element] - other.elements[element])
        
        return new_vector
    
    
    def __mul__(self, other):
        """Overloads the * operator to support 
            - Vec * Vec (dot product) raises ValueError if vectors are not same length in the case of dot product
            - Vec * float (component-wise product)
            - Vec * int (component-wise product)
            
        """
        new_vector = []
            
        if type(other) == Vec: #define dot product
            #FIXME: IMPLEMENT
            if len(self.elements) != len(other.elements):
                raise ValueError('vectors are not the same length')
                
            for element in range(len(self.elements)):
                new_vector.append(self.elements[element] * other.elements[element])
            
            x = 0
            for i in range(len(new_vector)):
                x += new_vector.pop()
            return x
            
        elif type(other) == float or type(other) == int: #scalar-vector multiplication
            #FIXME: IMPLEMENT
            for element in range(len(self.elements)):
                new_vector.append(self.elements[element] * other)
                
        return new_vector
    
    def __rmul__(self, other):
        """Overloads the * operation to support 
            - float * Vec
            - int * Vec
        """
        new_vector = []
        for element in range(len(self.elements)):
                new_vector.append(self.elements[element] * other)
                
        return new_vector

    
    def __str__(self):
        """returns string representation of this Vec object"""
        return str(self.elements) # does NOT need further implementation

class Matrix:
    
    def __init__(self, rowsp = []):  
        self.rowsp = rowsp
        self.colsp = self._construct_cols(rowsp)
        
    def _construct_cols(self, rowsp):
        colsp = [] #create columns list
        x = [] #create temp column
        element = 0 #iterator for element in row
        
        if (len(rowsp) == 0): #if row is empty then so is column
            return colsp
        
        for i in range(len(rowsp[0])): #iterating in terms of a single row
            if (len(x) != 0): #if temp column has values then append it to column space and empty
                colsp.append(x)
                x = []
                element += 1 #iterate element when temp list is emptied
                
            for j in range(len(rowsp)): #iterating in terms of the entire row space
                x.append(self.rowsp[j][element]) #append the element in a specific row depending on the column
                
        colsp.append(x) #append left over temp column
        return colsp #return column space in the form of a 2D-list
    
    def set_col (self, j, u): #set new column
        if (len(u) != len(self.colsp[j - 1])): #if the colummn you are trying to set is not the same size as an arbitrary column then raise ValueError
            raise ValueError("Incompatible column length.")
        else:
            self.colsp[j - 1] = u #set column
            element = 0 #change the values in the row space so that they match
            for row in self.rowsp:
                row[j - 1] = u[element]
                element += 1
                
    def set_row (self, i, v): #set new row
        if (len(v) != len(self.rowsp[i - 1])): #if the row you are trying to set is not the same size as an arbitrary row then raise ValueError
             raise ValueError("Incompatible row length.")
        else:
            self.rowsp[i - 1] = v
            self.colsp = self._construct_cols(self.rowsp) #reconstruct columns based on new row
    
    def set_entry (self, i, j, x): #set new entry
        self.rowsp[i - 1][j - 1] = x #changes the value in the row space
        self.colsp[j - 1][i - 1] = x #changes the value in the column space
        
    def get_col (self, j): #get column
        return self.colsp[j - 1]
    
    def get_row (self, i): #get row
        return self.rowsp[i - 1]
    
    def get_entry (self, i, j): #get entry
        return self.rowsp[i - 1][j - 1]
    
    def col_space (self): #get column space
        return self.colsp
    
    def row_space (self): #get row space
        return self.rowsp
    
    def get_diag (self, k): #get diagnol values
        '''better info for this on juypter'''
        diag = [] #create diagnol list
        if (k == 0): #if k is 0 then return main diagnol
            for i in range(len(self.colsp)):
               diag.append(self.get_entry(i + 1, i + 1))
            
        elif (k > 0): #if k is positive return diagnol above main diagnol
            for i in range(len(self.colsp)):
                if (k == (len(self.colsp))):
                    break
                k += 1
                diag.append(self.get_entry(i + 1, k))
        else: #if k is negative return diagnol below main diagnol
            k = -k #make k negative first
            for i in range(len(self.colsp)):
                if (k == (len(self.colsp))):
                    break
                k += 1
                diag.append(self.get_entry(k, i + 1))
                
        return diag
            
    def __add__(self, other): #add two matrices
        matrix = [] #new matrix
        item = [] #temp
        if (len(self.colsp) != len(other.colsp)):
            raise ValueError('Incompatible Dimensions.')
            
        elif (len(self.rowsp) != len(other.rowsp)):
            raise ValueError('Incompatible Dimensions.')
        
        for i in range(len(self.rowsp) + 1): #since the dimensions are the same you only really have to worry about 1 matrix
            if (len(item) != 0): #if temp item has values then append to new matrix
                matrix.append(item)
                item = []
                
            if (i + 1 == len(self.rowsp) + 1): #end of loop if next break
                break
                
            for j in range(len(self.rowsp[i])): #iterate the elemenets in one row
                item.append(self.get_entry(i + 1, j + 1) + other.get_entry(i + 1, j + 1))
                
        return Matrix(matrix) #return a matrix object
                
    
    def __sub__(self, other): #subtracting two matrices (same as above but with subtraction on line 222)
        matrix = []
        item = []
        
        if (len(self.colsp) != len(other.colsp)):
            raise ValueError('Incompatible Dimensions.')
            
        elif (len(self.rowsp) != len(other.rowsp)):
            raise ValueError('Incompatible Dimensions.')
        
        for i in range(len(self.rowsp) + 1):
            if (len(item) != 0):
                matrix.append(item)
                item = []
                
            if (i + 1 == len(self.rowsp) + 1):
                break
                
            for j in range(len(self.rowsp[i])):
                item.append(self.get_entry(i + 1, j + 1) - other.get_entry(i + 1, j + 1))
                
        return Matrix(matrix)
        
    def __mul__(self, other): #multiply a matrix against different objects 
        matrix = [] #new matrix
        item = [] #temp item
        sum = 0 #sum for multiplying matrices
        if type(other) == float or type(other) == int: #Matrix * Scalar, pretty much the same as addition and subtraction but with multiplying the scalar (scalar doesn't change)

            for i in range(len(self.rowsp) + 1):
                if (len(item) != 0):
                    matrix.append(item)
                    item = []
                
                if (i + 1 == len(self.rowsp) + 1):
                    break
                
                for j in range(len(self.rowsp[i])):
                    item.append(self.get_entry(i + 1, j + 1) * other)
                
        elif type(other) == Matrix: #Matrix * Matrix
            if (len(self.colsp) != len(other.rowsp)):
                raise ValueError('Incompatible Dimensions.')
            
            for i in range(len(other.colsp) + 1): #iterate the other matrix column space
                if (len(item) != 0):
                    matrix.append(item)
                    item = []
                    
                if (i + 1 == len(other.colsp) + 1):
                    break
                    
                for j in range(len(self.rowsp) + 1): #iterate self row space
                    if (sum != 0): #if the sum is not 0 then one row of the new matrix has been calculated and must be appended
                        item.append(sum)
                        sum = 0
                        
                    if (j + 1 == len(self.rowsp) + 1):
                        break
                        
                    for x in range(len(self.rowsp[j])): #iterate 1 self row space
                        sum += self.rowsp[j][x] * other.colsp[i][x] #the multiplication of the other column space elemenent and self row space element
            #return is messy so if a better solution comes up I'll use it
            return Matrix(Matrix(matrix).col_space()) #use the list to make a matrix and then get the column space and then make that column space a new matrix
                    
        elif type(other) == Vec: #Matrix * Vector
            if (len(other.elements) != len(self.colsp)): #if the columns of the matrix and number of elements in the vector don't match
                raise ValueError('Incompatible Dimensions.')
            
            for i in range(len(self.colsp) + 1): #iterate the column of the matrix
                if (len(item) != 0):
                    matrix.append(item)
                    item = []
                    
                if (i + 1 == len(self.colsp) + 1):
                    break
                    
                for j in range(len(self.colsp[i])): #iterate an arbitrary column in the matrix
                    if (other.elements[i] == 0): #if the other element is 0 then just break because all results will be 0
                        break
                    item.append(other.elements[i] * self.colsp[i][j]) #if it isn't 0 then calculate
                
        else:
            print("ERROR: Unsupported Type.")
       
        return Matrix(matrix)
    
    def __rmul__(self, other): #pretty much the same as scalar multiplication above 
        matrix = []
        item = []
        if type(other) == float or type(other) == int: #Scalar * Matrix
            for i in range(len(self.rowsp) + 1):
                if (len(item) != 0):
                    matrix.append(item)
                    item = []
                
                if (i + 1 == len(self.rowsp) + 1):
                    break
                
                for j in range(len(self.rowsp[i])):
                    item.append(other * self.get_entry(i + 1, j + 1))
        else:
            raise ValueError('Unsupported Value Type.')
            
        return Matrix(matrix)
    
    '''these are given'''
    def __str__(self):
        """prints the rows and columns in matrix form """
        mat_str = ""
        for row in self.rowsp:
            mat_str += str(row) + "\n"
        return mat_str
                
    def __eq__(self, other):
        """overloads the == operator to return True if 
        two Matrix objects have the same row space and column space"""
        return self.row_space() == other.row_space() and self.col_space() == other.col_space()

    def __req__(self, other):
        """overloads the == operator to return True if 
        two Matrix objects have the same row space and column space"""
        return self.row_space() == other.row_space() and self.col_space() == other.col_space()
    

def image2matrix(filename):
    """
    takes a png file and returns a Matrix object of the pixels 
    INPUT: filename - the path and filename of the png file
    OUTPUT: a Matrix object with dimensions m x n, assuming the png file has width = n and height = m, 
    """
    #a single line of code should go here
    img = image.file2image(f'images/{filename}') #convert file to image
    if (image.isgray(img) == False):#the image is not gray:
        image_data = image.color2gray(img)#FIXME: make the image grayscale     
    return Matrix(image_data) #return matrix of image data


def matrix2image(img_matrix, path):
    """
    returns a png file created using the Matrix object, img_matrix
    INPUT: 
        * img_matrix - a Matrix object where img_matrix[i][j] is the intensity of the (i,j) pixel
        * path - the location and name under which to save the created png file 
    OUTPUT: 
        * a png file
    """
    return image.image2file(img_matrix.rowsp, path) #return matrix to image

def mix(img1, img2):
    """
    generates a set of 101 images that results from the convex mixing the given images
    INPUT: 
        - img1: string of path + name of first image 
        - img2: string of path + name of second image 
        
    OUTPUT: None (images are saved to the path given to matrix2image())
    """
    # todo
    x = image2matrix(img1) #make images matrices
    y = image2matrix(img2)
    x_percents = [] #empty percentage lists
    y_percents = []
    x_reverse = [] #empty reverse lists for seemless changing on video
    y_reverse = []
    convex_combos = [] #empty results list
    
    percent = 0.01 #these for loops use the scalar * matrix method to get the percentages of images
    for i in range(102):
        x_percents.append(percent * x)
        percent += 0.01
        
    percent = 0.01
    for i in range(102):
        y_reverse.append(percent * y)
        percent += 0.01
    
    percent = 1 #these for loops are different because they start at a higher percentage (white) while the other for loops start lower (black)
    for i in range(102):
        y_percents.append(y * percent)
        percent -= 0.01
        
    percent = 1
    for i in range(102):
        x_reverse.append(x * percent)
        percent -= 0.01
        
    for i in range(len(x_percents)): #gets the convex combinations using matrix + matrix
        convex_combos.append(x_percents[i] + y_percents[i])
    for i in range(len(x_percents)): #gets convex combination for seemless loop
        convex_combos.append(y_reverse[i] + x_reverse[i])
        
    for i in range(len(convex_combos)): #converts each matrix into an image
        matrix2image(convex_combos[i], f'frames/img{i}.png')

def make_video(images, outvid=None, fps=10, size=None, is_color=True, format="XVID"): #this function is given
    """
    Create a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """

    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = cv2.imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
    vid.release()
    return vid


'''^^^FUNCTIONS^^^'''

mix('img05.png', 'img14.png') #mix two images of your choose from provided folder of images
img_path = "C:\\Users\\corre\\OneDrive\\Documents\\School\\CECS 229\\Programming Assignment #5 (done)\\Extra Credit\\frames\\" #path where images you mixed are stored
vid_path = "C:\\Users\\corre\\OneDrive\\Documents\School\\CECS 229\\Programming Assignment #5 (done)\\Extra Credit\\video\\faces.mp4" #where the video will be stored

images = []  # Initializing empty list of image paths
for i in range(204):  # adding images img0.png - img203.png to the list
    file = f'{img_path}img{i}.png'
    images.append(file)

make_video(images, vid_path, format = "mp4v")  # creating video
print('Video Finished!')