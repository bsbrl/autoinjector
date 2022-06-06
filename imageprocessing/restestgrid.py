import matplotlib.pyplot as plt

#height = 1000
#width = 3000
nvals = []

class ResTest():
    def makePoints(self, width, height):
        drawpointsx = []
        drawpointsy = []
        for n in range(1,6):
            if n == 1:
                xval = (width/6)*n
                yval = height/2
                nvals.append(n)
                drawpointsx.append(xval)
                drawpointsy.append(yval)

            if n == 2:
                for k in range(1,3):
                    xval = (width/6)*n
                    yval = k*(height/3)
                    nvals.append(n)
                    drawpointsx.append(xval)
                    drawpointsy.append(yval)

            if n == 3:
                for j in range(1,4):
                    xval = (width/6)*n
                    yval = j*(height/4)
                    nvals.append(n)
                    drawpointsx.append(xval)
                    drawpointsy.append(yval)

            if n == 4:
                for k in range(1,3):
                    xval = (width/6)*n
                    yval = k*(height/3)
                    nvals.append(n)
                    drawpointsx.append(xval)
                    drawpointsy.append(yval)

            if n == 5:
                xval = (width/6)*n
                yval = height/2
                #nvals.append(n)
                drawpointsx.append(xval)
                drawpointsy.append(yval)

        self.drawpointsx = drawpointsx
        self.drawpointsy = drawpointsy

        """
        
        print(nvals)
        print(drawpointsx)
        print(drawpointsy)
        plt.scatter(drawpointsx,drawpointsy)
        v = [0, width, 0, height]
        plt.axis(v)
        plt.show()
        """
        

#if __name__ == '__main__':
#    points = ResTest()
#    points.makePoints(1000,3000)
