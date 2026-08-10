"""Math museum beauty animations — rendered with Manim."""
from manim import *


class EulerIdentity(Scene):
    """e^(iπ) + 1 = 0 — the point rotates around the unit circle, tracing sine/cosine."""
    def construct(self):
        # Axes
        plane = ComplexPlane(
            x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
            background_line_style={"stroke_opacity": 0.25},
        ).scale(2)
        circle = Circle(radius=2, color=BLUE).scale(1)
        circle.set_stroke(width=2, opacity=0.8)
        label_circle = MathTex("|z| = 1").next_to(circle, DOWN + RIGHT, buff=0.2).scale(0.7)
        self.play(Create(plane), Create(circle), FadeIn(label_circle), run_time=1.2)
        self.wait(0.3)

        # The rotating point z = e^(iθ)
        z = Dot(color=YELLOW).move_to([2, 0, 0])
        z_dot = z
        radius_line = Line(ORIGIN, z.get_center(), color=YELLOW, stroke_width=3)
        trace = TracedPath(z_dot.get_center, stroke_width=2, stroke_opacity=0.6, color=TEAL)

        # Sine / cosine projections
        def cos_projection(p):
            return np.array([0, p[1], 0])  # vertical line for sin
        def sin_projection(p):
            return np.array([p[0], 0, 0])  # horizontal line for cos

        # Labels
        z_label = MathTex("e^{i\\theta}").scale(0.8)
        z_label.add_updater(lambda m: m.next_to(z_dot, UR, buff=0.1))

        self.add(z_dot, radius_line, trace, z_label)
        self.play(Rotating(z_dot, angle=2 * TAU, about_point=ORIGIN, run_time=6, rate_func=linear))
        self.wait(0.5)

        # Stop rotation, show final position at θ = π → e^(iπ) = -1
        z_dot.clear_updaters()
        self.play(
            z_dot.animate.move_to([-2, 0, 0]),
            run_time=1.2,
        )
        euler = MathTex("e^{i\\pi} + 1 = 0", color=GOLD).scale(1.4)
        euler.move_to(UP * 2)
        self.play(Write(euler))
        self.wait(1.5)


class FourierSeries(Scene):
    """Fourier series building a square wave from sines."""
    def construct(self):
        axes = Axes(
            x_range=[-0.5, 6.5, 1], y_range=[-1.8, 1.8, 1],
            x_length=7, y_length=3.6,
        ).to_edge(DOWN)
        labels = axes.get_axis_labels(x_label="t", y_label="")
        self.play(Create(axes), FadeIn(labels), run_time=1)

        # Square wave target (faded)
        square = axes.plot(
            lambda t: 1 if (t % 4) < 2 else -1,
            x_range=[0, 6, 0.02],
            color=GREY,
            stroke_opacity=0.5,
        )
        self.play(Create(square), run_time=0.8)

        formula = MathTex("\\sin t + \\tfrac{1}{3}\\sin 3t + \\tfrac{1}{5}\\sin 5t + \\cdots", color=BLUE).to_edge(UP)
        self.play(Write(formula), run_time=1)

        # Accumulate harmonics
        partial = axes.plot(
            lambda t: 0 * t, x_range=[0, 6, 0.02],
            color=BLUE,
        )
        self.add(partial)
        n_terms = [1, 2, 3, 5, 8, 12]
        for i, n in enumerate(n_terms):
            new = axes.plot(
                lambda t, n=n: sum(
                    (4 / np.pi) * (1 / (2 * k + 1)) * np.sin((2 * k + 1) * np.pi * t / 2)
                    for k in range(n)
                ),
                x_range=[0, 6, 0.02],
                color=BLUE,
            )
            self.play(Transform(partial, new), run_time=0.9)
            if i == len(n_terms) - 1:
                label = MathTex(f"N = {n}", color=BLUE).next_to(partial, UR, buff=0.2)
                self.play(FadeIn(label), run_time=0.3)
        self.wait(1.5)


class RiemannSum(Scene):
    """Riemann sum rectangles approximating the area under x²."""
    def construct(self):
        axes = Axes(
            x_range=[0, 3, 1], y_range=[0, 9, 2],
            x_length=6, y_length=6,
        ).to_edge(DOWN).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=0.8)

        curve = axes.plot(lambda x: x * x, x_range=[0, 3], color=YELLOW)
        curve_label = MathTex("f(x) = x^2").next_to(axes.c2p(1.5, 2.25), UP).scale(0.8)
        self.play(Create(curve), FadeIn(curve_label), run_time=0.8)

        area_value = DecimalNumber(0, num_decimal_places=3, color=GOLD).to_corner(UR)
        area_text = MathTex("\\text{Area} \\approx").next_to(area_value, LEFT)
        self.play(FadeIn(VGroup(area_text, area_value)), run_time=0.4)

        for n in [1, 2, 4, 8, 16, 32]:
            rects = VGroup()
            for i in range(n):
                x0 = 3 * i / n
                x1 = 3 * (i + 1) / n
                mid = (x0 + x1) / 2
                h = mid * mid
                r = Rectangle(
                    width=axes.c2p(x1, 0)[0] - axes.c2p(x0, 0)[0],
                    height=axes.c2p(0, h)[1] - axes.c2p(0, 0)[1],
                )
                r.move_to([(axes.c2p(x0, 0)[0] + axes.c2p(x1, 0)[0]) / 2, (axes.c2p(0, h)[1]) / 2, 0])
                r.set_stroke(color=BLUE, width=1)
                r.set_fill(color=BLUE, opacity=0.35)
                rects.add(r)
            area = sum(((3 * i + 3 * (i + 1)) / (2 * n)) ** 2 * (3 / n) for i in range(n))
            self.play(
                FadeIn(rects, lag_ratio=0.02),
                area_value.animate.set_value(area),
                run_time=1.1,
            )
            self.remove(rects)

        final = MathTex("\\lim_{n \\to \\infty} \\sum f(x_i^*) \\Delta x = \\int_0^3 x^2 \\, dx = 9", color=GOLD).scale(1.1)
        final.to_edge(UP)
        self.play(Write(final), run_time=1.2)
        self.wait(1.5)


class FractalZoom(Scene):
    """A fractal-like zoom using a self-similar triangular pattern."""
    def construct(self):
        title = Text("Self-Similarity", font_size=44, color=BLUE).to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Sierpinski triangle up to depth 5
        def sierpinski(vertices, depth, max_depth=5):
            if depth >= max_depth:
                return Polygon(*vertices, fill_opacity=0.9, stroke_width=0, fill_color=TEAL)
            a, b, c = vertices
            mab = (a + b) / 2
            mbc = (b + c) / 2
            mca = (c + a) / 2
            return VGroup(
                sierpinski([a, mab, mca], depth + 1, max_depth),
                sierpinski([mab, b, mbc], depth + 1, max_depth),
                sierpinski([mca, mbc, c], depth + 1, max_depth),
            )

        tri = sierpinski([np.array([-3, -2, 0]), np.array([3, -2, 0]), np.array([0, 2.5, 0])], 0)
        self.play(Create(tri), run_time=1.5)

        # Zoom into a corner — dramatic scale
        for _ in range(3):
            self.play(
                tri.animate.scale(2.2).shift(LEFT * 2 + DOWN * 1.2),
                run_time=1.4,
            )
        self.wait(1.5)
