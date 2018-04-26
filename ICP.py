import numpy as np
from sklearn.neighbors import NearestNeighbors

from ReadFile import ReadFile


class ICP:

    def __init__(self, f1, f2):

        # source 
        self.X = f1.cpts

        # destination
        self.Y = f2.cpts

        assert self.X.shape == self.Y.shape

        # get number of dimensions
        self.m = self.X.shape[1]


    # def homogenize(self):

        # make points homogeneous, copy them to maintain the originals

        self.src = np.ones((self.m+1, self.X.shape[0]))

        self.dst = np.ones((self.m+1, self.Y.shape[0]))

        self.src[:self.m, :] = np.copy(self.X.T)

        self.dst[:self.m, :] = np.copy(self.Y.T)

        self.neigh = NearestNeighbors(n_neighbors=1)

        # return src, dst






    def best_fit_transform(self, A, B):

        '''

        Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions

        Input:

          A: Nxm numpy array of corresponding points

          B: Nxm numpy array of corresponding points

        Returns:

          T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B

          R: mxm rotation matrix

          t: mx1 translation vector

        '''



        assert A.shape == B.shape



        # get number of dimensions

        m = A.shape[1]



        # translate points to their centroids

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

        t = centroid_B.T - np.dot(R,centroid_A.T)



        # homogeneous transformation

        T = np.identity(m+1)

        T[:m, :m] = R

        T[:m, m] = t



        return T #, R, t





    def nearest_neighbor(self):

        '''

        Find the nearest (Euclidean) neighbor in dst for each point in src

        Output:

            distances: Euclidean distances of the nearest neighbor

            indices: dst indices of the nearest neighbor

        '''



        # assert src.shape == dst.shape



        self.neigh = NearestNeighbors(n_neighbors=1)

        self.neigh.fit(self.dst[:self.m, :].T)

        distances, indices = self.neigh.kneighbors(self.src[:self.m, :].T, return_distance=True)

        return distances.ravel(), indices.ravel()





    def iterativeClosestPoint(self, max_iterations=20, tolerance=0.001):

        '''

        The Iterative Closest Point method: finds best-fit transform that maps points A on to points B

        Input:

            A: Nxm numpy array of source mD points

            B: Nxm numpy array of destination mD point

            init_pose: (m+1)x(m+1) homogeneous transformation

            max_iterations: exit algorithm after max_iterations

            tolerance: convergence criteria

        Output:

            T: final homogeneous transformation that maps A on to B

            distances: Euclidean distances (errors) of the nearest neighbor

            i: number of iterations to converge

        '''



        # assert self.X.shape == self.Y.shape



        # get number of dimensions

        # m = A.shape[1]



        # make points homogeneous, copy them to maintain the originals

        # src = np.ones((self.m+1, self.X.shape[0]))

        # dst = np.ones((self.m+1, self.Y.shape[0]))

        # src[:m,:] = np.copy(self.X.T)

        # dst[:m,:] = np.copy(self.Y.T)



        prev_error = 0



        for i in range(max_iterations):

            # find the nearest neighbors between the current source and destination points

            distances, indices = self.nearest_neighbor()

            

            # compute the transformation between the current source and nearest destination points
            

            T = self.best_fit_transform(self.src[:self.m,:].T, self.dst[:self.m,indices].T)



            # update the current source

            self.src = np.dot(T, self.src)



            # check error

            mean_error = np.mean(distances)

            if np.abs(prev_error - mean_error) < tolerance:

                break

            prev_error = mean_error



        # calculate final transformation

        T = self.best_fit_transform(self.X, self.src[:self.m,:].T)



        return T, distances, i


