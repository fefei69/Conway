import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):

	"""returns a grid of NxN random values"""
	return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def update(fm,img, grid, N):

	# copy grid since we require 8 neighbors
	# for calculation and we go line by line
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N):

			# compute 8-neghbor sum
			# using toroidal boundary conditions - x and y wrap around
			# so that the simulaton takes place on a toroidal surface.
			total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
						grid[(i-1)%N, j] + grid[(i+1)%N, j] +
						grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
						grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

			# apply Conway's rules
			#cell is alive
			if grid[i, j] == ON:
				if (total < 2) or (total > 3):
					newGrid[i, j] = OFF
			#cell is dead
			else:
				#reproduction
				if total == 3:
					newGrid[i, j] = ON

	# update data
	img.set_data(newGrid)

	grid[:] = newGrid[:]
	return img,grid


def make_pattern(i, j, grid):

    # pat = np.zeros(6*5).reshape(6,5)
    # pat[1][2] = pat[1][3] = pat[1][4] = 255
    # pat[2][1] = pat[2][4] = 255 
    # pat[3][4] = 255
    # pat[4][4] = 255
    # pat[5][1] = pat[5][3]  = 255
    #pattern1
    pat = np.zeros(19*28).reshape(19,28)
    pat[2][1] = pat[3][1] = pat[4][1] = 255
    pat[1][2] = pat[4][2] = 255 
    pat[4][3] = 255
    pat[4][4] = 255
    pat[1][5] = pat[2][5]  = 255
    #pattern2
    pat[9][3] = pat[9][4] = pat[9][5] = 255
    pat[10][3] = 255
    pat[11][3] = pat[11][5] = 255
    pat[12][4] = pat[12][5] = 255
    #pattern3
    pat[15][2] = pat[15][5] = 255
    pat[16][1] = 255
    pat[17][1] = pat[17][5] = 255
    pat[18][1] = pat[18][2] = pat[18][3] = pat[18][4] = 255
    #pattern4
    pat[1][11] = pat[1][12] = 255
    pat[2][10] = pat[2][11] = pat[2][12] = pat[2][13] = 255
    pat[3][9] = pat[3][10] = pat[3][12] = pat[3][13] = 255
    pat[4][10] = pat[4][11] = 255
    #pattern5
    pat[8][12] = pat[8][13] = 255
    pat[9][13] = pat[9][14] = 255
    pat[10][10] = pat[10][13] = 255
    pat[11][12] = 255
    pat[12][9] = pat[12][10] = 255
    #pattern6 
    pat[13][26] = pat[13][27] = 255
    pat[14][26] = 255
    pat[15][24] = pat[15][25] = pat[15][26] = 255 
    grid[i:i+19, j:j+28] = pat

def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--eco', action='store_true', required=False)
    args = parser.parse_args()
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
	    N = int(args.N)
    grid = np.array([])
    # set animation update interval
    updateInterval = 5
    if args.eco:
        grid = np.zeros(N*N).reshape(N, N)
        make_pattern(50, 50, grid)
    else: 
	    grid = randomGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                frames = 10,
                                interval=updateInterval,
                                save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
	main()