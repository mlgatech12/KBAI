# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageFilter
import numpy as np
#from IPython.display import display 
#from guppy import hpy
from PIL import ImageChops as chops

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    #List to contain solution score for each option
    #Answers - 2, 5, 1, 3, 4, 5, 6, 6, 5, 3, 1, 1
    
    
    
    #create a list of attributes to find the difference in transformation:
    sizes = []
    size_attributes = ['small', 'medium', 'large', 'very large', 'huge']
    complex_attrib = ['above', 'inside']
    
    #other factors
    flip_factor = .01
    flip_mirror_factor = .035
    split_factor = .09
    medium_factor = .02
    rot_factor = .035
    same_dpr_factor = .0178
    diff_dpr_factor = 102
   
    
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        if problem.problemType.strip() == "2x2":
            #First get figure A, B and C
            solution = self.solve_2_by_2(problem)
        elif problem.problemType.strip() == "3x3":
            solution = self.solve_3_by_3(problem)
            
        print("Answer = ", solution)
        return solution
    
    def solve_2_by_2(self, problem):
        optionImg = []
        sol_score_2by2 = [0]*6
        transform_change = 15
        dpr_change = 10
        
        
        imgA = self.getImage(problem.figures['A'])
        imgB = self.getImage(problem.figures['B'])
        imgC = self.getImage(problem.figures['C'])
        for i in range(0,6):
            optionImg.append(self.getImage(problem.figures[str(i + 1)]))
        
        
        #First get figure A, B and C
        figA = problem.figures['A']
        figB = problem.figures['B']
        figC = problem.figures['C']
        
        #Check the better transformation
        better = self.getBetterTransformation(figA, figB, figC)
        if(problem.hasVerbal):
            if better == 'B' :
                mapping = self.transform(figA, figB)
                solution = self.getAnswer_2_by_2(problem, figC, mapping)
            else:
                mapping = self.transform(figA, figC)
                solution = self.getAnswer_2_by_2(problem, figB, mapping)
        
        #Solve problems visually
        else:
        #check difference
            transform = chops.difference(imgA, imgB)
            for i in range(len(optionImg)):
                option_transform = chops.difference(imgC, optionImg[i])
                if(transform == option_transform):
                    print("Adding score in difference:", i+1 )
                    sol_score_2by2[i] += transform_change
            
        
            #check logical and #fails Basic B-4
            '''
            transform = chops.logical_and(imgA.convert(mode = "1"), imgB.convert(mode = "1"))
            for j in range(len(optionImg)):
                option_transform = chops.logical_and(imgC.convert(mode = "1"), optionImg[j].convert(mode = "1"))
                if(transform == option_transform):
                    print("Answer match with logical and")
                    return (j + 1)
            '''
            
            
            transform = chops.logical_or(imgA.convert(mode = "1"), imgB.convert(mode = "1"))
            for ij in range(len(optionImg)):
                option_transform = chops.logical_or(imgC.convert(mode = "1"), optionImg[i].convert(mode = "1"))
                if(transform == option_transform):
                    print("Adding score logical or for:", i+1 )
                    sol_score_2by2[i] += transform_change
                    
            
            #check addition
            transform = chops.add(imgA, imgB)
            for i in range(len(optionImg)):
                option_transform = chops.add(imgC, optionImg[i])
                if(transform == option_transform):
                    print("Adding score in add:", i+1 )
                    sol_score_2by2[i] += transform_change
            
            #print("length = ", len(sol_score_2by2), ",", len(optionImg))
            #print("values = ", sol_score_2by2)
            if (self.check_dark_pixel_ratio_increase_2(imgA, imgB)):
                for i in range(len(optionImg)):
                    if(self.check_dark_pixel_ratio_increase_2(imgC, optionImg[i])):
                        print("Adding score in dark_pixel_ratio_increase 1 for:", i+1 )
                        sol_score_2by2[i] += dpr_change
                        
            #check vertical transform rowwise
            if (self.vertical_transform(imgA, imgB)):
                for i in range(len(optionImg)):
                    if(self.vertical_transform(imgC, optionImg[i])):
                        print("Adding score for vertical_transform:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check vertical transform colwise
            if (self.vertical_transform(imgA, imgC)):
                for i in range(len(optionImg)):
                    if(self.vertical_transform(imgB, optionImg[i])):
                        print("Adding score for vertical_transform:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check horizontal transform rowwise
            if (self.horizontal_transform(imgA, imgB)):
                for i in range(len(optionImg)):
                    if(self.horizontal_transform(imgC, optionImg[i])):
                        print("Adding score for horizontal_transform:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check vertical transform colwise
            if (self.horizontal_transform(imgA, imgC)):
                for i in range(len(optionImg)):
                    if(self.horizontal_transform(imgB, optionImg[i])):
                        print("Adding score for horizontal_transform:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            
            #check rotation
            if (self.check_rotation_90(imgA, imgB, ct = 3)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgC, optionImg[i], ct = 3)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check vertical transform colwise
            if (self.check_rotation_90(imgA, imgC, ct = 3)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgB, optionImg[i], ct = 3)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check rotation
            if (self.check_rotation_90(imgA, imgB, ct = 2)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgC, optionImg[i], ct = 2)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check vertical transform colwise
            if (self.check_rotation_90(imgA, imgC, ct = 2)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgB, optionImg[i], ct = 2)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check rotation
            if (self.check_rotation_90(imgA, imgB, ct = 1)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgC, optionImg[i], ct = 1)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            #check vertical transform colwise
            if (self.check_rotation_90(imgA, imgC, ct = 1)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgB, optionImg[i], ct = 1)):
                        print("Adding score for check_rotation_90:", i+1 )
                        sol_score_2by2[i] += transform_change
                        
            
        
        
            print("Problem name = ", problem.name, "Scores = ", sol_score_2by2 )
            solution =  sol_score_2by2.index(max(sol_score_2by2)) + 1 
            
        return solution
    
    
    def solve_3_by_3(self, problem):
        sol_score_3by3 = [0]*8
        #weights 
        dpl_same = 20
        dpl_change = 15
        transform_change = 18
        split_change = 10
        closest_match_change = 4 #this causes overfitting, keep it low
        addition_change = 10
        pair_wise_change = 20
        zigzag_dpl_change = 15
        
        optionImg = []
        imgA = self.getImage(problem.figures['A'])
        imgB = self.getImage(problem.figures['B'])
        imgC = self.getImage(problem.figures['C'])
        imgD = self.getImage(problem.figures['D'])
        imgE = self.getImage(problem.figures['E'])
        imgF = self.getImage(problem.figures['F'])
        imgG = self.getImage(problem.figures['G'])
        imgH = self.getImage(problem.figures['H'])
        
        
        #load solution array
        for i in range(0,8):
            optionImg.append(self.getImage(problem.figures[str(i + 1)]))
            
        
        t = self.vertical_split_and_double(imgH, optionImg[4])
        print("t = ", t)
        
        
        
        #add score for better dark pixel ratio
        #check if dark pixel ratio is increasing rowwise A,B,C and D,E,F. Check with bottom row G,H, option
        if (self.check_dark_pixel_ratio_increase(imgA, imgB, imgC) and self.check_dark_pixel_ratio_increase(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_increase(imgG, imgH, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_increase 1 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
        
        #check if dark pixel ratio is increasing colwise A,D,G and B,E,H. Check with last col C,F, option
        if (self.check_dark_pixel_ratio_increase(imgA, imgD, imgG) and self.check_dark_pixel_ratio_increase(imgB, imgE, imgH)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_increase(imgC, imgF, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_increase 2 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
        
        #check zig zag dpr increase 
        #zig-zag addition - H - F = F - A, C - G = G - E, D -B = B - option
        if (abs(self.get_difference_dark_pixel(imgH, imgF) - self.get_difference_dark_pixel(imgF, imgA)) < self.diff_dpr_factor
           and abs(self.get_difference_dark_pixel(imgC, imgG) - self.get_difference_dark_pixel(imgG, imgE)) < self.diff_dpr_factor):
            print("--match")
            for i in range(len(optionImg)):
                if(abs(self.get_difference_dark_pixel(imgD, imgB) - self.get_difference_dark_pixel(imgB, optionImg[i])) < self.diff_dpr_factor):
                    print("Adding score in zig zag dpr change for:", i+1 )
                    sol_score_3by3[i] += zigzag_dpl_change
       
        
            
         #check if dark pixel ratio is increasing diagonally C,E,G. Check with other diagonal col A,E, option
        if (self.check_dark_pixel_ratio_increase(imgC, imgE, imgG)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_increase(imgA, imgE, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_increase 3 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
                    
           
        #check if dark pixel ratio is decreasing rowwise A,B,C and D,E,F. Check with bottom row G,H, option
        if (self.check_dark_pixel_ratio_decrease(imgA, imgB, imgC) and self.check_dark_pixel_ratio_decrease(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_decrease(imgG, imgH, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_decrease 1 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
        
        #check if dark pixel ratio is decreasing colwise A,D,G and B,E,H. Check with last col C,F, option
        if (self.check_dark_pixel_ratio_decrease(imgA, imgD, imgG) and self.check_dark_pixel_ratio_decrease(imgB, imgE, imgH)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_decrease(imgC, imgF, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_decrease 2 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
                    
         #check if dark pixel ratio is decreasing diagonally C,E,G. Check with other diagonal col A,E, option
        if (self.check_dark_pixel_ratio_decrease(imgC, imgE, imgG)):
            for i in range(len(optionImg)):
                if(self.check_dark_pixel_ratio_decrease(imgA, imgE, optionImg[i])):
                    print("Adding score in dark_pixel_ratio_decrease 3 for:", i+1 )
                    sol_score_3by3[i] += dpl_change
                    
        #check if dark pixel ratio is same rowwise and colwise   
        if (abs(self.get_dark_pixel_ratio_sum(imgA, imgB, imgC) - self.get_dark_pixel_ratio_sum(imgD, imgE, imgF)) < self.same_dpr_factor
           and abs(self.get_dark_pixel_ratio_sum(imgA, imgD, imgG) - self.get_dark_pixel_ratio_sum(imgB, imgE, imgH)) < .025) :
           for i in range(len(optionImg)):
               if((abs(self.get_dark_pixel_ratio_sum(imgG, imgH, optionImg[i]) - self.get_dark_pixel_ratio_sum(imgD, imgE, imgF))) < self.same_dpr_factor
                  and abs(self.get_dark_pixel_ratio_sum(imgC, imgF, optionImg[i]) - self.get_dark_pixel_ratio_sum(imgB, imgE, imgH)) < self.same_dpr_factor):
                   print("Adding score in dark_pixel_ratio_ same for:", i+1 )
                   sol_score_3by3[i] += dpl_same
       
       
        #check vertical transformation A,G 
        if (self.vertical_transform(imgA, imgG) and self.vertical_transform(imgB, imgH)):
            for i in range(len(optionImg)):
                if(self.vertical_transform(imgC, optionImg[i])):
                    print("Adding score in vertical_transform 1 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
        '''
        #check vertical transformation B,H 
        if (self.vertical_transform(imgB, imgH)):
            for i in range(len(optionImg)):
                if(self.vertical_transform(imgC, optionImg[i])):
                    print("Adding score in vertical_transform 2 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        '''            
        #check horizontal transformation A,C 
        if (self.horizontal_transform(imgA, imgC)):
            print("horizontal_transform")
            for i in range(len(optionImg)):
                if(self.horizontal_transform(imgG, optionImg[i])):
                    print("Adding score in horizontal_transform 1 for:", i+1 )
                    sol_score_3by3[i] += transform_change
                    
         #check horizontal transformation D,F
        if (self.horizontal_transform(imgD, imgF)):
            for i in range(len(optionImg)):
                if(self.horizontal_transform(imgG, optionImg[i])):
                    print("Adding score in horizontal_transform 2 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
        
        #check and logic - rowwise
        if (self.check_and(imgA, imgB, imgC) and self.check_and(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                if(self.check_and(imgG,imgH, optionImg[i])):
                    print("Adding score in check_and 1 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
         #check and logic - colwise
        if (self.check_and(imgA, imgD, imgG) and self.check_and(imgB, imgE, imgH)):
            for i in range(len(optionImg)):
                if(self.check_and(imgC,imgF, optionImg[i])):
                    print("Adding score in check_and 2 for:", i+1 )
                    sol_score_3by3[i] += transform_change
                    
        #check rowwise alternate
        if (self.check_and(imgA, imgG, imgD) and self.check_and(imgB, imgH, imgE)):
            for i in range(len(optionImg)):
                if(self.check_and(imgC,optionImg[i], imgF)):
                    print("Adding score in check_and 3 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
         #check colwise alternate
        if (self.check_and(imgA, imgC, imgB) and self.check_and(imgD, imgF, imgE)):
            for i in range(len(optionImg)):
                if(self.check_and(imgG,optionImg[i], imgH)):
                    print("Adding score in check_and 4 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
            
         #check and logic - diagonally
        if (self.check_and(imgC, imgE, imgG)):
            for i in range(len(optionImg)):
                if(self.check_and(imgA,imgE, optionImg[i])):
                    print("Adding score in check_or 5 for:", i+1 )
                    sol_score_3by3[i] += transform_change
                    
                  
         #check or logic - rowwise
        if (self.check_or(imgA, imgB, imgC) and self.check_or(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                if(self.check_or(imgG,imgH, optionImg[i])):
                    print("Adding score in check_or 2 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
         #check or logic - colwise
        if (self.check_or(imgA, imgD, imgG) and self.check_or(imgB, imgE, imgH)):
            for i in range(len(optionImg)):
                if(self.check_or(imgC,imgF, optionImg[i])):
                    print("Adding score in check_or 3 for:", i+1 )
                    sol_score_3by3[i] += transform_change
                    
        #check rowwise alternate
        if (self.check_or(imgA, imgG, imgD) and self.check_or(imgB, imgH, imgE)):
            for i in range(len(optionImg)):
                if(self.check_or(imgC,optionImg[i], imgF)):
                    print("Adding score in check_or 4 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
         #check colwise alternate
        if (self.check_or(imgA, imgC, imgB) and self.check_or(imgD, imgF, imgE)):
            for i in range(len(optionImg)):
                if(self.check_or(imgG,optionImg[i], imgH)):
                    print("Adding score in check_or 4 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
            
         #check or logic - diagonally
        if (self.check_or(imgC, imgE, imgG)):
            for i in range(len(optionImg)):
                if(self.check_or(imgA,imgE, optionImg[i])):
                    print("Adding score in check_or 5 for:", i+1 )
                    sol_score_3by3[i] += transform_change
        
        #check for perfect match by splitting - rowwise
        if (self.horizontal_split_partial(imgA,imgG) and self.horizontal_split_partial(imgB,imgH)):
            for i in range(len(optionImg)):
                if(self.horizontal_split_partial(imgC,optionImg[i])):
                    print("Adding score in horizontal_split_partial 1 for:", i+1 )
                    sol_score_3by3[i] += transform_change
                    
         #check for perfect match by splitting - colwise
        if (self.horizontal_split_partial(imgA,imgC) and self.horizontal_split_partial(imgD,imgF)):
            for i in range(len(optionImg)):
                if(self.horizontal_split_partial(imgG,optionImg[i])):
                    print("Adding score in horizontal_split_partial 2 for:", i+1 )
                    sol_score_3by3[i] += transform_change
       
        
        #check for perfect match by splitting & mirror
        if (self.check_split_and_mirror(imgA,imgC) and self.check_split_and_mirror(imgD,imgF)):
            for i in range(len(optionImg)):
                if(self.check_split_and_mirror(imgG,optionImg[i])):
                    print("Adding score in vertical_split_mirror for:", i+1 )
                    sol_score_3by3[i] += split_change
        
        
        #check for perfect match by splitting & mirror
        if (self.check_split_and_mirror(imgC,imgA) and self.check_split_and_mirror(imgF,imgD)):
            for i in range(len(optionImg)):
                if(self.check_split_and_mirror(optionImg[i], imgG)):
                    print("Adding score in vertical_split_mirror for:", i+1 )
                    sol_score_3by3[i] += split_change
        
        #check with xor rowwise
        if (self.check_xor(imgD, imgE, imgG, imgH)):
            for i in range(len(optionImg)):
                if(self.check_xor(imgF, imgE, optionImg[i], imgH)):
                    print("Adding score in check_xor rowwise:", i+1 )
                    sol_score_3by3[i] += split_change
        
            
        #check add and difference rowwise
        if (self.check_add_and_difference(imgA, imgB, imgC) and self.check_add_and_difference(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                if(self.check_add_and_difference(imgG, imgH, optionImg[i])):
                    print("Adding score in check_add_and_difference rowwise:", i+1 )
                    sol_score_3by3[i] += split_change
                    
        
        #check if pixel size is doubled
        if (self.check_pixels_doubled(imgC, imgF) and self.check_pixels_doubled(imgA, imgD) and self.check_pixels_doubled(imgB, imgE)):
            for i in range(len(optionImg)):
                print("calling from check_pixels_doubled ", i+1)
                if(self.check_pixels_tripled(imgC,optionImg[i])):
                    print("Adding score in check_pixels_doubled:", i+1 )
                    sol_score_3by3[i] += transform_change
        
        
        #check if inner images are same - rowwise
        if (self.fraction_horizontal_split(imgA, imgB, imgC) and self.fraction_horizontal_split(imgD, imgE, imgF)):
            for i in range(len(optionImg)):
                print("calling from fraction_horizontal_split ", i+1)
                if(self.fraction_horizontal_split(imgG, imgH, optionImg[i])):
                    print("Adding score in fraction_horizontal_split 1:", i+1 )
                    sol_score_3by3[i] += transform_change
        
        #check with pairwise difference
        if (self.check_same(self.get_difference(imgB, imgC), self.get_difference(imgE, imgF), 2.5) and
            self.check_same(self.get_difference(imgB, imgA), self.get_difference(imgE, imgD), 2.5)) :
            for i in range(len(optionImg)):
                if(self.check_same(self.get_difference(imgB, imgC), self.get_difference(optionImg[i], imgH), 2.5)):
                    print("Adding score in pairwise difference 1:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
        
        
         #check double pairwise addition
        if (self.check_same(self.get_addition(imgA, imgB), self.get_addition(imgB, imgC), 2.0) and
            self.check_same(self.get_addition(imgD, imgE), self.get_addition(imgE, imgF), 2.0)):
            for i in range(len(optionImg)):
                if(self.check_same(self.get_addition(imgG, imgH), self.get_addition(imgH, optionImg[i]), 2.0)
                and self.check_same(self.get_addition(imgC, imgF), self.get_addition(imgF, optionImg[i]), 2.0)):
                    print("Adding score in pairwise addition 1:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
        
        
        #check with pairwise addition
        if (self.check_same(self.get_addition(imgA, imgB), self.get_addition(imgC, imgC), 2.5) and
            self.check_same(self.get_addition(imgD, imgE), self.get_addition(imgF, imgF), 2.5)):
            for i in range(len(optionImg)):
                if(self.check_same(self.get_addition(imgG, imgH), self.get_addition(optionImg[i], optionImg[i]), 2.5)):
                    print("Adding score in pairwise addition 2:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
                    
         #check with all rowwise addition
        if (self.check_same(self.get_addition_all(imgA, imgB, imgC), self.get_addition_all(imgD, imgE, imgF), 2.5)):
            for i in range(len(optionImg)):
                if(self.check_same(self.get_addition_all(imgA, imgB, imgC), self.get_addition_all(optionImg[i], imgG, imgH), 2.5)):
                    print("Adding score in all rowwise addition:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
        
          #check with all colwise addition
        if (self.check_same(self.get_addition_all(imgA, imgD, imgG), self.get_addition_all(imgB, imgE, imgH), 2.5)):
            for i in range(len(optionImg)):
                if(self.check_same(self.get_addition_all(imgA, imgD, imgG), self.get_addition_all(optionImg[i], imgC, imgF), 2.5)):
                    print("Adding score in all colwise addition:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
       
        #zig-zag addition - A + F = H, G + E = C, B + option = D
        if (self.check_same(self.get_addition(imgA, imgF), self.get_addition(imgH, imgH), 2.5) and self.check_same(self.get_addition(imgG, imgE), self.get_addition(imgC, imgC), 2.5)):
            for i in range(len(optionImg)):
                if(self.check_same(self.get_addition(imgB, optionImg[i]), self.get_addition(imgD, imgD), 2.5)):
                    print("Adding score in zig zag addition:", i+1 )
                    sol_score_3by3[i] += pair_wise_change
       
        #check rotation
        if (self.check_rotation_90(imgA, imgC, ct = 3) and self.check_rotation_90(imgD, imgF, ct = 3)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgG, optionImg[i], ct = 3)):
                        print("Adding score for check_rotation_90 1:", i+1 )
                        sol_score_3by3[i] += pair_wise_change
        
        #check rotation
        if (self.check_rotation_90(imgA, imgB, ct = 3) and self.check_rotation_90(imgB, imgC, ct = 3) and self.check_rotation_90(imgD, imgE, ct = 3) and self.check_rotation_90(imgE, imgF, ct = 3)):
                for i in range(len(optionImg)):
                    if(self.check_rotation_90(imgH, optionImg[i], ct = 3)):
                        print("Adding score for check_rotation_90 2:", i+1 )
                        sol_score_3by3[i] += pair_wise_change
         
        # specific solution move image and add
        if (self.move_image_and_add(imgA, imgB, imgC) and self.move_image_and_add(imgD, imgE, imgF)):
                for i in range(len(optionImg)):
                    if(self.move_image_and_add(imgG, imgH, optionImg[i])):
                        print("Adding score for move_image_and_add:", i+1 )
                        sol_score_3by3[i] += pair_wise_change
        
        # specific solution move image, rotate and add
        if ( self.move_image_rotate_and_add(imgD, imgE, imgF, move_1 = -25, move_2 = 50) and self.move_image_rotate_and_add(imgA, imgB, imgC)):
                for i in range(len(optionImg)):
                    if(self.move_image_rotate_and_add(imgG, imgH, optionImg[i], move_1 = -25)):
                        print("Adding score for move_image_and_add:", i+1 )
                        sol_score_3by3[i] += pair_wise_change
        
        #increase image size and zig zag add
        #self.increase_size(imgB)
        #check if pixel solution should be mirror image
        #if (self.horizontal_split_half(imgC) and self.horizontal_split_half(imgF)):
        #    for i in range(len(optionImg)):
        #        if(self.horizontal_split_half(optionImg[i])):
        #            print("Adding score in check_pixels_doubled:", i+1 )
        #            sol_score_3by3[i] += mirror_factor
        
        #calculate rowwise quadrants ratio (1st row)
        ab_quads = self.get_dark_pixel_quads_ratio(imgA, imgB)
        bc_quads = self.get_dark_pixel_quads_ratio(imgB, imgC)
        gh_quads = self.get_dark_pixel_quads_ratio(imgG, imgH)
        prop_arr = [0.0]*8
        for i in range(len(optionImg)):
            prop_arr[i] = self.get_dark_pixel_quads_ratio(imgH,optionImg[i])
        
        idx = self.add_closest_quads_match(ab_quads, bc_quads, gh_quads, prop_arr )
        if(idx is not None):
            print("Adding score match for rowwise quadrants ratio (1st row)" , idx + 1)
            sol_score_3by3[idx] += closest_match_change
        
        #calculate rowwise quadrants ratio (2nd row)
        de_quads = self.get_dark_pixel_quads_ratio(imgD, imgE)
        ef_quads = self.get_dark_pixel_quads_ratio(imgE, imgF)
        
        idx = self.add_closest_quads_match(de_quads, ef_quads, gh_quads, prop_arr )
        if(idx is not None):
            print("Adding score for rowwise quadrants ratio (2nd row)" , idx + 1)
            sol_score_3by3[idx] += closest_match_change
        
        
        
         #calculate colwise quadrants ratio (1st col)
        ad_quads = self.get_dark_pixel_quads_ratio(imgA, imgD)
        dg_quads = self.get_dark_pixel_quads_ratio(imgD, imgG)
        cf_quads = self.get_dark_pixel_quads_ratio(imgC, imgF)
        prop_arr = [0.0]*8
        for i in range(len(optionImg)):
            prop_arr[i] = self.get_dark_pixel_quads_ratio(imgF,optionImg[i])
        
        idx = self.add_closest_quads_match(ad_quads, dg_quads, cf_quads, prop_arr )
        if(idx is not None):
            print("Adding score for colwise quadrants ratio (1st col)" , idx + 1)
            sol_score_3by3[idx] += closest_match_change
        
        #calculate colwise quadrants ratio (2nd col)
        be_quads = self.get_dark_pixel_quads_ratio(imgB, imgE)
        eh_quads = self.get_dark_pixel_quads_ratio(imgE, imgH)
        
        idx = self.add_closest_quads_match(be_quads, eh_quads, cf_quads, prop_arr )
        if(idx is not None):
            print("Adding score colwise quadrants ratio (2nd col)" , idx + 1)
            sol_score_3by3[idx] += closest_match_change
        
        
        #calculate diagonal wise quadrants ratio
        ce_quads = self.get_dark_pixel_quads_ratio(imgC, imgE)
        eg_quads = self.get_dark_pixel_quads_ratio(imgE, imgG)
        ae_quads = self.get_dark_pixel_quads_ratio(imgA, imgE)
        prop_arr = [0.0]*8
        for i in range(len(optionImg)):
            prop_arr[i] = self.get_dark_pixel_quads_ratio(imgE,optionImg[i])
        
        
        idx = self.add_closest_quads_match(ce_quads, eg_quads, ae_quads, prop_arr )
        if(idx is not None):
            print("Adding score for digonalwise quadrants" , idx + 1)
        
            sol_score_3by3[idx] += closest_match_change
            
        ## Check if there are more than one answers 
        ans = max(sol_score_3by3)
        ans_indices = [i for i, j in enumerate(sol_score_3by3) if j == ans]
        
        
        #check if pixel sum remains almost constant
        if (ans_indices is not None and len(ans_indices) >= 2):
            sum_1 = self.sum_pixels(imgA, imgB, imgC)
            sum_2 = self.sum_pixels(imgD, imgE, imgF)
            if(self.is_close_sum(sum_1, sum_2)):
                for i in range(len(optionImg)):
                    sum_3 = self.sum_pixels(imgG, imgH, optionImg[i])
                    if(self.is_close_sum(sum_1, sum_3) or self.is_close_sum(sum_2, sum_3)):
                        print("Adding score in sum_pixels:", i+1 )
                        sol_score_3by3[i] += addition_change
                        
            if(self.vertical_split_and_double(imgB,imgC) and self.vertical_split_and_double(imgE,imgF)):
                for i in range(len(optionImg)):
                    if(self.vertical_split_and_double(imgH,optionImg[i])):
                        print("Adding score in vertical_split_and_double:", i+1 )
                        sol_score_3by3[i] += addition_change
        
        
        print("Problem name = ", problem.name, "Scores = ", sol_score_3by3 )
        
        return  sol_score_3by3.index(max(sol_score_3by3)) + 1
   
    def vertical_split_one_third(self, img1):
        array1 = self.convert_img_to_array(img1)
        print(array1.shape)
        split_result = np.array_split(array1, 3, axis=1)
        
        print(split_result[0].shape)
        print(split_result[1].shape)
        print(split_result[2].shape)
        
        #new_img = np.fliplr(split_result[1])
        '''
        print("---")
        display(Image.fromarray(split_result[0]).convert(mode = "L"))
        print("---")
        display(Image.fromarray(split_result[1]).convert(mode = "L"))
        print("---")
        display(Image.fromarray(split_result[2]).convert(mode = "L"))
        
        '''
        if(split_result[0].shape == split_result[1].shape):
            actual_result = np.bitwise_xor(split_result[0], new_img)
            print("diff = ", np.count_nonzero(actual_result)/ actual_result.size)
            return (np.count_nonzero(actual_result) < self.flip_mirror_factor * actual_result.size)
        
        if(split_result[0].shape == split_result[1].shape):
            actual_result = np.bitwise_xor(split_result[0], split_result[1])
            print("diff = ", np.count_nonzero(actual_result)/ actual_result.size)
            return (np.count_nonzero(actual_result) < self.flip_mirror_factor * actual_result.size)
        
        
        #print("diff = ", np.count_nonzero(actual_result))
        
        return False
    
    def vertical_split_and_double(self, img1, img2):
        #print("inside  vertical_split_and double")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        #print(array1.shape)
        split_result = np.array_split(array1, 2, axis=1)
        
        pixels_1 = 2 * (split_result[1].size - np.count_nonzero(split_result[1]))
        pixels_2 = array2.size - np.count_nonzero(array2)
        
        
        diff = abs(pixels_1 - pixels_2)
        #print("diff = ", diff)
        if diff < 50:
            #print("returning true")
            return True
        else:
            #print("difference = " , diff)
            return False
        
    def horizontal_split_half(self, img1):
        array1 = self.convert_img_to_array(img1)
        print(array1.shape)
        split_result = np.array_split(array1, 2, axis=1)
        
        print(split_result[0].shape)
        print(split_result[1].shape)
        
        new_img = np.fliplr(split_result[1])
        '''
        print("---")
        display(Image.fromarray(split_result[0]).convert(mode = "L"))
        print("---")
        display(Image.fromarray(new_img).convert(mode = "L"))
        print("---")
        display(Image.fromarray(split_result[1]).convert(mode = "L"))
        '''
        
        if(split_result[0].shape == split_result[1].shape):
            actual_result = np.bitwise_xor(split_result[0], new_img)
            #print("diff = ", np.count_nonzero(actual_result)/ actual_result.size)
            return (np.count_nonzero(actual_result) < self.flip_mirror_factor * actual_result.size)
        
        if(split_result[0].shape == split_result[1].shape):
            actual_result = np.bitwise_xor(split_result[0], split_result[1])
            #print("diff = ", np.count_nonzero(actual_result)/ actual_result.size)
            return (np.count_nonzero(actual_result) < self.flip_mirror_factor * actual_result.size)
        
        
        #print("diff = ", np.count_nonzero(actual_result))
        return False
    
    
    def keep_score_for_better_dpr_match(self, img1, img2, optionImgs, solnList):
        dpr1 = self.get_dark_pixel_ratio(img1)
        dpr2 = self.get_dark_pixel_ratio(img2)
        
        t1  = dpr2 - dpr1
        ratios_diff = [0]*8
        for i in range(len(optionImgs)):
            if (solnList[i] != -1):
                ratios_diff[i] = abs(dpr2 - self.get_dark_pixel_ratio(optionImgs[i]) - t1)
        
        idx = ratios_diff.index(max(ratios_diff))   
        if(idx >= 0 and solnList[idx] != -1):
            return idx
        
    
    def check_dark_pixel_ratio_increase(self, image1, image2, image3):
        dpr1 = self.get_dark_pixel_ratio(image1)
        dpr2 = self.get_dark_pixel_ratio(image2)
        dpr3 = self.get_dark_pixel_ratio(image3)
        
        #check difference and return true only if the increase is not significant
        '''
        print("ratios")
        print("image1 = ",dpr1)
        print("image2 = ",dpr2)
        print("image3 = ",dpr3)
        '''
        if(dpr3 > dpr2 > dpr1):
            t1 = dpr2 - dpr1
            t2 = dpr3 - dpr2
            if(t2 > t1 * 2.0):
                return False
            else:
                return True
        else:
            return False
        
    def check_dark_pixel_ratio_decrease(self, image1, image2, image3):
        dpr1 = self.get_dark_pixel_ratio(image1)
        dpr2 = self.get_dark_pixel_ratio(image2)
        dpr3 = self.get_dark_pixel_ratio(image3)
        
        #check difference and return true only if the increase is not significant
        '''
        if(dpr1 > dpr2 > dpr3):
            t1 = dpr2 - dpr1
            t2 = dpr3 - dpr2
            if(t2 > t1 * 2.0):
                return False
            else:
                return True
        '''
        return dpr1 > dpr2 > dpr3
    
    def get_dark_pixel_ratio_sum(self, image1, image2, image3):
        print("inside get_dark_pixel_ratio_sum")
        dpr1 = self.get_dark_pixel_ratio(image1)
        dpr2 = self.get_dark_pixel_ratio(image2)
        dpr3 = self.get_dark_pixel_ratio(image3)
        
        print("sum = ", dpr1 + dpr2 + dpr3)
        return dpr1 + dpr2 + dpr3
    
    def get_difference_dark_pixel(self, img1, img2):
        print("inside get_difference_dark_pixel")
        dpr1 = self.get_dark_pixel_count(img1)
        dpr2 = self.get_dark_pixel_count(img2)
        
        diff = abs(dpr1 - dpr2)
        print("difference = ", diff)
        return diff
        
    def transform2by2(self, figure1 , figure2):
        mapping = chops.difference(figure1, figure2)
        #print("mapping is" , mapping)
        return mapping
    
    def transform3by3(self, figure1 , figure2, figure3, figure4, figure5, figure6, figure7, figure8):
        mapping = chops.difference(figure1, figure2)
        return mapping
    
    def getDifferenceForSize(a,b):
        return size_attributes.indexof(a) - size_attributes.indexof(b)
    
    def vertical_transform(self, img1, img2):
        print("in vertical_transform")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        flip_result = np.flipud(array1)
        actual_result = np.bitwise_xor(array2, flip_result)
        
        print("end ", (np.count_nonzero(actual_result)) < self.flip_factor * flip_result.size)
        
        return (np.count_nonzero(actual_result) < self.flip_factor * flip_result.size)
    
    def horizontal_transform(self, img1, img2):
        print("in horizontal_transform")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        flip_result = np.fliplr(array1)
        actual_result = np.bitwise_xor(array2, flip_result)
        
        
        return (np.count_nonzero(actual_result) < self.flip_factor * flip_result.size)
    
    def move_image_and_add(self, img1, img2, img3):
        print("inside move_image")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img2_roll = np.roll(array2, -50, axis = 1)
        img3_roll = np.roll(array3, 25, axis = 1)
        
        new_img_1 = Image.fromarray(array1).convert(mode = "1")
        new_img_2 = Image.fromarray(img2_roll).convert(mode = "1")
        new_img_3 = Image.fromarray(img3_roll).convert(mode = "1")
        
        add_1 = chops.logical_and(new_img_2, new_img_3)
        add_2 = chops.logical_and(new_img_1,new_img_1)
         
        '''
        display(Image.fromarray(img2_roll))
        display(Image.fromarray(img3_roll))
        display(add_2)
        display(add_1)
        '''
        match = self.check_same(add_2, add_1, 2.5)
        
        print("match = ", match)
        
        return match
    
    def increase_size(self, img1):
        print("increase_size")
        #display(img1)
        array1 = self.convert_img_to_array(img1)
        array1 = array1.repeat([10, 10], axis=0)
        
        #display(Image.fromarray(array1))
        print(array1.shape)
    
    # negative moves left, +ve moves right
    def move_image_rotate_and_add(self, img1, img2, img3, move_1 = -50, move_2 = 25):
        print("move_image_rotate_and_add")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img2_a = np.flipud(array2)
        
        img2_b = np.roll(img2_a, move_1, axis = 1)
        img3_a = np.roll(array3, move_2, axis = 1)
        
        new_img_1 = Image.fromarray(array1).convert(mode = "1")
        
        new_img_2 = Image.fromarray(img2_b).convert(mode = "1")
        new_img_3 = Image.fromarray(img3_a).convert(mode = "1")
        
        add_1 = chops.logical_and(new_img_2, new_img_3)
        add_2 = chops.logical_and(new_img_1,new_img_1)
         
        '''
        display(Image.fromarray(img2_b))
        display(Image.fromarray(img3_a))
        display(add_2)
        display(add_1)
        
        '''
        match = self.check_same(add_2, add_1, 2.5)
        
        print("match = ", match)
        
        return match
    
    
    def check_rotation_90(self, img1, img2, ct = 1):
        print("in check_rotation_90")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        flip_result = np.rot90(array1, ct)
        
        #display(Image.fromarray(flip_result))
        #display(Image.fromarray(array2))
        actual_result = np.bitwise_xor(array2, flip_result)
        
        print("end ", np.count_nonzero(actual_result),"," ,self.rot_factor * flip_result.size)
        
        return (np.count_nonzero(actual_result) < self.rot_factor * flip_result.size)
    
    def horizontal_split_partial(self, img1, img2):
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        #print(array1.shape)
        split_result = np.array_split(array1, 3, axis=0)
        split_soln = np.array_split(array2, 3, axis=0)
        
        '''
        display(Image.fromarray(split_result[0]).convert(mode = "L"))
        print("---")
        display(Image.fromarray(split_result[1]).convert(mode = "L"))
        print("---")
        display(Image.fromarray(split_result[2]).convert(mode = "L"))
        '''
        
        
        #newimg = np.add(split_result[1],(split_result[2]))
        #print("done split", newimg.shape)
        #display(Image.fromarray(newimg).convert(mode = "L"))
        if(split_soln[2].shape == split_result[2].shape):
            actual_result = np.bitwise_xor(split_soln[2], split_result[2])
            return (np.count_nonzero(actual_result) < self.flip_factor * actual_result.size)
        else:
            return False
    
    
    def fraction_horizontal_split(self, img1, img2, img3):
        print("in fraction_horizontal_split")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        #print(array1.shape)
        split_result_1 = np.split(array1, [40,140,], axis=0)
        split_result_2 = np.split(array2, [40,140,], axis=0)
        split_result_3 = np.split(array3, [40,140,], axis=0)
        
        inner_result_1 = np.split(split_result_1[1], [40,140,], axis=1)
        inner_result_2 = np.split(split_result_2[1], [40,140,], axis=1)
        inner_result_3 = np.split(split_result_3[1], [40,140,], axis=1)
        
        
        
        #check if inner shapes are same
        if(inner_result_1[1].shape == inner_result_2[1].shape and inner_result_2[1].shape == inner_result_3[1].shape):
            diff_a = np.bitwise_xor(inner_result_1[1], inner_result_2[1])
            diff_b = np.bitwise_xor(inner_result_2[1], inner_result_3[1])
            
            match_1 = np.count_nonzero(diff_a) < self.flip_factor * diff_a.size
            match_2 = np.count_nonzero(diff_b) < self.flip_factor * diff_b.size
            print("match 1 = ", match_1)
            print("match = ", match_2)
        
            return (match_1 and match_2)
        
        else:
            return False
    
        
    def check_xor(self, img1, img2, img3, img4):
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        array4 = self.convert_img_to_array(img4)
        
        img1 = Image.fromarray(array1).convert(mode = "1")
        img2 = Image.fromarray(array2).convert(mode = "1")
        img3 = Image.fromarray(array3).convert(mode = "1")
        img4 = Image.fromarray(array4).convert(mode = "1")
        
        '''
        img1 = img1.convert(mode = "1")
        img2 = img2.convert(mode = "1")
        img3 = img3.convert(mode = "1")
        img4 = img4.convert(mode = "1")
        '''
        
        t1 = chops.logical_xor(img1, img2)
        t2 = chops.logical_xor(img3, img4)
        print("inside check_xor" )
        
        return self.check_same(t1, t2, 2.5)
    
    def get_difference(self, img1, img2):
        #print("inside get_difference")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        img1 = Image.fromarray(array1)
        img2 = Image.fromarray(array2)
        
        diff = chops.difference(img1,img2)
        
        #display(diff)
        #print("get_difference : " , diff )
        
        return diff
    
    
    def get_addition(self, img1, img2):
        print("inside get_addition")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        img1_a = Image.fromarray(array1).convert(mode = "1")
        img2_a = Image.fromarray(array2).convert(mode = "1")
        
        add = chops.logical_and(img1_a, img2_a)
        #display(add)
        
        #print("End --")
        return add
    
    
      
    def get_addition_all(self, img1, img2, img3):
        print("inside get_addition_all")
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img1_a = Image.fromarray(array1).convert(mode = "1")
        img2_a = Image.fromarray(array2).convert(mode = "1")
        img3_a = Image.fromarray(array3).convert(mode = "1")
        
        
        add_1 = chops.logical_and(img1_a, img2_a)
        add_2 = chops.logical_and(add_1, img3_a)
        
        #display(add_2)
        
        return add_2
    
    def check_add_and_difference(self, img1, img2, img3):
        #print("inside check_add_and_difference" )
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img1 = Image.fromarray(array1).convert(mode = "1")
        img2 = Image.fromarray(array2).convert(mode = "1")
        img3 = Image.fromarray(array3).convert(mode = "1")
        
        t1 = chops.add(img1, img2)
        t2 = chops.difference(img3, img2)
        
        #display(t1)
        #display(t2)
        return self.check_same(t1, t2)
     
    def check_split_and_mirror(self, img1, img2):
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        #array3 = self.convert_img_to_array(img3)
        
        split_result = np.hsplit(array1, 2)
        
        part_1 = split_result[1]
        part_2 = split_result[0]
        
        '''
        im1 = Image.fromarray(part_1)
        im2 = Image.fromarray(part_2)
        im3 = chops.multiply(im1,im2)
        im3array = self.convert_img_to_array(im3)
        display(im3)
        
        part_1 = np.transpose(np.transpose(split_result[1]))
        part_2 = np.transpose(np.transpose(split_result[0]))
        '''
        
        split_soln = np.array_split(array2, 2, axis=1)
        soln_part_1 = split_soln[0]
        soln_part_2 = split_soln[1]
        
        
        
        #display(Image.fromarray(part_1).convert(mode = "1"))
        #print("--- ", part_1.shape)
        #display(Image.fromarray(part_2).convert(mode = "1"))
        #print("---", part_2.shape)
        #display(Image.fromarray(soln_part_1).convert(mode = "1"))
        #print("---", soln_part_1.shape)
        #display(Image.fromarray(soln_part_2).convert(mode = "1"))
        #print("---", soln_part_2.shape)
        
        #return (np.count_nonzero(actual_result_1) < self.flip_factor * actual_result_1.size and np.count_nonzero(actual_result_2) < self.flip_factor * actual_result_2.size)
        
        if(part_1.shape == soln_part_1.shape) and (part_2.shape == soln_part_2.shape):
            #print(part_1.size)
            t1 = (part_1 != soln_part_1).sum()
            t2 = (part_2 != soln_part_2).sum()
            #print("t1 =", t1)
            return self.split_factor * part_1.size > t1 and self.split_factor * part_2.size > t2
        
        else:
            return False
        
    
    def check_and(self, img1, img2, img3):
        #print("start andTest")
        #add_result = chops.difference(img1, img2)
        
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img1 = Image.fromarray(array1).convert(mode = "1")
        img2 = Image.fromarray(array2).convert(mode = "1")
        img3 = Image.fromarray(array3).convert(mode = "1")
        
        add_result = chops.logical_and(img1.convert(mode= "1"), img2.convert(mode= "1"))
        #display(add_result)
        #print("is same figure check_and =" , self.check_same(add_result,img3))
        return (self.check_same(add_result, img3))
    
    def check_or(self, img1, img2, img3):
        #add_result = chops.difference(img1, img2)
        
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        array3 = self.convert_img_to_array(img3)
        
        img1 = Image.fromarray(array1).convert(mode = "1")
        img2 = Image.fromarray(array2).convert(mode = "1")
        img3 = Image.fromarray(array3).convert(mode = "1")
        
        or_result = chops.logical_or(img1.convert(mode= "1"), img2.convert(mode= "1"))
        return (self.check_same(or_result, img3))
    
    def check_same(self, img1, img2, variation = None):
        #print("inside check_same")
        if variation == None:
            variation = 1.5
        #print("check same")
        
        img1 = img1.convert(mode = "L")#.filter(ImageFilter.SMOOTH_MORE)
        img2 = img2.convert(mode = "L")#.filter(ImageFilter.SMOOTH_MORE)
        #display("img1 = ", img1)
        #display("img2 = ", img2)
        
        change = chops.difference(img1, img2)
        #print("change = ", change)
        #display(change)
        diff = np.array(change)
        amt_change = np.count_nonzero(diff)
        #print(amt_change)
        
        #print("change = ", (amt_change/diff.size) * 100 )
        return ((amt_change/diff.size) * 100 < variation)
        
    def getAnswer(self, problem, figure1 , mapping):
        answerScore = []
        for j in range(1,7):
            optionImg = self.getImage(problem.figures[str(j)]) 
            prob_answer = chops.difference(figure1, optionImg)
            if(prob_answer == mapping):
                return j
            
        #answer = answerScore.index(min(answerScore)) + 1                    
        return -1
    
    def getImage(self, figure):
        image = Image.open(figure.visualFilename).convert("L")
        image = image.filter(ImageFilter.SMOOTH_MORE)
        
        return image
        
    def get_dark_pixel_ratio(self, image):
        nparray = self.convert_img_to_array(image)
        non_dark = np.count_nonzero(nparray)
        return (nparray.size - non_dark) / nparray.size
    
    def get_dark_pixel_count(self, image):
        nparray = self.convert_img_to_array(image)
        non_dark = np.count_nonzero(nparray)
        return (nparray.size - non_dark) 
        
    
    def convert_img_to_array(self, image):
        nparray = np.array(image)
        nparray[nparray >= 128] = 255
        nparray[nparray < 128] = 0
        return nparray
    
    def get_dark_pixel_quads_ratio(self, img1, img2):
        array1 = self.convert_img_to_array(img1)
        array2 = self.convert_img_to_array(img2)
        
        array1_split = np.vsplit(array1, 2)
        array1L = np.hsplit(array1_split[0], 2)
        array1R = np.hsplit(array1_split[1], 2)

        array2_split = np.vsplit(array2, 2)
        array2L = np.hsplit(array2_split[0], 2)
        array2R = np.hsplit(array2_split[1], 2)
        
        TL = np.count_nonzero(array1L[0]==array2L[0])
        BL = np.count_nonzero(array1R[0]==array2R[0])
        TR = np.count_nonzero(array1L[1]==array2L[1])
        BR = np.count_nonzero(array1R[1]==array2R[1])

        ratios = {}
        ratios['TL'] = (array1L[0].size - TL) / array1L[0].size
        ratios['TR'] = (array1R[0].size - TR) / array1R[0].size
        ratios['BL'] = (array1L[1].size - BL) / array1L[1].size
        ratios['BR'] = (array1R[1].size - BR) / array1R[1].size

        return ratios
    
    def get_dark_pixel_proportion(self, image1, image2, image3):
        dpr1 = self.get_dark_pixel_ratio(image1)
        dpr2 = self.get_dark_pixel_ratio(image2)
        dpr3 = self.get_dark_pixel_ratio(image3)
        
        if (dpr1 > 0.0 and dpr2 > 0.0 and dpr3 > 0.0):
            return ((dpr1/dpr2))/dpr3
        else:
            return 0.0
    
    def add_closest_quads_match(self, ab_quads, bc_quads, gh_quads, prop_arr):
        TL_ratio = ab_quads['TL'] + bc_quads['TL']
        TR_ratio = ab_quads['TR'] + bc_quads['TR']
        BL_ratio = ab_quads['BL'] + bc_quads['BL']
        BR_ratio = ab_quads['BR'] + bc_quads['BR']
        
        sol_TL_ratio = []
        sol_TR_ratio = []
        sol_BL_ratio = []
        sol_BR_ratio = []
        
        for i in range(0,8):
            sol_TL_ratio.append(gh_quads['TL'] + (prop_arr[i])['TL'])
            sol_TR_ratio.append(gh_quads['TR'] + (prop_arr[i])['TR'])
            sol_BL_ratio.append(gh_quads['BL'] + (prop_arr[i])['BL'])
            sol_BR_ratio.append(gh_quads['BR'] + (prop_arr[i])['BR'])
            
        
        for i in range(0,8):
            sol_TL_ratio[i] = abs((prop_arr[i])['TL'] - TL_ratio)
            sol_TR_ratio[i] = abs((prop_arr[i])['TR'] - TR_ratio)
            sol_BL_ratio[i] = abs((prop_arr[i])['BL'] - BL_ratio)
            sol_BR_ratio[i] = abs((prop_arr[i])['BR'] - BR_ratio)
    
        min_TL= min(sol_TL_ratio)
        min_TR= min(sol_TR_ratio)
        min_BL= min(sol_BL_ratio)
        min_BR= min(sol_BR_ratio)
        
        TL_indices = [i for i, v in enumerate(sol_TL_ratio) if v == min_TL]
        TR_indices = [i for i, v in enumerate(sol_TR_ratio) if v == min_TR]
        BL_indices = [i for i, v in enumerate(sol_BL_ratio) if v == min_BL]
        BR_indices = [i for i, v in enumerate(sol_BR_ratio) if v == min_BR]
        
        '''
        print("TL_indices = ", TL_indices)
        print(TR_indices)
        print(BL_indices)
        print(BR_indices)
        '''
        idx = (set(TL_indices).intersection(set(TR_indices)).intersection(set(BL_indices)).intersection(BR_indices))
        
        if len(idx) == 0:
            return None
        else:
            #print("idx = ", idx)
            return((list(idx))[0])
        
    def check_pixels_doubled(self, img1, img2):
        print("check_pixels_doubled")
        array1  = self.convert_img_to_array(img1)
        array2  = self.convert_img_to_array(img2)
        
        pixels_1 = array1.size - np.count_nonzero(array1)
        pixels_2 = array2.size - np.count_nonzero(array2)
        
        if pixels_2 == 2 * pixels_1:
            #print("returning true")
            return True
        else:
            #print("pixels = ", pixels_1)
            #print("pixels = ", pixels_2)
            #print("pixels = ", pixels_1 * 2)
            return False
        
    def check_pixels_tripled(self, img1, img2):
        print("check_pixels_tripled")
        array1  = self.convert_img_to_array(img1)
        array2  = self.convert_img_to_array(img2)
        
        pixels_1 = array1.size - np.count_nonzero(array1)
        pixels_2 = array2.size - np.count_nonzero(array2)
        
        diff = abs(pixels_2 - 3 * pixels_1)
        print("diff = ", diff)
        if diff < 150:
            print("returning true")
            return True
        else:
            '''
            print("pixels = ", pixels_1)
            print("pixels = ", pixels_2)
            print("pixels = ", pixels_1 * 3)
            '''
            return False
    
    def sum_pixels(self, img1, img2, img3):
        #print("inside sum_pixels")
        array1  = self.convert_img_to_array(img1)
        array2  = self.convert_img_to_array(img2)
        array3  = self.convert_img_to_array(img3)
        
        pixels_1 = array1.size - np.count_nonzero(array1)
        pixels_2 = array2.size - np.count_nonzero(array2)
        pixels_3 = array2.size - np.count_nonzero(array3)
        
        
        return pixels_1 + pixels_2 + pixels_3
        
    def is_close_sum(self, sum_1, sum_2):
        
        diff = abs(sum_1 - sum_2)
        if diff < 270:
            print("returning true")
            return True
        else:
            print("difference = " , diff)
            return False
        
    
    '''
    def get_closest(self, a_list, a_number):
        min(a_list, key=lambda x:abs(x - a_Number))
    '''    
    def transform(self, figure1 , figure2):
        objA = figure1.objects
        objB = figure2.objects
        mapping = {}
        obj_mapping = {}
        objLen = 0 #Number of objects 
        diffObjs = 0 #Difference in number of objects
        
        if (len(objA) != len(objB)):
            diffObjs = len(objA) - len(objB)
            objLen = len(objB)
        
            if diffObjs < 0:
                diffObjs = len(objB) - len(objA)
                objLen = len(objA)
        else:
            diffObjs = 0
            objLen = len(objA)
        
        #build mapping for each object 
        for j in range(objLen):
            #print "lengths of objects is 1"
            objA_key = sorted(objA.keys())
            attributes_A = objA[objA_key[j]].attributes.keys()
            
            
            objB_key = sorted(objB.keys())
            attributes_B = objB[objB_key[j]].attributes.keys()
            
            commonAttribs = self.findCommonAttributes(attributes_A, attributes_B)
            
            #print("keys = ", keys)
            mapping = {}
            for i in range(len(commonAttribs)):
                #print("A feature = ", (objA[objA_key[0]].attributes)[commonAttribs[i]])
                #print("B feature = ", (objB[objB_key[0]].attributes)[commonAttribs[i]])
                if ((objA[objA_key[j]].attributes)[commonAttribs[i]] == (objB[objB_key[j]].attributes)[commonAttribs[i]]):
                    mapping[commonAttribs[i]] = "SAME"
                elif commonAttribs[i] == 'angle':
                    mapping[commonAttribs[i]] = abs(int((objA[objA_key[j]].attributes)[commonAttribs[i]]) - int((objB[objB_key[j]].attributes)[commonAttribs[i]]))
                elif commonAttribs[i] == 'alignment':
                    mapping['alignment1'] = self.getAlignment1((objA[objA_key[j]].attributes)[commonAttribs[i]],(objB[objB_key[j]].attributes)[commonAttribs[i]])
                    mapping['alignment2'] = self.getAlignment2((objA[objA_key[j]].attributes)[commonAttribs[i]],(objB[objB_key[j]].attributes)[commonAttribs[i]])
                else:
                    mapping[commonAttribs[i]] = (objA[objA_key[j]].attributes)[commonAttribs[i]]+"|"+(objB[objB_key[j]].attributes)[commonAttribs[i]]
                
                if 'above' in mapping:
                    del mapping['above']
                if 'inside' in mapping:
                    del mapping['inside']
            #print(mapping) 
            obj_mapping[j] = mapping  
        
        
        #add mapping for extra objects
        nn = len(obj_mapping) 
        if(diffObjs != 0):
            if(len(objB) > len(objA)):
                attributes_B = objB[objB_key[nn]].attributes.keys()
                for key in attributes_B:
                    mapping[key] = ("|"+ (objB[objB_key[nn]].attributes)[key])
            else:
                attributes_A = objA[objA_key[nn]].attributes.keys()
                for key in attributes_A:
                    mapping[key] = ("|"+(objA[objA_key[nn]].attributes)[key])
       
        obj_mapping[j] = mapping          
        
        return obj_mapping
    
    def getAnswer_2_by_2(self, problem, figure1 , mapping):
        answerScore = []
        for j in range(1,7):
            option = problem.figures[str(j)] 
            option_map = self.transform(figure1, option)
            #print("solution ", j)
            answerScore.append(self.getScore(mapping,option_map))
        
        #print(answerScore)
        answer = answerScore.index(min(answerScore)) + 1                    
        return answer
    
    def findCommonAttributes(self, listA, listB):
        a_set = set(listA) 
        b_set = set(listB) 
        if (a_set & b_set): 
            return  list(a_set & b_set)
        else: 
            return None
        
    def getBetterTransformation(self, figA, figB, figC):
        objA = figA.objects
        objB = figB.objects
        objC = figC.objects
        
        if len(objA) != len(objB):
            return 'B'
        elif len(objA) != len(objC):
            return 'C'
        else:
            return 'B'
        
    def getScore(self, map1, map2):
        #print(map1)
        #print(map2)
        diff = 0
        map1Len = len(map1)
        map2Len = len(map2)
        objLen = 0
        if map1Len > map2Len:
            objLen = map2Len
        else:
            objLen = map1Len
            
        for i in range(objLen):
            for keys in map1[i]:
                if keys in map2[i] and map1[i][keys] == map2[i][keys]:
                    diff += 0
                else:
                    diff += 1
            
        return diff
    
    def getAlignment1(self, str1, str2):
        if ("-" in str1 and "-" in str2):
            if str1[ str1.index("-") + 1 : ] == str2[str2.index("-") + 1 : ]:
                return "SAME"
            else:
                return str1[str1.index("-") + 1 : ] + "|" + str2[ str2.index("-") + 1 : ]
            
        else:
            return str1 + "|" + str2
        
    def getAlignment2(self, str1, str2):
        if ("-" in str1 and "-" in str2):
            if str1[ : str1.index("-")] == str2[: str2.index("-")]:
                return "SAME"
            else:
                return str1[ : str1.index("-")] + "|" + str2[: str2.index("-")]
            
        else:
            return str1 + "|" + str2
        
    def check_dark_pixel_ratio_increase_2(self, image1, image2):
        dpr1 = self.get_dark_pixel_ratio(image1)
        dpr2 = self.get_dark_pixel_ratio(image2)
        
        #check difference and return true only if the increase is not significant
        '''
        print("ratios")
        print("image1 = ",dpr1)
        print("image2 = ",dpr2)
        '''
        if(dpr2 > dpr1):
            return True
        else:
            return False
    
    
                   