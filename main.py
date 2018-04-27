
from ReadFile import ReadFile
from ICP import ICP

def main() :

	p1 = ReadFile('./point_cloud_registration/pointcloud1.fuse')
	p2 = ReadFile('./point_cloud_registration/pointcloud2.fuse')

	icp = ICP(p1, p2)

	icp.setThres(0.1)

	icp.setTol(0.01)

	t = icp.iterativeClosestPoint()

	print('Rotation matrix')

	print(t[0])

	print('Translation vector')

	print(t[1])

	print('iteration No.')

	print(t[2])

if __name__ == '__main__':
	main()
