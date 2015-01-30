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
        answer = "7"
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

        #generate relationships between frames
        AtoB = self.getRelationships(A,B)
        Cto1 = self.getRelationships(C,one)
        Cto2 = self.getRelationships(C,two)
        Cto3 = self.getRelationships(C,three)
        Cto4 = self.getRelationships(C,four)
        Cto5 = self.getRelationships(C,five)
        Cto6 = self.getRelationships(C,six)

        possible = {"1":Cto1, "2":Cto2, "3":Cto3, "4":Cto4, "5":Cto5, "6":Cto6}
##        for name,rels in possible.iteritems():
##            print rels
        #pick best frame
        for name,rels in possible.iteritems():
            if AtoB == rels:
                print "match found!"
                #print rels
                answer = name
                break #TODO INSTEAD OF BREAKING COMPARE POSSIBLE SOLNS
        
        print "Answer:", answer
        return answer

    def getRelationships(self,A,B):
        #generates a dictionary of lists of relations between each object A->B
        A_Objs = A.getObjects()
        B_Objs = B.getObjects()


            


        rels = {}
        A_names = [A_Obj.getName() for A_Obj in A_Objs]
        B_names = [B_Obj.getName() for B_Obj in B_Objs]
        
        for A_name,B_name in [ (n if n in A_names else None, n if n in B_names else None) for n in set(A_names + B_names)]:
            print A_name,B_name
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
                        rels[B_Obj.getName()].append("fillDiff")
                except KeyError:
                    pass

                try:
                    if A_atts["angle"] == B_atts["angle"]:
                        rels[B_Obj.getName()].append("angleSame")
                    else:
                        rels[B_Obj.getName()].append("angleDiff")
                except KeyError:
                    pass
    ##                "above"
    ##                "vertical-flip"
    ##                "inside"
    ##                "left-of"
    ##                "overlaps"
        print rels
        return rels
            
