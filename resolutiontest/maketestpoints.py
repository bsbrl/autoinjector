import matplotlib.pyplot as plt


length = 4000
width = 2000
centerlength = length/2
centerwidth = width/2

dist = 500
pointcloudx = [centerlength]
pointcloudy = [centerwidth]
for i in range(0,1):
    for k in range(0,8):
        if k == 0:
            pointx = centerlength + dist 
            pointy = centerwidth + dist 
        if k == 1:
            pointx = centerlength - dist 
            pointy = centerwidth + dist 
        if k == 2:
            pointx = centerlength + dist 
            pointy = centerwidth - dist
        if k == 3:
            pointx = centerlength - dist 
            pointy = centerwidth - dist
        if k == 4:
            pointx = centerlength  
            pointy = centerwidth + 2*dist 
        if k == 5:
            pointx = centerlength  
            pointy = centerwidth - 2*dist 
        if k == 6:
            pointx = centerlength + 2*dist 
            pointy = centerwidth
        if k == 7:
            pointx = centerlength - 2*dist 
            pointy = centerwidth
        pointcloudx.append(pointx)
        pointcloudy.append(pointy)
    dist += 500
print(pointcloudx)

plt.scatter(pointcloudx,pointcloudy)
plt.ylabel('some numbers')
plt.show()