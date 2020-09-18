from PIL import Image
import  numpy as np
import time

def applythreshold(arry1_in):
    arry1=arry1_in.copy()
    arry1 [arry1 <= 128] = 1
    arry1 [arry1 > 128] = 0
    return arry1

# problems=["Basic Problem B-01","Basic Problem B-02","Basic Problem B-03","Basic Problem B-04","Basic Problem B-05","Basic Problem B-06","Basic Problem B-07","Basic Problem B-08",
#           "Basic Problem B-09","Basic Problem B-10"]
problems=["Basic Problem B-10"]

for problem in problems:
    dir ="C:/Java/cs7637/Project-Code-Python/Project-Code-Python/Problems/Basic Problems B/" + problem + "/"
    print("problem {}  BEGIN ============".format(dir))

    imga = Image.open(dir+"C.png")
    imga_bw_arry = np.asarray(imga.convert('L'), dtype=np.int32)
    imga_bw_arryc = imga_bw_arry.copy()
    imga_bw_arryc = applythreshold(imga_bw_arryc)

    labels={}
    d = imga_bw_arryc.copy()
    # print(d.shape)
    np.savetxt("d.txt", d, fmt='%d')
    labels[0]=d;

    shape_ind=2
    shape_fnd=0
    shape_set = 0
    any_shape = 1

    while any_shape == 1:
        any_shape = 0
        print(shape_ind)
        shape1 = np.zeros((d.shape[0], d.shape[1]), dtype=int)

        #reset vars
        lx = 0
        ly = 0
        fx = 0
        fy = 0
        shape_fnd = 0
        shape_set = 0

        for x in range(d.shape[0]):
            # print(d[x,:])
            for y in range(d.shape[1]):
                # print("x {} y {} pixel {}".format(x,y,d[x,y]))
                if d[x,y]==0:
                    pass
                if d[x,y]==1 \
                        and ( (d[x+1,y]==1 and d[x-1,y]==0) or (d[x+1,y]==0 and d[x-1,y]==1) or d[x+1,y]==d[x-1,y] ) \
                        and ( (d[x,y-1] == 0 and d[x,y+1] == 1) or (d[x,y-1] == 1 and d[x,y+1] == 0 ) or d[x,y-1] == d[x,y+1] ) \
                        and shape_fnd==0:
                    print("shape_ind {} d[x+1,y] {} ,d[x,y-1] {} ,d[x-1,y+1] {}".format(shape_ind,d[x+1,y],d[x,y-1],d[x-1,y+1]))

                    any_shape = 1
                    shape1[x,y]=1
                    fx=x
                    fy=y
                    shape_fnd=1
                    d[x,y]=shape_ind
                    shape_set = 1
                    x1=x
                    y1=y+1

                    #first look right
                    while d[x1,y1] != 0 and y1+1 < d.shape[1] - 1:
                        # print("first move right same x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format(x,y,x1,y1,d[x1,y1],d[x1-1,y1] , d[x1+1,y] , d[x1,y1-1] , d[x1,y1+1]))
                        if d[x1,y1-1]==shape_ind and d[x1,y1]==1 \
                                and ( (d[x1-1,y1]==0 and d[x1+1,y]==1) or (d[x1-1,y1]==1 and d[x1+1,y1]==0) or d[x1-1,y1]==d[x1+1,y1] ):
                            shape1[x1,y1]=1
                            d[x1, y1] = shape_ind
                            shape_set = 1
                            # print("set shape {}, increment y1 {}".format(shape1[x1,y1-1],y1))
                            # np.savetxt("shape1.txt", shape1, fmt='%d')
                            # np.savetxt("d_aft.txt", d, fmt='%d')
                        # time.sleep(1/10)
                        y1 = y1 + 1

                    # print("first move right y1",y1)
                    #move to next line
                    while d[x1,y1-1] == shape_ind:
                        if d[x1+1,y1-1] == 1:
                            x=x1+1
                            y=y1
                            # print("first shift to next line in shape","x",x,"y1",y1,"d",d[x,y1])
                            # break
                        y1=y1-1

                    while x <= d.shape[0] and shape_set != 0:
                        # print("shape_set=0 {}".format(shape_set))
                        shape_set=0

                        #look right next line
                        shape1[x, y] = 1
                        d[x, y] = shape_ind
                        x1 = x
                        y1 = y + 1
                        while d[x1, y1] != 0 and y1 + 1 < d.shape[1] - 1:
                            # print("second move right enter x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format(x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                            if d[x1, y1 - 1] == shape_ind and d[x1, y1] == 1 \
                                    and ((d[x1 - 1, y1] in [0,shape_ind] and d[x1 + 1, y1] == 1) or (d[x1 - 1, y1] in [1,shape_ind] and d[x1 + 1, y1] == 0) or d[x1 - 1, y1] == d[x1 + 1, y1]):
                                shape1[x1, y1] = 1
                                d[x1, y1] = shape_ind
                                shape_set = 1
                                # print("set shape {}, y1 {}".format(shape1[x1, y1 - 1], y1))
                                # np.savetxt("shape1.txt", shape1, fmt='%d')
                                # np.savetxt("d_aft.txt", d, fmt='%d')
                            # else:
                            #     print("second move right exit x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format(x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1],d[x1, y1 + 1]))
                            # time.sleep(1 / 10)
                            y1 = y1 + 1

                        #look left
                        shape1[x, y] = 1
                        d[x, y] = shape_ind
                        x1 = x
                        y1 = y - 1
                        while d[x1, y1] != 0 and y1 - 1 > 0:
                            # print("first move left enter x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y1] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format( \
                            #         x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                            if d[x1, y1] == 1 \
                                    and ((d[x1 - 1, y1] in [0,shape_ind] and d[x1 + 1, y1] == 1) or (d[x1 - 1, y1] in [1,shape_ind] and d[x1 + 1, y1] == 0) or (d[x1 - 1, y1] == shape_ind and d[x1 + 1, y1] in [0,1]) or (d[x1 + 1, y1] == d[x1 - 1, y1])):
                                shape1[x1, y1] = 1
                                d[x1, y1] = shape_ind
                                shape_set = 1
                                # print("set shape {}, y1 {}".format(shape1[x1, y1], y1))
                                # np.savetxt("shape1.txt", shape1, fmt='%d')
                                # np.savetxt("d_aft.txt", d, fmt='%d')
                            # else:
                            #     print("first move left exiting same x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y1] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format( x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                            # time.sleep(1 / 10)
                            y1 = y1 - 1


                        # print("first move left y1",y1)
                        #move to next line
                        while d[x1,y1+1] == shape_ind:
                            if d[x1+1,y1+1] == 1:
                                x=x1+1
                                y=y1
                                # print("second shift to next line in shape","x",x,"y1",y1,"d",d[x,y1])
                                # break
                            y1=y1+1

                    # print(x,y,fx,fy)
                    lx = x
                    ly = y

        #go up the side to complete the shape

        x1=lx
        y1=ly
        # print(x1,y1,fx,fy)

        shape_set = 0

        # move up lines
        while d[x1,y1] == shape_ind:
            if d[x1-1,y1] == shape_ind:
                # print("shape ind",d[x1-1,y1])
                x1=x1-1
                y1=ly
                # print(x1,y1,d[x1,y1])
            elif d[x1-1,y1] == 0:
                # print("0", y1,d[x1 - 1, y1])
                y1=y1-1
            elif d[x1-1,y1] == 1:
                # print("1", x1, d[x1 - 1, y1])
                r=x1-1
                c=y1
            y1=y1-1

        shape_set=1
        # print(r, c,d[r,c],fx,fy,shape_set)
        # for x in range (r,fx,-1):
        #     for y in range(max(c,fy),min(c,fy),-1):
        #         # print("d[x,y]",d[x,y])

        x=r
        y=c

        while x >= fx and shape_set != 0:
            shape_set = 0
            # look right next line
            shape1[x, y] = 1
            d[x, y] = shape_ind
            x1 = x
            y1 = y + 1
            while d[x1, y1] != 0 and y1 + 1 < d.shape[1] - 1:
                # print("second move right enter x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format(x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                if d[x1, y1 - 1] == shape_ind and d[x1, y1] == 1 \
                        and ((d[x1 - 1, y1] == 0 and d[x1 + 1, y1] == shape_ind) or (
                        d[x1 - 1, y1] == 1 and d[x1 + 1, y1] in [0,shape_ind]) or (d[x1 - 1, y1] == shape_ind and d[x1 + 1, y1] == 0 )
                             or d[x1 - 1, y1] == d[x1 + 1, y1]):
                    shape1[x1, y1] = 1
                    d[x1, y1] = shape_ind
                    shape_set = 1
                    # print("set shape {}, x1,y1 {},{}".format(shape1[x1, y1 - 1], x1,y1))
                    # np.savetxt("shape1.txt", shape1, fmt='%d')
                    # np.savetxt("d_aft.txt", d, fmt='%d')
                # else:
                    # print("second move right exit x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format(x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1],d[x1, y1 + 1]))
                # time.sleep(1 / 10)
                y1 = y1 + 1
                # print("after move right x1,y1 {},{} d[x1,y1] {}".format(x1, y1, d[x1, y1]))

            #look left
            x1 = x
            y1 = y
            # print("d[x1,y1]",d[x1,y1])
            while d[x1, y1] != 0 and y1 - 1 > 0:
                # print(
                #     "first move left enter x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y1] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format( \
                #         x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                if d[x1, y1] == 1 \
                        and ((d[x1 - 1, y1] in [0, shape_ind] and d[x1 + 1, y1] == shape_ind) or (
                        d[x1 - 1, y1] == 1 and d[x1 + 1, y1] in [0, shape_ind]) or (
                                     d[x1 - 1, y1] == shape_ind and d[x1 + 1, y1] in [0, 1]) or (
                                     d[x1 + 1, y1] == d[x1 - 1, y1])):
                    shape1[x1, y1] = 1
                    d[x1, y1] = shape_ind
                    shape_set = 1
                    # print("set shape {}, x1 {} y1 {}".format(shape1[x1, y1], x1, y1))
                    # np.savetxt("shape1.txt", shape1, fmt='%d')
                    # np.savetxt("d_aft.txt", d, fmt='%d')
                # else:
                    # print("first move left exiting same x {} y {} x1 {} y1 {} d[x1,y1] {} d[x1-1,y1] {} d[x1+1,y1] {} d[x1,y1-1] {} d[x1,y1+1] {} ".format( x, y, x1, y1, d[x1, y1], d[x1 - 1, y1], d[x1 + 1, y1], d[x1, y1 - 1], d[x1, y1 + 1]))
                    # time.sleep(1 / 10)
                y1 = y1 - 1
                # print("after move left x1,y1 {},{} d[x1,y1] {}".format(x1,y1,d[x1,y1]))

            # move up next line
            while d[x1, y1 + 1] == shape_ind:
                if d[x1 - 1, y1 + 1] == 1:
                    x = x1 - 1
                    y = y1
                    # print("second shift to next line in shape","x",x,"y",y,"d",d[x,y])
                y1 = y1 + 1

        np.savetxt("shape" + str(shape_ind) + ".txt", shape1, fmt='%d')
        np.savetxt("d_aft" + str(shape_ind) + ".txt", d, fmt='%d')
        labels[shape_ind]= shape1

        shape_ind = shape_ind + 1


    np.savetxt("d_aft.txt", d, fmt='%d')

    print ("================ end of problem ============ {} END ".format(problem))

