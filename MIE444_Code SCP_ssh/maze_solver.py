def get_path(init):
        path1 = a_star_search.maze_solver(init, 1)
        path2 = a_star_search.maze_solver(init, 8)

        plt.close('fig')
        if len(path1) < len(path2):
                return path1
        else:
                return path2



maze = [[[3,3,0,0],[0,1,1,2],[0,0,1,2],[0,0,1,3],[],[0,0,0,3],[],[0,0,0,3]],
        [[0,1,1,2],[0,1,1,0],[],[0,0,1,4],[0,0,1,3],[2,1,2,2],[0,0,1,3],[4,1,0,2]],
        [[0,0,1,2],[],[1,0,0,0],[],[],[0,0,1,2],[],[0,0,1,2]],
        [[0,0,3,5],[0,0,1,4],[2,1,3,0],[3,0,2,0],[0,0,1,4],[0,0,3,5],[],[0,0,0,3]]]

#### UNIQUE POINTS ####
#u = [3,3,0,0]
#u = [1,1,0,0]
#u = [1,2,2,2]
#u = [0,1,2,4]
#u = [0,0,1,0]
#u = [0,1,2,3]
#u = [0,0,2,3]

while True:
        u_distances = [0,0,2,3] #read serial surrounding obstacles, [forward, right, back, left]

        u = [i//30 for i in u_distances] #convert cm to units of blocks
        k = u #store original u

        u.sort() #sort u in ascending order


        indices = []
        #store indices of maze positions with identical sensor readings
        for row, cols in enumerate(maze):
                for col,j in enumerate(cols):
                        j.sort()
                        if u == j:
                                indices += [[row,col]]

        if len(indices) == 1: #localized to one of the unique points in the maze
                [[row,col]] = indices #extract row and column indices
                orientation = maze[row][col] #left facing orientation stored in maze
                init = row*8 + col #get position index
                path = get_path(init) #call A* for path from localized point

                msg = ''


                if u == orientation:
                        #heading = 1 #'same'
                        # heading matches orientation for path
                        msg = 'forward'
                elif u == [orientation[1],orientation[2],orientation[3],orientation[0]]:
                        #heading = 2 #'ccw turn 90'
                        # heading is 90 deg orientation from path
                        msg = 'right'
                elif u == [orientation[2],orientation[3],orientation[0],orientation[1]]:
                        #heading = 3 #'ccw turn 180'
                        # heading is 180 deg orientation from path
                        msg = 'turn'
                elif u == [orientation[3],orientation[0],orientation[1],orientation[2]]:
                        #heading = 4 #'cw turn 90'
                        # heading is -90 deg orientation from path
                        msg = 'left'
                else:
                        print("ERROR")



                #serial send msg



