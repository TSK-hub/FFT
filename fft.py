import cmath
from cmath import pi

def FFT(poly):
    deg = len(poly)
    if deg == 1:
        return
    halfdeg = int(deg / 2)
    theta = 2 * pi / deg

    w = complex(1)
    RootOfUnity = complex(cmath.cos(theta), cmath.sin(theta))

    SubPoly1 = []
    SubPoly2 = []
    ind = 0

    for i in range(halfdeg): #subpolynomial 2개로 나눈다
        ind = 2 * i
        SubPoly1.append(poly[ind])
        SubPoly2.append(poly[ind+1])
        i += i

    FFT(SubPoly1)
    FFT(SubPoly2)

    for i in range(halfdeg):
        poly[i] = SubPoly1[i] + w * SubPoly2[i]
        poly[i + halfdeg] = SubPoly1[i] - w * SubPoly2[i] #sin앞의 부호가 바뀐다
        w *= RootOfUnity
    return poly

def invFFT(poly):
    deg = len(poly)
    if deg == 1:
        return
    halfdeg = int(deg / 2)
    #make conjugate complex number
    theta = -2 * pi / deg

    w = complex(1)
    RootOfUnity = complex(cmath.cos(theta), cmath.sin(theta))

    SubPoly1 = []
    SubPoly2 = []
    ind = 0

    for i in range(halfdeg):
        ind = 2 * i
        SubPoly1.append(poly[ind])
        SubPoly2.append(poly[ind+1])
        i += i

    invFFT(SubPoly1)
    invFFT(SubPoly2)

    for i in range(halfdeg):
        poly[i] = SubPoly1[i] + w * SubPoly2[i]
        poly[i + halfdeg] = SubPoly1[i] - w * SubPoly2[i]
        poly[i] /=2
        poly[i+halfdeg] /=2
        w *= RootOfUnity
    return poly

#polynomial multiplication using FFT
def MulFFT(poly1, poly2):
    deg1 = len(poly1)
    deg2 = len(poly2)
    #polynomial multiplication의 degree를 맞춰주기 위함
    for i in range(deg1):
        poly1.append(0)
    for i in range(deg2):
        poly2.append(0)
    deg1 = deg1 * 2
    deg2 = deg2 * 2

    tempPoly1 = poly1
    tempPoly2 = poly2

    #FFT
    tempPoly1 = FFT(tempPoly1)
    tempPoly2 = FFT(tempPoly2)
    mulpoly=[]

    #pointwise multiplication
    for i in range(deg1):
        mulpoly.append(tempPoly1[i] * tempPoly2[i])

    #inverse FFT
    mulpoly = invFFT(mulpoly)
    for i in range(deg1):
        mulpoly[i] = round(mulpoly[i].real,1)
    mulpoly.pop()
    return mulpoly

#polynomial multiplication
def MulPoly(poly1, poly2):
    deg1 = len(poly1)
    deg2 = len(poly2)
    deg = deg1 + deg2 - 1
    mulpoly=[]
    for i in range(deg):
        mulpoly.append(0)
    for i in range(deg1):
        for j in range(deg2):
            ind=(i+j) % deg
            mulpoly[ind] += poly1[i] * poly2[j]
    return mulpoly

#assume the number of coefficients should be power of 2
poly1=input("Coefficients of Poly1= ").split()
poly2=input("Coefficients of Poly2= ").split()
for i in range(len(poly1)):
    poly1[i]=float(poly1[i])
for i in range(len(poly2)):
    poly2[i]=float(poly2[i])


mulpoly2 = MulPoly(poly1, poly2)
mulpoly1 = MulFFT(poly1, poly2)

print("FFT Multiplication = ", mulpoly1)
print("Polynomial Multiplication = ", mulpoly2)
