import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""![](public/2023-06-23-16-01-24.png)""")
    return


@app.cell
def _():
    import dimstack as ds
    import marimo as mo
    import plotly
    import numpy as np

    ds.display.mode("df")
    return ds, mo, np, plotly


@app.cell
def _(ds, np):
    m1 = ds.dim.Basic(
        nom=2.565/2,
        tol=ds.tol.Bilateral.symmetric(0.05/2),
        name="Datum C Slot Size",
    )
    m2 = ds.dim.Basic(
        nom=0.7/2,
        tol=ds.tol.Bilateral.symmetric(0.07/2),
        name="Datum C Slot Diameter",
    )
    m3 = ds.dim.Basic(
        nom=-np.sqrt(45.05**2 + 39.8**2),
        # tol=ds.tol.Bilateral.symmetric(np.sqrt(0.3**2 + 0.27**2)),
        tol=ds.tol.Bilateral.symmetric(np.sqrt(0.46**2 + 0.4**2)), # Per suppliers request
        name="Datum C Slot Location",
        desc="Relative to Datum B",
    )
    m4 = ds.dim.Basic(
        nom=3.065/2,
        tol=ds.tol.Bilateral.symmetric(0.05/2),
        name="Datum B Hole Size",
    )
    m5 = ds.dim.Basic(
        nom=-2.99/2,
        tol=ds.tol.Bilateral.symmetric(0.03/2),
        name="Datum B Pin Size",
    )
    m6 = ds.dim.Basic(
        nom=np.sqrt(45.05**2 + 39.8**2),
        tol=ds.tol.Bilateral.symmetric(0.1/2), # 0.08/2 per reference design, but customer likely to be sloppy.
        name="Datum C Pin Position",
        desc="Relative to Datum B Pin",
    )
    m7 = ds.dim.Basic(
        nom=-2.49/2,
        tol=ds.tol.Bilateral.symmetric(0.03/2),
        name="Datum C Pin Size",
    )
    items = [m1, m2, m3, m4, m5, m6, m7]

    stack = ds.Stack(name="Datum C Pin-Slot Gap", dims=items)
    stack.show()
    return items, m1, m2, m3, m4, m5, m6, m7, stack


@app.cell
def _(ds, stack):
    ds.plot.StackPlot().add(stack).show()
    return


@app.cell
def _(ds, stack):
    ds.calc.WC(stack).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Since the left side of the slot is our 0 point, we want the left size of the pin to be in the positive direction, or the bounds of the entire tolerance stack to be greater than zero.

        At worst-case, the lower bound is negative, meaning the pin would not fit in the slot. It would need to grow 340 [um] in both directions to get there.

        That is quite a bit. What if we don't need it to fit every time, just pretty dang close to almost every time...
        """
    )
    return


@app.cell
def _(ds, stack):
    ds.calc.RSS(stack).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        If we wanted to target W.C or RSS we would have to rework the dimensions to keep the bounds within the positive region for those capabilities

        Let's lengthen the slot to 1.2 mm. Because this stackup is large and will likely never get to where each part is at worst tolerance on the worst direction in the assembly, we will proceed with RSS analysis.
        """
    )
    return


@app.cell
def _(ds, m1, m3, m4, m5, m6, m7, mo):
    m2_longer = ds.dim.Basic(
        nom=0.7/2 + 0.5/2, # grow the entire slot by 500 [um]
        tol=ds.tol.Bilateral.symmetric(0.07/2),
        name="Datum C Slot Length",
    )
    items_longerm2 = [m1, m2_longer, m3, m4, m5, m6, m7]
    stack_longerm2 = ds.Stack(name="Datum C Pin-Slot Gap", dims=items_longerm2)
    mo.vstack([
        ds.calc.WC(stack_longerm2).show(),
        ds.calc.RSS(stack_longerm2).show()
    ])
    return items_longerm2, m2_longer, stack_longerm2


@app.cell
def _(ds, stack_longerm2):
    spec = ds.Requirement("stack spec", "", distribution=ds.calc.RSS(stack_longerm2).review(3).distribution, LL=0.0, UL=99)
    spec.show()
    return (spec,)


@app.cell
def _(mo):
    mo.md(r"""This means the assembly will be maufactured to the allowable bounds 99.95% of the time if the slot was increased to 1.2 mm""")
    return


@app.cell
def _(mo):
    mo.md(r""" """)
    return


if __name__ == "__main__":
    app.run()
