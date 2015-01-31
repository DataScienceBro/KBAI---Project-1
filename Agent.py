# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self,problem):
        print "Working on problem", problem.getName()
        
        #set default answer
        answer = []
        #Get Figures
        A = problem.getFigures().get("A")
        B = problem.getFigures().get("B")
        C = problem.getFigures().get("C")
        one = problem.getFigures().get("1")
        two = problem.getFigures().get("2")
        three = problem.getFigures().get("3")
        four = problem.getFigures().get("4")
        five = problem.getFigures().get("5")
        six = problem.getFigures().get("6")

        #generate transformation relationships between frames
        AtoB = self.getRelationships(A,B)
        Cto1 = self.getRelationships(C,one)
        Cto2 = self.getRelationships(C,two)
        Cto3 = self.getRelationships(C,three)
        Cto4 = self.getRelationships(C,four)
        Cto5 = self.getRelationships(C,five)
        Cto6 = self.getRelationships(C,six)

        possible = {"1":Cto1, "2":Cto2, "3":Cto3, "4":Cto4, "5":Cto5, "6":Cto6}

        #Choose answers C-># with same transformations as A->B
        for name,rels in possible.iteritems():
            if AtoB == rels:
                #print "match found!"
                #print rels
                answer.append(name)
        print "before positions", answer
        #if there is more than one possible answer, compare relative positions of objects in B with solutions
        if len(answer) > 1:
            #generate positional relationships in frames B and 1-6
            B_pos = self.getPositions(B)
            one_pos = self.getPositions(one)
            two_pos = self.getPositions(two)
            three_pos = self.getPositions(three)
            four_pos = self.getPositions(four)
            five_pos = self.getPositions(five)
            six_pos = self.getPositions(six)

            possible = {"1":one_pos, "2":two_pos, "3":three_pos, "4":four_pos, "5":five_pos, "6":six_pos}
            #eliminate answers not in answer
            for k in possible.keys(): 
                if k not in answer:
                    del possible[k]
            #eliminate answers with different positions than B
            B_pos = sorted(B_pos)
            for name,positions in possible.iteritems():
                if B_pos != sorted(positions):
                    answer.remove(name)
                    
        
        print "Answer:", answer
        return min(answer) if len(answer) > 0 else "7" #pick one randomly if multiple answers left





    def getRelationships(self,A,B):
        #generates a dictionary of lists of relations between each object A->B
        A_Objs = A.getObjects()
        B_Objs = B.getObjects()


            


        rels = {}
        A_names = [A_Obj.getName() for A_Obj in A_Objs]
        B_names = [B_Obj.getName() for B_Obj in B_Objs]
        
        for A_name,B_name in [ (n if n in A_names else None, n if n in B_names else None) for n in set(A_names + B_names)]:
            #print A_name,B_name
            if A_name:
                for n in A_Objs:
                    if n.getName() == A_name:
                        A_Obj = n
            else:
                A_Obj = None
            if B_name:
                for n in B_Objs:
                    if n.getName() == B_name:
                        B_Obj = n
            else:
                A_Obj = None

            if not A_name:
                #obj was added to b
                rels[B_name] = []
                rels[B_name].append("added")
            elif not B_name:
                #obj was deleted from a
                rels[A_name] = []
                rels[A_name].append("deleted")
            else:
                rels[B_name] = []
                A_atts = {}
                B_atts = {}
                for A_att,B_att in zip(A_Obj.getAttributes(),B_Obj.getAttributes()):
                    A_atts[A_att.getName()] = A_att.getValue()
                    B_atts[B_att.getName()] = B_att.getValue()

                #now for some attribute rules:
                try:
                    if A_atts["shape"] == B_atts["shape"]:
                        rels[B_Obj.getName()].append("shapeSame")
                    else:
                        rels[B_Obj.getName()].append("shapeDiff")
                except KeyError:
                    pass

                try:
                    if A_atts["size"] == B_atts["size"]:
                        rels[B_Obj.getName()].append("sizeSame")
                    else:
                        rels[B_Obj.getName()].append("sizeDiff")
                except KeyError:
                    pass

                try:
                    if A_atts["fill"] == B_atts["fill"]:
                        rels[B_Obj.getName()].append("fillSame")
                    else:
                        rels[B_Obj.getName()].append(A_atts["fill"] + B_atts["fill"])
                except KeyError:
                    pass

                try:
                    A_atts["angle"]
                except KeyError:
                    try:
                        B_atts["angle"]
                    except KeyError:
                        rels[B_Obj.getName()].append("angleSame") #neither have angle
                    else:
                        rels[B_Obj.getName()].append("angleDiff") #only B has angle
                else:
                    try:
                        B_atts["angle"]
                    except KeyError:
                        rels[B_Obj.getName()].append("angleDiff") #only A has angle
                    else:
                        if A_atts["angle"] == B_atts["angle"]:
                            rels[B_Obj.getName()].append("angleSame")
                        else:
                            rels[B_Obj.getName()].append("angleDiff")
                        
##                "vertical-flip"
        print rels
        return rels

    def getPositions(self,A):
        A_Objs = A.getObjects()
        A_names = [A_Obj.getName() for A_Obj in A_Objs]
        pos = []
        for A_Obj in A_Objs:
            A_atts = A_Obj.getAttributes()
            objpos = []
           # print A_atts
            
            for att in A_atts:
            
                try:
                    if att.getName() == "inside":
                        objpos.append("inside")
                except KeyError:
                    pass

                try:
                    if att.getName() == "above":
                        objpos.append("above")
                except KeyError:
                    pass

                try:
                    if att.getName() == "left-of":
                        objpos.append("left-of")
                except KeyError:
                    pass
                try:
                    if att.getName() == "overlaps":
                        objpos.append("overlaps")
                except KeyError:
                    pass
            pos.append(objpos)
      
        print pos
        return pos
