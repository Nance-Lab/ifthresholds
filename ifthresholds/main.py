import skimage
import skimage.io as sio
from skimage.color import rgb2gray
from skimage.measure import regionprops
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import try_all_threshold
from skimage.morphology import remove_small_objects
from skimage.measure import label
from scipy.ndimage.morphology import binary_fill_holes
import csv

def img_score(filepath, man_img, man_count):
    imagefile = sio.imread(filepath)
    imgman = sio.imread(man_img)
    img = rgb2gray(imagefile)
    # 8 threshold
    # original = img
    li = skimage.filters.threshold_li(img)
    minimum = skimage.filters.threshold_minimum(img)
    triangle = skimage.filters.threshold_triangle(img)
    isodata = skimage.filters.threshold_isodata(img)
    mean = skimage.filters.threshold_mean(img)
    otsu = skimage.filters.threshold_otsu(img)
    yen = skimage.filters.threshold_yen(img)
    # while loop for 7 methods
    # img_list = []
    threshold = [li, minimum, triangle, isodata, mean, otsu, yen]
    scorelist = []
    
    for i in range (0,7):  
        score =[]
        thre = threshold[i]
        binary = img > thre
        #img_list.append(binary)
        clean_img = remove_small_objects(binary)  # remove small objects
        lab_img = label(clean_img)  # label images to be seen as one or multiple object(s)
        lab_imgm = label(imgman)
        # count method
        props = regionprops(lab_img)
        x = np.zeros(len(props))
        y = np.zeros(len(props))
        area = np.zeros(len(props))
        perim = np.zeros(len(props))
        #intensity = np.zeros(len(props))
        counter = 0
        for prop in props:
            x[counter] = prop.centroid[0]
            y[counter] = prop.centroid[1]
            area[counter] = prop.area
            perim[counter] = prop.perimeter
            #intensity[counter] = prop.mean_intensity
            counter += 1
        countscore = np.abs((counter-man_count)/man_count)*100
        countmethod = ('count method', countscore)
        score.append(countmethod)
        
        # area method
        propsm = regionprops(lab_imgm)
        xm = np.zeros(len(propsm))
        ym = np.zeros(len(propsm))
        aream = np.zeros(len(propsm))
        perimm = np.zeros(len(propsm))
        counterm = 0
        for prop in propsm:
            xm[counterm] = prop.centroid[0]
            ym[counterm] = prop.centroid[1]
            aream[counterm] = prop.area
            perimm[counterm] = prop.perimeter
            counterm += 1
        countermin = min(counter, counterm)
        if countermin <= 0:
            countermin += 1
        area.sort()
        aream.sort()
        areadiff = 0 
        for i in range(0, countermin-1):
            areaper = ((area[i]-aream[i])/aream[i])*10
            areadiff += areaper
        areadiffmean = areadiff/countermin
        areamethod = ('area method', areadiffmean)
        score.append(areamethod)
        
        # overlap method
        fill = binary_fill_holes(clean_img) # filling holes of every cell
        rows, cols = fill.shape
        num = 0
        for i in range(rows):
            for j in range(cols):
                if fill[i,j] == imgman[i,j]:
                    num += 1
        overlapdiff = 100-num/(rows*cols)*100
        overlapmethod = ('overlap method', overlapdiff)
        score.append(overlapmethod)
        scorelist.append(score)
        #i += 1
    return scorelist

