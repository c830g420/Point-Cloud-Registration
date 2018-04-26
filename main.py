
from ReadFile import ReadFile
from ICP import ICP

def main() :

	p1 = ReadFile('./point_cloud_registration/pointcloud1.fuse')
	p2 = ReadFile('./point_cloud_registration/pointcloud2.fuse')

	icp = ICP(p1, p2)

	t = icp.iterativeClosestPoint()

	print(t)

if __name__ == '__main__':
	main()
