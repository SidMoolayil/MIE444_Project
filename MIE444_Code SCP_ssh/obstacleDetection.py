import cv2
import matplotlib.pyplot as plt
import numpy as np
import maze
import serial_comm
import a_star_search

def obstacle_region(image):
    for i,r in enumerate(image):
        #print(np.size(r))
        for j,c in enumerate(r):
            #print(np.size(c))
            [b,g,r] = c
            #print((b/2)-(r/2))
            if (abs((b/2)-(r/2))>10) or (abs((b/2)-(g/2))>10):
                #print("true")
                image[i][j] = np.array([0,100,100])

    mask1 = cv2.inRange(image, np.array([0,100,100]), np.array([0,100,100]))

    return mask1

def wb_region(image):
    # blacks
    lower1 = np.array([0, 0, 0])
    upper1 = np.array([150, 150, 150])

    # whites
    lower2 = np.array([151, 151, 151])
    upper2 = np.array([255, 255, 255])

    mask1 = cv2.inRange(image, lower1, upper1)
    mask2 = cv2.inRange(image, lower2, upper2)

    return [mask1, mask2]

def obstacle_detect(points, image):
    obstacle = obstacle_region(image)

    #cv2.imshow("mask", obstacle)
    #cv2.waitKey(0)

    for i,p in enumerate(points):
        if obstacle[int(p[1])][int(p[0])]:
            #print(p[1],p[0])
            return True

    return False

def collect_ground(points, image):
    check = [-1 for i in points]
    for i,point in enumerate(points):
        [black, white] = wb_region(image)
        if black[int(point[1])][int(point[0])]:
            #print(p[1],p[0])
            check[i] = 1
        elif white[int(point[1])][int(point[0])]:
            check[i] = 0
        else:
            print("ISSUE HERE")
        #colour = image[int(point[0])][int(point[1])]
        #print(i,colour)
        #if sum(colour)>150*3:
        #    check[i] = 0
        #else:
        #    check[i] = 1
    matrix = np.resize(np.array(check),[4,4])
    return matrix

def ismember(a,b):
    #a = a.flatten()
    for k in range(4):
        b = np.rot90(b)
        for i in range(13):
            for j in range(29):
                a_i = np.array([[a[i][j],a[i][j+1],a[i][j+2],a[i][j+3]],
                               [a[i+1][j],a[i+1][j+1],a[i+1][j+2],a[i+1][j+3]],
                               [a[i+2][j],a[i+2][j+1],a[i+2][j+2],a[i+2][j+3]],
                               [a[i+3][j],a[i+3][j+1],a[i+3][j+2],a[i+3][j+3]]])
                if np.array_equal(b,a_i):
                    return [i,j,k]
        '''for i in a:
            index = np.where(b==i)[0]
            if index.size == 0:
                yield 0
            else:
                yield index'''

def f(A, gen_obj):
    my_array = np.arange(len(A))
    for i in my_array:
        my_array[i] = gen_obj.next()
    return my_array

def get_heading(next_node,init):
    if abs(next_node - init) == 1:
        if next_node < init:
            heading = 0  # east
        else:
            heading = 2  # west
    else:
        if next_node > init:
            heading = 1  # south
        else:
            heading = 3  # north
    return heading

def get_path(init):
    path1 = a_star_search.maze_solver(init, 1)
    path2 = a_star_search.maze_solver(init, 8)

    plt.close('fig')
    if len(path1) < len(path2):
        path = a_star_search.maze_solver_disp(init, 1)
    else:
        path = a_star_search.maze_solver_disp(init, 8)
    # print(path)
    # location[2] is orientation relative to maze, 0==E,1==S,2==W,3==N
    return path

def path_planning(image, maze):
    resize = 500

    img = np.copy(image)
    #print(len(img),len(img[0]))

    # set of points in image coordinates defined as safe distance in world coordinates
    points = np.array([[838,1894],[1297,1894],[1821,1894],[2380,1894],[725,2211],[1268,2211],[1867,2211],[2448,2211],[560,2697],[1202,2697],[1919,2697],[2606,2697],[357,3397],[1147,3397],[1935,3397],[2786,3397]])

    for point in points:
        point[0] = point[0]*resize/len(img[1])
        point[1] = point[1]*resize/len(img)
    points = np.rint(points)
    #print(points)

    img = cv2.resize(img, [resize, resize])
    image = cv2.resize(image, [resize, resize])

    if not obstacle_detect(points, img):
        matrix = collect_ground(points, image)
        #print(matrix)
        plt.imshow(matrix, cmap='Greys', interpolation='nearest')
        plt.show()

        location = ismember(maze, matrix)
        #print(location)
        init = (location[0]//4)*8 + location[1]//4
        #print(init)

        path = get_path(init)

        orientation = location[2]
        heading = get_heading(path[1],init)

        #print(orientation, heading)
        if orientation == heading:
            print("GO FORWARD")
            serial_comm.send_command = b'forward'
        elif abs(orientation - heading) == 2:
            print("TURN 180 deg")
            serial_comm.send_command = b'full turn'
        elif (heading > orientation) or (heading == 3 and orientation == 0):
            print("TURN CCW")
            serial_comm.send_command = b'ccw'
        else:
            print("TURN CW")
            serial_comm.send_command = b'cw'

    else:
        print("TURN or KEEP TURNING until view is clear")
        serial_comm.send_command = b'continue rotate'


if __name__ == "__main__":
    image_path = "/Users/sidhanthmoolayil/Desktop/MIE444_Code/IMG_8152.jpg"  # IMG_8149.jpg" #IMG_8154.jpg" #IMG_8153.jpg"
    image = cv2.imread(image_path)

    path_planning(image)
    cv2.waitKey(0)