def whichBest(scores):
    li = scores[0][0][1] + scores[0][1][1] + scores[0][2][1]
    minimum = scores[1][0][1] + scores[1][1][1] + scores[1][2][1]
    triangle = scores[2][0][1] + scores[2][1][1] + scores[2][2][1]
    isodata = scores[3][0][1] + scores[3][1][1] + scores[3][2][1]
    mean = scores[4][0][1] + scores[4][1][1] + scores[4][2][1]
    otsu = scores[5][0][1] + scores[5][1][1] + scores[5][2][1]
    yen = scores[6][0][1] + scores[6][1][1] + scores[6][2][1]
    minScore = min(li, minimum, triangle, isodata, mean, otsu, yen) 
    if minScore == li:
        print ("The recommended threshold method is Li with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == minimum:
        print ("The recommended threshold method is Minimum with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == triangle:
        print ("The recommended threshold method is Triangle with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == isodata:
        print ("The recommended threshold method is Isodata with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == mean:
        print ("The recommended threshold method is Mean with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == otsu:
        print ("The recommended threshold method is Otsu with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")
    if minScore == yen:
        print ("The recommended threshold method is Yen with a score of ", minScore/3, "which means the thresholded image is ", minScore/3, "% different from the manually labelled image.")

def main():

    # Calls for an infinite loop that keeps executing
    # until an exception occurs
    while True:
        print("Are you ready to find the most suitable threshold method for your medical images? ifThresholds can help you to find the best one among li, minimum, triangle, isodata, mean, otsu, and yen threshold methods.")
        ori_path = input("What is the path to your orginal TIFF image?")
        man_path = input("What is the path to your manually labelled TIFF image?")
        
        try:
            manual_count= int(input("What is the number of cells in your image based on your manual count?" ))

        # If something else that is not the string
        # version of a number is introduced, the
        # ValueError exception will be called.
        except ValueError:
            print ("Error! The manual count has to be an integer!" )
            # The cycle will go on until validation
            # print("Error! Couldn't find the image. Please check the location of your image.")

        # When successfully converted to an integer,
        # the loop will end.
        else:
            scores = img_score(ori_path, man_path, manual_count)
            whichBest(scores)
            #print("Impressive, ", test4word, "! You spent", test4num*60, "minutes or", test4num*60*60, "seconds in your mobile!")
            ifCVS = input("Do you want to obtain a score table of your image saved in your current directiory (y) or exit the program (n)?")
            if ifCVS == 'y' or ifCVS == 'Y':
                with open('scoretable.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Threshold_method', 'score_method', 'Score % off']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    writer.writerow({'Threshold_method': 'Li', 'score_method': 'count method', 'Score % off': scores[0][0][1]})
                    writer.writerow({'Threshold_method': 'Li', 'score_method': 'area method', 'Score % off': scores[0][1][1]})
                    writer.writerow({'Threshold_method': 'Li', 'score_method': 'overlap method', 'Score % off': scores[0][2][1]})
                    writer.writerow({'Threshold_method': 'Minimum', 'score_method': 'count method', 'Score % off': scores[1][0][1]})
                    writer.writerow({'Threshold_method': 'Minimum', 'score_method': 'area method', 'Score % off': scores[1][1][1]})
                    writer.writerow({'Threshold_method': 'Minimum', 'score_method': 'overlap method', 'Score % off': scores[1][2][1]})
                    writer.writerow({'Threshold_method': 'Triangle', 'score_method': 'count method', 'Score % off': scores[2][0][1]})
                    writer.writerow({'Threshold_method': 'Triangle', 'score_method': 'area method', 'Score % off': scores[2][1][1]})
                    writer.writerow({'Threshold_method': 'Triangle', 'score_method': 'overlap method', 'Score % off': scores[2][2][1]})
                    writer.writerow({'Threshold_method': 'isodata', 'score_method': 'count method', 'Score % off': scores[3][0][1]})
                    writer.writerow({'Threshold_method': 'isodata', 'score_method': 'area method', 'Score % off': scores[3][1][1]})
                    writer.writerow({'Threshold_method': 'isodata', 'score_method': 'overlap method', 'Score % off': scores[3][2][1]})
                    writer.writerow({'Threshold_method': 'Mean', 'score_method': 'count method', 'Score % off': scores[4][0][1]})
                    writer.writerow({'Threshold_method': 'Mean', 'score_method': 'area method', 'Score % off': scores[4][1][1]})
                    writer.writerow({'Threshold_method': 'Mean', 'score_method': 'overlap method', 'Score % off': scores[4][2][1]})
                    writer.writerow({'Threshold_method': 'Otsu', 'score_method': 'count method', 'Score % off': scores[5][0][1]})
                    writer.writerow({'Threshold_method': 'Otsu', 'score_method': 'area method', 'Score % off': scores[5][1][1]})
                    writer.writerow({'Threshold_method': 'Otsu', 'score_method': 'overlap method', 'Score % off': scores[5][2][1]})
                    writer.writerow({'Threshold_method': 'Yen', 'score_method': 'count method', 'Score % off': scores[6][0][1]})
                    writer.writerow({'Threshold_method': 'Yen', 'score_method': 'area method', 'Score % off': scores[6][1][1]})
                    writer.writerow({'Threshold_method': 'Yen', 'score_method': 'overlap method', 'Score % off': scores[6][2][1]})   
                print ('The socre table scoretable.csv is saved in your current directory! Thanks for using ifThresholds!')
                import pandas as pd
                print (pd.read_csv('scoretable.csv'))
            if ifCVS == 'n' or ifCVS == 'N':
                print("Thanks for using ifThresholds!")
            else:
                print ("Please type y to get a score table or type n to exit.")
            #ifAll = input("Do you want to have an image that is thresholded by all the threshold methods saved in your current directiory (y) or exit the program (n)?")
            #if ifAll == 'y' or ifAll == 'Y':
                
            break

# The function is called
main()

