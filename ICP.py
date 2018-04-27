'''
    inspired by https://github.com/ClayFlannigan/icp
'''

import numpy as np
from sklearn.neighbors import NearestNeighbors

from ReadFile import ReadFile


class ICP:

    def __init__(self, f1, f2):

        # source 

        self.X = f1.cpts[:, :3]

        # destination

        self.Y = f2.cpts[:, :3]

        assert self.X.shape == self.Y.shape

        # get number of dimensions , default 3

        self.m = self.X.shape[1]

        # self.m = 3



        # make points homogeneous, copy them to maintain the originals

        self.src = np.ones((self.m+1, self.X.shape[0]))

        self.dst = np.ones((self.m+1, self.Y.shape[0]))

        self.src[:self.m, :] = np.copy(self.X.T)

        self.dst[:self.m, :] = np.copy(self.Y.T)

        self.neigh = NearestNeighbors(n_neighbors = 1)

        self.miter = 10

        self.tol = 0.1

        self.thres = 1



    def setIter(self, iter):

        '''

        set max number of iterations


        '''

        self.miter = iter



    def setTol(self, tolerance):

        '''

        set the tolerance


        '''

        self.tol = tolerance



    def setThres(self, thres):

        '''

        set max number of iterations


        '''

        self.thres = thres



    def best_fit_transform(self, A, B):

        '''

        Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions


        '''



        assert A.shape == B.shape



        m = A.shape[1]




        centroid_A = np.mean(A, axis=0)

        centroid_B = np.mean(B, axis=0)

        AA = A - centroid_A

        BB = B - centroid_B



        # rotation matrix

        H = np.dot(AA.T, BB)

        U, S, Vt = np.linalg.svd(H)

        R = np.dot(Vt.T, U.T)



        # special reflection case

        if np.linalg.det(R) < 0:

           Vt[m-1,:] *= -1

           R = np.dot(Vt.T, U.T)



        # translation

        t = centroid_B.T - np.dot(R, centroid_A.T)



        # homogeneous transformation

        T = np.identity(m+1)

        T[:m, :m] = R

        T[:m, m] = t



        return T , t




    def nearest_neighbor(self):

        '''

        Find the nearest (Euclidean) neighbor in dst for each point in src

        '''



        # assert src.shape == dst.shape



        self.neigh = NearestNeighbors(n_neighbors=1)

        self.neigh.fit(self.dst[:self.m, :].T)

        distances, indices = self.neigh.kneighbors(self.src[:self.m, :].T, return_distance=True)

        return distances.ravel(), indices.ravel()





    def iterativeClosestPoint(self, max_iterations = 50, tolerance = 0, threshold = 0 ) :

        '''

        The Iterative Closest Point method: finds best-fit transform that maps points A on to points B


        '''

        max_iterations = self.miter

        tolerance = self.tol

        print('Tolerance :')

        print(tolerance)

        threshold = self.thres

        print('Threshold :')

        print(threshold)



        prev_error = 0



        for i in range(max_iterations) :

            # find the nearest neighbors between the current source and destination points

            distances, indices = self.nearest_neighbor()

            

            # compute the transformation between the current source and nearest destination points
            

            T, _ = self.best_fit_transform(self.src[:self.m, :].T, self.dst[:self.m, indices].T)



            # update the current source

            self.src = np.dot(T, self.src)



            # check error



            mean_error = np.mean(distances)

            print('Current error: ')
            
            print(mean_error)

            if mean_error < threshold :

                break


            if np.abs(prev_error - mean_error) < tolerance :

                break

            prev_error = mean_error



        T, t = self.best_fit_transform(self.X, self.src[:self.m, :].T)



        return T[:self.m, :self.m], t, i


