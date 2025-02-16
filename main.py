from manim import *
import math
import random
from telnetlib import OUTMRK

# Set a random seed for reproducibility
random.seed(792)
r = math.ceil(random.random() * 1000)  # Random value for testing

# Pseudorandom deterministic function
def rand(n, upper):
    return (hash(n + r) % (upper - 1)) + 1

# Kangaroo algorithm
def kangaroo(alpha, beta, n, a, b):
    trapSteps = math.floor(math.sqrt((b - a) / 2))  # Heuristic tame trap steps
    # trapSteps = 4
    # Output of the random number generator for steps
    upperStep = math.floor(math.sqrt((b - a) / 2))

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

        # Run the kangaroo algorithm
        try:
            tame_steps, wild_steps, dTame, dWild, wild_steps_count = kangaroo(
                g, beta, n, 0, n)
        except Exception as e:
            print("failed:", e)
            return

        # Create circles for the cyclic group
        circle_radius = 3
        num_members = n - 1
        circle_center = ORIGIN + 3 * RIGHT
        status_center = ORIGIN + 4 * LEFT + 3 * UP

        general_status = MathTex(
            f"\\alpha={g}, n={n}, x={secret}").move_to(status_center)
        self.add(general_status)
        problem_desc = MathTex(f"\\beta \\equiv {g}^{secret} \mod {n} \equiv {beta}").next_to(
                    general_status, DOWN)
        self.add(problem_desc)


        # Create the members of the cyclic group
        members = [circle_center + circle_radius * np.array([np.cos(2 * PI * i / num_members), np.sin(
            2 * PI * i / num_members), 0]) for i in range(num_members)]
        member_circles = [Circle(radius=0.3, color=BLUE).move_to(
            member) for member in members]
        member_labels = [MathTex(str(i + 1)).move_to(member)
                         for i, member in enumerate(members)]

        # Add members to the scene
        for circle, label in zip(member_circles, member_labels):
            self.add(circle, label)

        # Animate the tame kangaroo
        dist_status = MathTex(f"d_T = 0, x_T = {n-1}").next_to(problem_desc, DOWN*2)
        self.add(dist_status)
        next_step = MathTex(f"step = f({n-1}) = {rand(n-1, n)}").next_to(dist_status, DOWN)
        self.add(next_step)
        next_x = MathTex(f"x_T = x_T \\alpha ^({rand(n-1, n)}) \mod {n} = {pow(n-1, rand(n-1, n), n)}").next_to(next_step, DOWN)
        self.add(next_x)

        tame_arrows = []
        for i, (xTame, dTame, step) in enumerate(tame_steps):
            start = members[tame_steps[i - 1][0] -
                            1] if i > 0 else members[((n-1) % n) - 1]
            end = members[xTame - 1]

            tame_arrow = CurvedArrow(
                start_point=start, end_point=end, color=GREEN, radius=-10)
            tame_arrows.append(tame_arrow)

            updated_dist_status = MathTex(f"d_T = {dTame}, x_T = {xTame}").move_to(dist_status.get_center())
            self.play(Transform(dist_status, updated_dist_status))
            self.wait(0.5)

            updated_next_step = MathTex(f"step = f(x_T) = {rand(xTame, n)}").move_to(next_step.get_center())
            self.play(Transform(next_step, updated_next_step))
            self.wait(0.5)

            updated_next_x = MathTex(f"x_T = x_T (\\alpha ^ {rand(xTame, n)}) \mod {n} = {pow(xTame, rand(xTame, n), n)}").move_to(next_x.get_center())
            self.play(Transform(next_x, updated_next_x))
            self.wait(0.5)

            # Animate the creation of the arrow
            self.play(Create(tame_arrows[-1]), run_time=0.5)
            self.wait(0.1)

        # Animate the wild kangaroo
        wild_arrows = []
        for i, (yWild, dWild, step) in enumerate(wild_steps):
            start = members[wild_steps[i - 1][0] - 1] if i > 0 else members[beta - 1]
            end = members[yWild - 1]
            wild_arrow = Arrow(start=start, end=end,
                               color=RED, buff=0.3, stroke_width=3)
            wild_arrows.append(wild_arrow)

            # Animate the creation of the arrow
            self.play(Create(wild_arrows[-1]), run_time=0.5)
            self.wait(0.1)

        # Show the final result
        result_text = MathTex(f"Secret x = {dTame + dWild}").to_edge(UP)
        self.play(Write(result_text))

        # Show the calculations for deriving the secret (x)
        calculation_text = MathTex(
            f"f(x) = \\alpha^{{x}} \\mod n = {g}^{{{dTame + dWild}}} \\mod {n} = {pow(g, dTame + dWild, n)}"
        ).next_to(result_text, DOWN)
        self.play(Write(calculation_text))

        # Highlight the trap and the wild kangaroo's position
        trap_circle = Circle(radius=0.25, color=YELLOW).move_to(
            members[(tame_steps[-1][0] - 1) % (n - 1)])
        self.play(Create(trap_circle))
        self.wait(1)

        # Show the wild kangaroo hitting the trap
        wild_final_position = members[tame_steps[-1][0]-1]
        self.play(wild_arrows[-1].animate.put_start_and_end_on(
            wild_final_position, members[(tame_steps[-1][0] - 1) % (n - 1)]), run_time=0.5)
        self.wait(1)

        # Indicate that the wild kangaroo has been trapped
        trapped_text = MathTex(
            "Wild Kangaroo Trapped!").next_to(trap_circle, UP)
        self.play(Write(trapped_text))
        self.wait(2)

        # Clean up the scene
        self.play(FadeOut(*tame_arrows), FadeOut(*wild_arrows), FadeOut(trap_circle),
                  FadeOut(result_text), FadeOut(calculation_text), FadeOut(trapped_text))
        self.wait(1)

        # End the scene
        self.play(FadeOut(*member_circles), FadeOut(*member_labels))
        self.wait(1)
