import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
from shinyswatch import theme

# Load the dataset of penguins
df = palmerpenguins.load_penguins()

# Set page options such as the title and fillable option for the layout
ui.page_opts(title="Shrestha Penguin dashboard", fillable=True)

# Side panel for user input to control the filters applied to the penguin data
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/sshres10/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/sshres10/cintel-07-tdash/blob/main/app/app.py",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/sshres10/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://sshres10.github.io/cintel-07-tdash/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://sshres10.github.io/cintel-07-tdash/",
        target="_blank",
    )

# Detailed plots and data grid showing the filtered penguin data
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
theme.darkly()