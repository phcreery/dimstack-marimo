import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import dimstack as ds
    import marimo as mo
    import plotly
    return ds, mo, plotly


@app.cell
def _(ds):
    ds.display.mode("df")

    k = 0.25
    target_process_sigma = 3
    stdev = 0.036 / target_process_sigma
    m1 = dim = ds.dim.Basic(
        nom=208,
        tol=ds.tol.Bilateral.symmetric(0.036),
        name="a",
        desc="Shaft",
    ).review(
        distribution=ds.dist.Normal(208 + k * target_process_sigma * stdev, stdev),
        target_process_sigma=target_process_sigma,
    )
    m2 = dim = ds.dim.Basic(
        nom=-1.75,
        tol=ds.tol.Bilateral.unequal(0, 0.06),
        name="b",
        desc="Retainer ring",
    ).review(
        target_process_sigma=3,
    )
    m3 = dim = ds.dim.Basic(
        nom=-23,
        tol=ds.tol.Bilateral.unequal(0, 0.12),
        name="c",
        desc="Bearing",
    ).review(
        target_process_sigma=3,
    )
    m4 = dim = ds.dim.Basic(
        nom=20,
        tol=ds.tol.Bilateral.symmetric(0.026),
        name="d",
        desc="Bearing Sleeve",
    ).review(
        target_process_sigma=3,
    )
    m5 = im = ds.dim.Basic(
        nom=-200,
        tol=ds.tol.Bilateral.symmetric(0.145),
        name="e",
        desc="Case",
    ).review(
        target_process_sigma=3,
    )
    m6 = ds.dim.Basic(
        nom=20,
        tol=ds.tol.Bilateral.symmetric(0.026),
        name="f",
        desc="Bearing Sleeve",
    )
    m7 = dim = ds.dim.Basic(
        nom=-23,
        tol=ds.tol.Bilateral.unequal(0, 0.12),
        name="g",
        desc="Bearing",
    ).review(
        target_process_sigma=3,
    )

    return dim, im, k, m1, m2, m3, m4, m5, m6, m7, stdev, target_process_sigma


@app.cell
def _(ds, m1, m2, m3, m4, m5, m7, mo):
    items = [m1, m2, m3, m4, m5, m7]
    stack = ds.dim.ReviewedStack(name="stacks on stacks", dims=items)

    mo.vstack([
        stack.show(),
        stack.to_basic_stack().show()
    ])
    return items, stack


@app.cell
def _(ds, m1):
    ds.plot.StackPlot().add(m1).show()
    return


@app.cell
def _(ds, stack):
    ds.plot.StackPlot().add(stack).show()
    return


@app.cell
def _(ds, mo, stack):
    designed_for = ds.calc.SixSigma(stack, at=4.5)
    mo.vstack(
        [
            ds.calc.Closed(stack).show(),
            ds.calc.WC(stack).show(),
            ds.calc.RSS(stack).show(),
            ds.calc.MRSS(stack).show(),
            designed_for.show(),
        
        ]
    )
    return (designed_for,)


@app.cell
def _(ds, stack):
    sp = ds.plot.StackPlot()
    sp.add(ds.calc.Closed(stack))
    sp.start_pos = 0
    sp.add(ds.calc.WC(stack))
    sp.start_pos = 0
    sp.add(ds.calc.RSS(stack))
    sp.start_pos = 0
    sp.add(ds.calc.MRSS(stack))
    sp.start_pos = 0
    sp.add(ds.calc.SixSigma(stack, at=4.5))
    sp.show()
    ds.calc.SixSigma(stack, at=4.5).show()
    return (sp,)


@app.cell
def _(ds, stack):
    requirement = ds.dim.Requirement("stack spec", "", distribution=ds.calc.SixSigma(stack, at=4.5).distribution, LL=0.05, UL=0.8)
    requirement.show()
    return (requirement,)


if __name__ == "__main__":
    app.run()
