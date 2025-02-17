from manim import *
import math
import random

# Set a random seed for reproducibility
random.seed(1)
r = math.ceil(random.random() * 1000)  # Random value for testing

fsize = 25

# Pseudorandom deterministic function
def rand(n, upper):
    return (hash(n + r) % (upper - 1)) + 1

# Kangaroo algorithm
def kangaroo(alpha, beta, n, a, b):
    print(alpha, beta, n, a, b)
    trapSteps = math.ceil(math.sqrt((b - a) / 2))  # Heuristic tame trap steps
    #trapSteps = 4
    # Output of the random number generator for steps
    upperStep = math.ceil(math.sqrt((b - a))*1.5)

    # Tame kangaroo
    xTame = pow(alpha, b, n)  # Trap
    dTame = 0  # Distance traveled
    tame_steps = []

    for i in range(trapSteps):
        step = rand(xTame, upperStep)  # Random step
        xTame = (xTame * pow(alpha, step, n)) % n
        dTame += step
        tame_steps.append((xTame, dTame, step))  # Include step in the tuple

    # Wild kangaroo
    yWild = beta  # Start at beta
    dWild = 0  # Distance traveled
    wild_steps = []
    i = 0

    while dWild <= b - a + dTame:
        step = rand(yWild, upperStep)  # Random step
        yWild = (yWild * pow(alpha, step, n)) % n
        dWild += step
        wild_steps.append((yWild, dWild, step))  # Include step in the tuple

        if yWild == xTame:  # Wild kangaroo trapped
            return tame_steps, wild_steps, dTame, dWild, i
        i += 1

    raise Exception("failed to reach trap.")

