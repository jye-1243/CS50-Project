import Brain
import operator

class Dot(object):
    def __init__(self, w, h):
        self.brain = Brain(1000)
        pos = (w/2, h - 10)
        self.w = w
        self.h = h
        vel = (0,0)
        acc = (0,0)
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0

    def show(self):
        if self.isBest:
            print("woo!")


    def move(self):
        if self.brain.size > self.brain.step:
            self.acc = self.brain.directions[self.brain.step]
        else:
            self.dead = True

        self.vel = tuple(map(operator.add, self.vel, self.acc))
        mag = self.vel[0] * self.vel[0] + self.vel[1] * self.vel[1]
        if mag > 5:
            self.vel = tuple(i * 5 / mag for i in self.vel)
        self.pos = tuple(map(operator.add, self.pos, self.vel))
        
    def update(self, goalx, goaly):
        if not self.dead and not self.reachedGoal:
            self.move()
            if self.pos[0] < 2 or self.pos[1] < 2 or self.pos[0] > self.w-2 or self.pos[1] > self.h - 2:
                self.dead = True
            elif math.sqrt((goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])) < 5:
                self.reachedGoal = True
            elif self.pos[0] < 600 and self.pos[1] < 310 and self.pos[0] > 0 and self.pos[1] > 300:
                self.dead = True

    def calculateFitness(self, goalx, goaly):
        if self.reachedGoal:
            self.fitness = 1/16 + 10000 * self.brain.step * self.brain.step
        else:
            dist = (goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])
            self.fitness = 1/dist

    def makeBaby(self):
        baby = Dot(self.w, self.h)
        baby.brain = self.brain.clone()
        return baby



