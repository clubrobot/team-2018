import time
class AutomateTools:
    stopThisAction="stop"

    @staticmethod
    def myWait(robot,action):
        try:
            robot.wait()
        except :
            print("Patinage")
            robot.set_velocities(-300,0)
            time.sleep(0.2)
            r = action()
            if(r==AutomateTools.stopThisAction):
                return
            AutomateTools.myWait(robot,action)

    @staticmethod
    def myTurnonthespot(robot,theta):
        func = lambda : robot.turnonthespot(theta) 
        func()
        AutomateTools.myWait(robot,func)

    @staticmethod
    def myPurepursuite(robot,path,direction="forward"):
        func = lambda : robot.purepursuit(path,direction)
        func()
        AutomateTools.myWait(robot,func)

    #follow path and do the pick
    @staticmethod
    def myGrab(robot,funcGrab,path=None):
        if not (path is None):
            AutomateTools.myPurepursuite(robot,path)
        print("picking")
        funcGrab()
        AutomateTools.myWait(robot,lambda : AutomateTools.myGrab(robot,funcGrab,path))
        
    @staticmethod
    def myFire(waterLauncher):
        pass
       #waterLauncher.fire_all()

    @staticmethod
    def myDrop(waterSorter):
        pass
        #waterSorter.drop_all()