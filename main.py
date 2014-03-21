import cv2
import numpy.random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def preview(img):
    cv2.imshow("orig", img)
    cv2.waitKey(0)

def trial_add(truth, img):
    y,x,c = img.shape
    rx, ry = np.random.ranf((2,))
    ix = int(rx*x)
    iy = int(ry*y)
    color = truth[iy,ix,:] + (np.random.ranf((3,))-.5) * .2
    k_size = np.random.randint(3, 150)
    test = np.copy(img)
    sig = (iy-k_size, iy+k_size, ix-k_size, ix+k_size)
    alpha = np.random.ranf()
    test[sig[0]:sig[1], sig[2]:sig[3], :] *= (1-alpha) 
    test[sig[0]:sig[1], sig[2]:sig[3], :] += alpha * color
    return test

def error(canvas, orig):
    x = (canvas-orig)
    return np.sum(x*x)

img = cv2.imread("japan1.jpg")
print img

img = cv2.resize(img, (img.shape[1]/2, img.shape[0]/2))
print np.max(img)
img = img/255.0

canvas = np.zeros_like(img).astype(float)
canvas = np.random.ranf(img.shape).astype(float)
canvas = np.ones_like(img).astype(float)
print canvas[0,0,0]

on_iter = 0
prior_error = error(canvas, img)
errors = []
times = []
while True:
    on_iter += 1
    test = trial_add(img, canvas)
    cur_error = error(test, img)
    if on_iter % 100 == 0:
        print cur_error, prior_error
        print on_iter
    if  cur_error <= prior_error:
        prior_error = cur_error
        errors.append(prior_error)
        times.append(times)
        canvas = test
    if on_iter % 1000 == 0:
        cv2.imwrite("imgLS/"+str(on_iter)+".png", canvas*255)
        #plt.plot(times, errors)
        #plt.show()
        #preview(canvas)
        print "going to next"