class KangarooAnimation(Scene):
    def construct(self):
        g = 2
        n = 17
        secret = 3
        beta = pow(g, secret, n)

        trapSteps = math.ceil(math.sqrt((n) / 2))  # Heuristic tame trap steps
        #trapSteps = 4
        # Output of the random number generator for steps
        upperStep = math.ceil(math.sqrt((n))*1.5)
        # Run the kangaroo algorithm
        try:
            tame_steps, wild_steps, dTame, dWild, wild_steps_count = kangaroo(
                g, beta, n, 0, n)
            print(tame_steps, "\n\n")
            print(wild_steps, "\n\n")
        except Exception as e:
            print("failed:", e)
            return

        # Create circles for the cyclic group
        circle_radius = 3
        num_members = n - 1
        circle_center = ORIGIN + 3 * RIGHT
        status_center = ORIGIN + 3.4 * LEFT + 3 * UP

        general_status = MathTex(
            f"\\alpha={g}, n={(n%n) + 1}, x={secret}").move_to(status_center)
        self.add(general_status)
        problem_desc = MathTex(f"\\beta \\equiv {g}^{secret} \mod {n} \equiv {beta}").next_to(
                    general_status, DOWN)
        self.add(problem_desc)


        # Create the members of the cyclic group
        members = [circle_center + circle_radius * np.array([np.cos(2 * PI * i / num_members), np.sin(
            2 * PI * i / num_members), 0]) for i in range(num_members)]
        member_circles = [Circle(radius=0.3, color=BLUE).move_to(
            member) for member in members]
        member_labels = [MathTex(str(i)).move_to(member)
                         for i, member in enumerate(members)]

        # Add members to the scene
        for circle, label in zip(member_circles, member_labels):
            self.add(circle, label)

        # Animate the tame kangaroo
        dist_status = MathTex(f"d_T = 0, x_T = {pow(g, n, n)}").next_to(problem_desc, DOWN*2)
        self.add(dist_status)
        next_step = MathTex(f"step = f({pow(g, n, n)}) = {rand(pow(g, n, n), upperStep)}").next_to(dist_status, DOWN)
        self.add(next_step)
        next_x = MathTex(f"x_T = {pow(g, n, n)} * \\alpha ^ {rand(pow(g, n, n), upperStep)} \mod {n} = {((pow(g,n, n))*pow(g, rand(pow(g, n, n), upperStep), n)) % n}").next_to(next_step, DOWN)
        self.add(next_x)

        kangaroo_status = Text(f"Tame kangaroo is taking {trapSteps} steps.", font_size=fsize).next_to(next_x, DOWN*1.5)
        self.add(kangaroo_status)

        self.wait(1)

        tame_arrows = []
        for i, (xTame, dTame, step) in enumerate(tame_steps):
            start = members[tame_steps[i - 1][0]] if i > 0 else members[pow(g, n, n)]
            end = members[xTame]

            tame_arrow = CurvedArrow(
                start_point=start, end_point=end, color=GREEN, radius=-10)
            tame_arrows.append(tame_arrow)

            # Animate the creation of the arrow
            self.play(Create(tame_arrows[-1]), run_time=0.5)
            self.wait(0.1)

            updated_dist_status = MathTex(f"d_T = {dTame}, x_T = {xTame}").move_to(dist_status.get_center())
            self.play(Transform(dist_status, updated_dist_status))
            self.wait(0.5)

            if i == len(tame_steps) - 1:
                break

            updated_next_step = MathTex(f"step = f({xTame}) = {rand(xTame, upperStep)}").move_to(next_step.get_center())
            self.play(Transform(next_step, updated_next_step))
            self.wait(0.5)

            updated_next_x = MathTex(f"x_T = {xTame} * \\alpha ^ {rand(xTame, upperStep)} \mod {n} = {((xTame*pow(g, rand(xTame, upperStep), n)) % n)}").move_to(next_x.get_center())
            self.play(Transform(next_x, updated_next_x))
            self.wait(0.5)

        trap_circle = Circle(radius=0.58, color=RED).move_to(members[tame_steps[-1][0]])
        updated_kangaroo_status = Text(f"Tame kangaroo set a trap at {tame_steps[-1][0]}.", font_size=fsize).move_to(kangaroo_status.get_center())

        updated_kangaroo_status = Text(f"Wild kangaroo hopping until caught.", font_size=fsize).move_to(kangaroo_status.get_center())

        updated_dist_status = MathTex(f"d_W = {0}, y_W = {beta}").move_to(dist_status.get_center())

        updated_next_step = MathTex(f"step = f({beta}) = {rand(beta, upperStep)}").move_to(next_step.get_center())

        updated_next_x = MathTex(f"y_W = {beta} * \\alpha ^ {rand(beta, upperStep)} \mod {n} = {((beta*pow(g, rand(beta, upperStep), n)) % n)}").move_to(next_x.get_center())
        updated_general_status = MathTex(f"\\alpha = {g}, n = {n}, x={secret}, d_T={tame_steps[-1][1]}").move_to(general_status.get_center())
        self.play(Transform(general_status, updated_general_status), Transform(next_x, updated_next_x), Transform(kangaroo_status, updated_kangaroo_status), Transform(next_step, updated_next_step), Transform(dist_status, updated_dist_status), Transform(general_status, updated_general_status), Transform(kangaroo_status, updated_kangaroo_status), Create(trap_circle))
        self.wait(2)
        # Animate the wild kangaroo
        wild_arrows = []
        for i, (yWild, dWild, step) in enumerate(wild_steps):
            start = members[wild_steps[i - 1][0]] if i > 0 else members[beta]
            end = members[yWild]
            wild_arrow = Arrow(start=start, end=end,
                               color=RED, buff=0.3, stroke_width=3)
            wild_arrows.append(wild_arrow)

            # Animate the creation of the arrow
            self.play(Create(wild_arrows[-1]), run_time=0.5)
            self.wait(0.1)

            updated_dist_status = MathTex(f"d_W = {dWild}, y_W = {yWild}").move_to(dist_status.get_center())
            self.play(Transform(dist_status, updated_dist_status))
            self.wait(0.5)

            if i == len(wild_steps) - 1:
                break

            updated_next_step = MathTex(f"step = f({yWild}) = {rand(yWild, upperStep)}").move_to(next_step.get_center())
            self.play(Transform(next_step, updated_next_step))
            self.wait(0.5)

            updated_next_x = MathTex(f"y_W = {yWild} * \\alpha ^ {rand(yWild, upperStep)} \mod {n} = {((yWild*pow(g, rand(yWild, upperStep), n)) % n)}").move_to(next_x.get_center())
            self.play(Transform(next_x, updated_next_x))
            self.wait(0.5)

        updated_kangaroo_status = Text("Wild kangaroo caught!", font_size=fsize).move_to(kangaroo_status.get_center())
        success_circle =Circle(radius=0.25, color=YELLOW).move_to(members[(tame_steps[-1][0]) % n])

        # Show the final result
        updated_dist_status = MathTex(f"x = b + d_T - d_W \\mod n").move_to(dist_status.get_center())
        updated_next_step = MathTex(f"{n} + {tame_steps[-1][1]} - {wild_steps[-1][1]} \\mod {n} = {secret}").move_to(next_step.get_center())
        self.play(Transform(kangaroo_status, updated_kangaroo_status), FadeOut(next_x), Create(success_circle), Transform(dist_status, updated_dist_status), Transform(next_step, updated_next_step))
        self.wait(3)

        # Clean up the scene
        self.play(FadeOut(trap_circle, success_circle, problem_desc, dist_status, general_status, next_step, kangaroo_status, *tame_arrows, *wild_arrows, *member_circles, *member_labels), run_time=1)
        self.wait(1)
