from math import floor
import numpy as np

from Robot.joint_state import JointState

class Environment:
    def __init__(self, robot, obstacles, targets, initial_state = None, epsilon = 0.5, is_floor = True, is_wall = False):
        self.robot = robot
        self.obstacles = obstacles
        self.targets = targets
        self.initial_state = initial_state if initial_state is not None else self.robot.joint_values
        self.robot.forward_kinematics()
        self.epsilon = epsilon
        self.is_floor = is_floor
        self.is_wall = is_wall
        self.floor = np.array([[-1,0],[1,0]])*self.robot.n_dof*self.robot.link_length + np.array([[0,-0.1],[0,-0.1]]) if self.is_floor else None
        self.wall = np.array([[0,-1],[0,1]])*self.robot.n_dof*self.robot.link_length + np.array([[-0.1,0],[-0.1,0]]) if self.is_wall else None
        print("wall = ", self.wall)

    def distance(self, p1, p2):
        return np.linalg.norm(p2-p1)

    def query_boundary_collision(self):
        if self.is_floor:
            for i in range(len(self.robot.joint_positions)-1):  
                self.query_segment_collision(self.floor[0], self.floor[1],self.robot.joint_positions[i], self.robot.joint_positions[i+1])
            self.query_segment_collision(self.floor[0], self.floor[1],self.robot.joint_positions[-1], self.robot.gripper_position)

        if self.is_wall:
            for i in range(len(self.robot.joint_positions)-1):  
                self.query_segment_collision(self.wall[0], self.wall[1],self.robot.joint_positions[i], self.robot.joint_positions[i+1])
            self.query_segment_collision(self.wall[0], self.wall[1],self.robot.joint_positions[-1], self.robot.gripper_position)
            

    # def on_segment(self,p,q,r):
    #     if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0],r[0]))) and ((q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1],r[1]))):
    #         return True
    #     return False


    # def orientation(self, p, q, r):
    #     val = float(q[1]-p[1])*(r[0]-q[0])-float(q[0]-p[0])*(r[1]-q[1])
    #     if val > 0:
    #         return 1 #clockwise
    #     elif val < 0:
    #         return 2 #anticlockwise
    #     else:
    #         return 0 #colinear

    # Given three collinear points p, q, r, the function checks if 
    # point q lies on line segment 'pr' 
    def onSegment(self, p, q, r):
        if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False
    
    def orientation(self, p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/ 
        # for details of below formula. 
        
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):
            
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0
    
    # The main function that returns true if 
    # the line segment 'p1q1' and 'p2q2' intersect.
    def query_segment_collision(self, p1,q1,p2,q2):
        
        # Find the 4 orientations required for 
        # the general and special cases
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)
    
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True
    
        # Special Cases
    
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and self.onSegment(p1, p2, q1)):
            return True
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and self.onSegment(p1, q2, q1)):
            return True
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and self.onSegment(p2, p1, q2)):
            return True
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and self.onSegment(p2, q1, q2)):
            return True
    
        # If none of the cases
        return False

    def triangle_area(self, a, b, c):
        ab = np.array([b[0]-a[0], b[1]-a[1]])
        ac = np.array([c[0]-a[0], c[1]-a[1]])
        
        return abs(np.cross(ab, ac))/2

    # def query_segment_collision(self,p1,q1,p2,q2):
      
    #     # Find the 4 orientations required for 
    #     # the general and special cases
    #     o1 = self.orientation(p1, q1, p2)
    #     o2 = self.orientation(p1, q1, q2)
    #     o3 = self.orientation(p2, q2, p1)
    #     o4 = self.orientation(p2, q2, q1)
    
    #     # General case
    #     if ((o1 != o2) and (o3 != o4)):
    #         return True
    
    #     # Special Cases
    
    #     # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    #     if ((o1 == 0) and self.on_segment(p1, p2, q1)):
    #         return True
    
    #     # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    #     if ((o2 == 0) and self.on_segment(p1, q2, q1)):
    #         return True
    
    #     # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    #     if ((o3 == 0) and self.on_segment(p2, p1, q2)):
    #         return True
    
    #     # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    #     if ((o4 == 0) and self.on_segment(p2, q1, q2)):
    #         return True
    
    #     # If none of the cases
    #     return False

    def query_link_collision(self, radius, o, p1, p2):
        #this code which has been edited out checks between line and circle,
        #whereas the other code is between line-SEGMENT and circle
        # min_dist = 2*self.triangle_area(o, p1, p2)/self.distance(p1, p2)
        # if min_dist <= radius:
        #     return True
        # return False

        o_p1 = p1-o
        o_p2 = p2-o
        p1_p2 = p2-p1

        min_dist = np.Inf
        max_dist = max(self.distance(o,p1), self.distance(o,p2))          

        # if o_p1.dot(p1_p2) > 0 and o_p2.dot(p1_p2) > 0:
        if np.dot(p1-o, p1-p2) > 0 and np.dot(p2-o,p2-p1) > 0:
            min_dist = 2*self.triangle_area(o, p1, p2)/self.distance(p1, p2)
        else:
            min_dist = min(self.distance(o, p1), self.distance(o,p2))

        if min_dist <= radius and max_dist >= radius:
            return True
        else:
            return False

    def query_robot_collision(self):
        for i in range(len(self.obstacles)):
            for j in range(len(self.robot.joint_positions)-1):
                if self.query_link_collision(self.obstacles[i].radius, self.obstacles[i].centre, self.robot.joint_positions[j], self.robot.joint_positions[j+1]):
                    # print(f"collision at link {j+1}")
                    return True
            if self.query_link_collision(self.obstacles[i].radius, self.obstacles[i].centre, self.robot.joint_positions[-1], self.robot.gripper_position):
                # print(f"collision at link {self.robot.n_dof}")
                return True
        collide = self.query_boundary_collision()
        if collide is True:
            print("colided with floor or wall")
        return False

    def query_robot_at_goal(self):
        for target in self.targets:
            if self.distance(self.robot.gripper_position, target) <= self.epsilon:
                return True
        return False


    