# imports <<<
from typing import List, Optional, Tuple, Union

import numpy as np

from .expressions import Expression
from .interpolation import GridInterpolator, KDTreeInterpolator
from .plot import Plotter
from .util import evaluate_expression, extract_2d_table
# >>>


class Mosfet:
    """
    Initialize a MOSFET object.

    When creating a MOSFET object, exactly two of the parameters `length`, `vbs`, `vgs`, or `vds`
    must be provided as fixed values. The remaining parameters can be specified as a range or set to
    `None` to use the full range from the lookup table. Any parameter not fixed is treated as the
    secondary sweep variable.

    If two parameters are given as ranges, you must indicate which one is the primary sweep variable
    using the `primary` argument.

    Args:
        lookup_table: dictionary containing MOSFET parameter data.
        mos: model name of the MOSFET.
        length: mosfet length.
        vbs: body-source voltage.
        vgs: gate-source voltage.
        vds: drain-source voltage.
        primary: name of the primary sweep.

    Examples:
        Fixed vbs and vds; sweep vgs (primary) and length (secondary)

        nmos = Mosfet(lookup_table=lookup_table, mos="nch_lvt", vbs=0.0, vds=0.4, vgs=(0.01, 1.19))
        pmos = Mosfet(lookup_table=lookup_table, mos="pch_lvt", vbs=0.0, vgs=-0.4, vds=(-1.19, -0.01))
    """
    # init <<<
    def __init__(
        self,
        *,
        lookup_table: dict,
        mos: str,
        length: Optional[Union[float, List[float], np.ndarray]] = None,
        vbs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        vgs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        vds: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        primary: Optional[str] = None
    ) -> None:
        self.mos = mos
        self.lookup_table = lookup_table[mos]
        self.length_all = self.lookup_table["length"]
        self.parameters = self.lookup_table["parameter_names"]
        self.device_parameters = self.lookup_table["device_parameters"]
        self.width = self.compute_device_width()

        self.secondary_var, self.filtered_variables, self.extracted_table = extract_2d_table(
            lookup_table=self.lookup_table,
            length=length,
            vbs=vbs,
            vgs=vgs,
            vds=vds,
            primary=primary,
        )
        self.length = self.filtered_variables["length"]
        self.vbs = self.filtered_variables["vbs"]
        self.vgs = self.filtered_variables["vgs"]
        self.vds = self.filtered_variables["vds"]

        # Initialize basic expressions.
        self.length_expression  = Expression(variables=["length"],  label="$\\mathrm{Length}\\ (m)$")
        self.vbs_expression     = Expression(variables=["vbs"],     label="$V_{\\mathrm{BS}}\\ (V)$")
        self.vgs_expression     = Expression(variables=["vgs"],     label="$V_{\\mathrm{GS}}\\ (V)$")
        self.vds_expression     = Expression(variables=["vds"],     label="$V_{\\mathrm{DS}}\\ (V)$")
        self.id_expression      = Expression(variables=["id"],      label="$I_{D}\\ (A)$")
        self.vth_expression     = Expression(variables=["vth"],     label="$V_{\\mathrm{TH}}\\ (V)$")
        self.gm_expression      = Expression(variables=["gm"],      label="$g_{m}\\ (S)$")
        self.gmbs_expression    = Expression(variables=["gmbs"],    label="$g_{\\mathrm{mbs}}\\ (S)$")
        self.gds_expression     = Expression(variables=["gds"],     label="$g_{\\mathrm{ds}}\\ (S)$")
        self.cgg_expression     = Expression(variables=["cgg"],     label="$c_{\\mathrm{gg}}\\ (F)$")
        self.cgs_expression     = Expression(variables=["cgs"],     label="$c_{\\mathrm{gs}}\\ (F)$")
        self.cbg_expression     = Expression(variables=["cbg"],     label="$c_{\\mathrm{bg}}\\ (F)$")
        self.cgd_expression     = Expression(variables=["cgd"],     label="$c_{\\mathrm{gd}}\\ (F)$")
        self.cdd_expression     = Expression(variables=["cdd"],     label="$c_{\\mathrm{dd}}\\ (F)$")

        # Some models use vdssat instead of vdsat.
        if "vdssat" in self.parameters:
            self.vdsat_expression   = Expression(variables=["vdssat"],   label="$V_{\\mathrm{DS_{\\mathrm{SAT}}}}\\ (V)$")
        else:
            self.vdsat_expression   = Expression(variables=["vdsat"],   label="$V_{\\mathrm{DS_{\\mathrm{SAT}}}}\\ (V)$")

        ########################################
        #         Computed Expressions         #
        ########################################
        self.vsg_expression = Expression(
            variables=["vgs"],
            function=lambda x: -x,
            label="$V_{\\mathrm{SG}}\\ (V)$"
        )
        self.vsb_expression = Expression(
            variables=["vbs"],
            function=lambda x: -x,
            label="$V_{\\mathrm{SB}}\\ (V)$"
        )
        self.vsd_expression = Expression(
            variables=["vds"],
            function=lambda x: -x,
            label="$V_{\\mathrm{SD}}\\ (V)$"
        )
        self.gmid_expression = Expression(
            variables=["gm", "id"],
            function=lambda x, y: x / y,
            label="$g_m/I_D\\ (S/A)$"
        )
        self.vov_expression = Expression(
            variables=["vgs", "vth"],
            function=lambda x, y: x - y,
            label="$V_{\\mathrm{OV}}\\ (V)$"
        )
        self.vstar_expression = Expression(
            variables=["gm", "id"],
            function=lambda x, y: (2 * y) / x,
            label="$V^{\\star}\\ (V)$"
        )
        self.current_density_expression = Expression(
            variables=["id"],
            function=lambda x: x / self.width,
            label="$I_{D}/W\\ (A/m)$"
        )
        self.gain_expression = Expression(
            variables=["gm", "gds"],
            function=lambda x, y: x / y,
            label="$g_{m}/g_{\\mathrm{ds}}$"
        )
        self.transist_frequency_expression = Expression(
            variables=["gm", "cgg"],
            function=lambda x, y: x / (2 * np.pi * y),
            label="$f_{T}\\ (Hz)$"
        )
        self.early_voltage_expression = Expression(
            variables=["id", "gds"],
            function=lambda x, y: x / y,
            label="$V_{A}\\ (V)$"
        )
        self.inverse_early_voltage_expression = Expression(
            variables=["gds", "id"],
            function=lambda x, y: x / y,
            label="$1/V_{A}\\ (V^{-1})$"
        )
        self.rds_expression = Expression(
            variables=["gds"],
            function=lambda x: 1 / x,
            label="$r_{\\mathrm{ds}}\\ (\\Omega)$"
        )

    # TODO: I need to test this more to account for all cases.
    def compute_device_width(self):
        if "w" in self.device_parameters:
            return self.device_parameters["w"]

        elif "weff" in self.parameters:
            if "nf" in self.device_parameters:
                return self.lookup_table["weff"] * self.device_parameters["nf"]
            else:
                return self.lookup_table["weff"]

        raise ValueError("Device width could not be computed.")
    # >>>

    # calculate from expression <<<
    def calculate_from_expression(self, expression: Expression, filter_by_rows: Optional[np.ndarray] = None) -> Tuple[np.ndarray, str]:
        """
        Calculates values from a given expression over the extracted lookup table.

        Args:
            expression: The Expression object defining the computation.
            filter_by_rows: Optional array of row indices to filter the data.

        Returns:
            A tuple containing the computed numpy array and the expression's label.
        """
        return evaluate_expression(expression, self.extracted_table, filter_by_rows)
    # >>>

    # plot by expression <<<
    def plot_by_expression(
        self,
        *,
        x_expression: Expression,
        y_expression: Expression,
        y2_expression: Optional[Expression] = None,
        filtered_values: Optional[Union[float, List[float], np.ndarray]] = None,
        x_limit: Optional[Tuple[float, float]] = None,
        y_limit: Optional[Tuple[float, float]] = None,
        y2_limit: Optional[Tuple[float, float]] = None,
        x_scale: str = "",
        y_scale: str = "",
        y2_scale: str = "",
        x_eng_format: bool = False,
        y_eng_format: bool = False,
        y2_eng_format: bool = False,
        legend_placement: Optional[str] = None,
        legend_location: Optional[Tuple[float, float]] = None,
        legend_eng_format: bool = True,
        show_legend: bool = True,
        fig_size: Optional[Tuple[int, int]] = None,
        save_fig: str = "",
        return_result: bool = False
    ) -> Optional[Tuple]:
        """
        Plot computed x, y, and optionally y2 expressions, filtering by the secondary sweep variable.

        If y2_expression is provided, a twin y-axis plot is created.

        Parameters:
            x_expression: Expression for x-axis computation.
            y_expression: Expression for primary y-axis computation.
            y2_expression: Optional expression for secondary y-axis computation.
            filtered_values: Values to filter the secondary sweep variable.
            x_limit: Limits for the x-axis.
            y_limit: Limits for the primary y-axis.
            y2_limit: Limits for the secondary y-axis.
            x_scale: Scale type for the x-axis.
            y_scale: Scale type for the primary y-axis.
            y2_scale: Scale type for the secondary y-axis.
            x_eng_format: If True, format the x-axis in engineering units.
            y_eng_format: If True, format the primary y-axis in engineering units.
            y2_eng_format: If True, format the secondary y-axis in engineering units.
            legend_placement: Position of the legend (e.g., 'best', 'right', 'top', 'bottom').
            legend_location: Manual coordinates for legend placement as (x, y) tuple.
            lengend_eng_format: If True, format legend values in engineering units.
            save_fig: Filename to save the figure.
            return_result: If True, return the computed arrays.

        Returns:
            A tuple (x, y, y2) if y2_expression is provided; otherwise, (x, y) when return_result is True.
        """

        filter_var = self.secondary_var if self.secondary_var is not None else "length"
        sec_values = self.filtered_variables[filter_var]
        if filtered_values is not None:
            if isinstance(filtered_values, (list, np.ndarray)):
                indices = np.nonzero(np.isin(sec_values, np.array(filtered_values)))[0]
            else:
                indices = np.array([np.abs(sec_values - filtered_values).argmin()])
        else:
            indices = np.arange(len(sec_values))

        legend_values = np.array(sec_values)[indices]
        legend_title_mapping = {
            "length": "Length",
            "vbs": "$V_{\\mathrm{BS}}$",
            "vgs": "$V_{\\mathrm{GS}}$",
            "vds": "$V_{\\mathrm{DS}}$"
        }
        legend_title = legend_title_mapping.get(filter_var, filter_var)
        x, x_label = self.calculate_from_expression(x_expression, indices)
        y, y_label = self.calculate_from_expression(y_expression, indices)

        if y2_expression is not None:
            fig_size = (6, 4) if fig_size is None else fig_size
            self.plotter = Plotter(fig_size=fig_size, show_legend=show_legend)
            y2, y2_label = self.calculate_from_expression(y2_expression, indices)
            _, ax, ax2 = self.plotter.create_figure_with_twin(
                title="",
                x_label=x_label,
                y_label=y_label,
                y2_label=y2_label,
                x_lim=x_limit,
                y_lim=y_limit,
                y2_lim=y2_limit,
                x_scale=x_scale,
                y_scale=y_scale,
                y2_scale=y2_scale,
                x_eng_format=x_eng_format,
                y_eng_format=y_eng_format,
                y2_eng_format=y2_eng_format
            )
            self.plotter.plot_data(
                    ax2, x, y2,
                    line_style="dashed",
                    end_plotting=False
            )
            self.plotter.plot_data(
                    ax, x, y,
                    line_style="solid",
                    legend=legend_values,
                    legend_title=legend_title,
                    legend_eng_format=legend_eng_format,
                    legend_placement="top" if legend_placement is None else legend_placement,
                    bbox_to_anchor=legend_location,
                    save_fig=save_fig,
            )
            return (x, y, y2) if return_result else None
        else:
            fig_size = (8, 4) if fig_size is None else fig_size
            self.plotter = Plotter(fig_size=fig_size, show_legend=show_legend)
            _, ax = self.plotter.create_figure(
                title="",
                x_label=x_label,
                y_label=y_label,
                x_lim=x_limit,
                y_lim=y_limit,
                x_scale=x_scale,
                y_scale=y_scale,
                x_eng_format=x_eng_format,
                y_eng_format=y_eng_format
            )
            self.plotter.plot_data(
                ax, x, y,
                legend=legend_values,
                legend_title=legend_title,
                legend_eng_format=legend_eng_format,
                legend_placement=legend_placement,
                bbox_to_anchor=legend_location,
                save_fig=save_fig,
            )
            return (x, y) if return_result else None
    # >>>

    # plot by sweep <<<
    def plot_by_sweep(
        self,
        *,
        x_expression: Expression,
        y_expression: Expression,
        y2_expression: Optional[Expression] = None,
        primary: str,
        length: Optional[Union[float, List[float], np.ndarray]] = None,
        vbs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        vgs: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        vds: Optional[Union[float, Tuple[float, float], Tuple[float, float, float]]] = None,
        x_limit: Optional[Tuple[float, float]] = None,
        y_limit: Optional[Tuple[float, float]] = None,
        y2_limit: Optional[Tuple[float, float]] = None,
        x_scale: str = "",
        y_scale: str = "",
        y2_scale: str = "",
        x_eng_format: bool = False,
        y_eng_format: bool = False,
        y2_eng_format: bool = False,
        legend_location: Optional[Tuple[float, float]] = None,
        legend_placement: Optional[str] = None,
        legend_eng_format: bool = True,
        show_legend: bool = True,
        save_fig: str = "",
        fig_size: Optional[Tuple[int, int]] = None,
        return_result: bool = False
    ) -> Optional[Tuple]:
        """
        Plot computed x, y, and optionally y2 expressions for a sweep with fixed parameters.

        If y2_expression is provided, a twin y-axis plot is created.

        Parameters:
            x_expression: Expression for x-axis computation.
            y_expression: Expression for primary y-axis computation.
            y2_expression: Optional expression for secondary y-axis computation.
            primary: Primary sweep variable.
            length: Length value(s) to filter the lookup table.
            vbs: body-source voltage value(s) or range.
            vgs: Gate-source voltage value(s) or range.
            vds: Drain-source voltage value(s) or range.
            x_limit: Limits for the x-axis.
            y_limit: Limits for the primary y-axis.
            y2_limit: Limits for the secondary y-axis.
            x_scale: Scale type for the x-axis.
            y_scale: Scale type for the primary y-axis.
            y2_scale: Scale type for the secondary y-axis.
            x_eng_format: If True, format the x-axis in engineering units.
            y_eng_format: If True, format the primary y-axis in engineering units.
            y2_eng_format: If True, format the secondary y-axis in engineering units.
            legend_placement: Position of the legend (e.g., 'best', 'right', 'top', 'bottom').
            legend_location: Manual coordinates for legend placement as (x, y) tuple.
            lengend_eng_format: If True, format legend values in engineering units.
            save_fig: Filename to save the figure.
            return_result: If True, return the computed arrays.

        Returns:
            A tuple (x, y, y2) if y2_expression is provided; otherwise, (x, y) when return_result is True.
        """
        secondary_var, filtered_vars, extracted_table = extract_2d_table(
            lookup_table=self.lookup_table,
            length=length,
            vbs=vbs,
            vgs=vgs,
            vds=vds,
            primary=primary,
        )
        x, x_label = evaluate_expression(x_expression, extracted_table)
        y, y_label = evaluate_expression(y_expression, extracted_table)

        legend = None
        legend_title = None
        if secondary_var is not None:
            legend = [sw for sw in filtered_vars[secondary_var]]
            legend_title_mapping = {
                "length": "Length",
                "vbs": "$V_{\\mathrm{BS}}$",
                "vgs": "$V_{\\mathrm{GS}}$",
                "vds": "$V_{\\mathrm{DS}}$"
            }
            legend_title = legend_title_mapping.get(secondary_var, secondary_var)

        if y2_expression is not None:
            fig_size = (6, 4) if fig_size is None else fig_size
            self.plotter = Plotter(fig_size=fig_size, show_legend=show_legend)
            y2, y2_label = evaluate_expression(y2_expression, extracted_table)
            _, ax, ax2 = self.plotter.create_figure_with_twin(
                title="",
                x_label=x_label,
                y_label=y_label,
                y2_label=y2_label,
                x_lim=x_limit,
                y_lim=y_limit,
                y2_lim=y2_limit,
                x_scale=x_scale,
                y_scale=y_scale,
                y2_scale=y2_scale,
                x_eng_format=x_eng_format,
                y_eng_format=y_eng_format,
                y2_eng_format=y2_eng_format
            )
            self.plotter.plot_data(
                ax2, x, y2,
                line_style="dashed",
                end_plotting=False
            )
            self.plotter.plot_data(
                ax, x, y,
                line_style="solid",
                legend=legend,
                legend_title=legend_title,
                legend_eng_format=legend_eng_format,
                legend_placement="top" if legend_placement is None else legend_placement,
                bbox_to_anchor=legend_location,
                save_fig=save_fig,
            )
            return (x, y, y2) if return_result else None
        else:
            fig_size = (8, 4) if fig_size is None else fig_size
            self.plotter = Plotter(fig_size=fig_size, show_legend=show_legend)
            _, ax = self.plotter.create_figure(
                title="",
                x_label=x_label,
                y_label=y_label,
                x_lim=x_limit,
                y_lim=y_limit,
                x_scale=x_scale,
                y_scale=y_scale,
                x_eng_format=x_eng_format,
                y_eng_format=y_eng_format
            )
            self.plotter.plot_data(
                ax, x, y,
                legend=legend,
                legend_title=legend_title,
                legend_eng_format=legend_eng_format,
                bbox_to_anchor=legend_location,
                legend_placement="right" if legend_placement is None else legend_placement,
                save_fig=save_fig,
            )
            return (x, y) if return_result else None
    # >>>

    # quick_plot <<<
    def quick_plot(
        self,
        *,
        x: Union[np.ndarray, List[np.ndarray]],
        y: Union[np.ndarray, List[np.ndarray]],
        x_label: str = "",
        y_label: str = "",
        x_limit: Optional[Tuple[float, float]] = None,
        y_limit: Optional[Tuple[float, float]] = None,
        x_scale: str = "",
        y_scale: str = "",
        x_eng_format: bool = False,
        y_eng_format: bool = False,
        legend: Optional[List[str]] = None,
        fig_size: Optional[Tuple[int, int]] = None,
        legend_title: Optional[str] = "",
        legend_location: Optional[Tuple[float, float]] = None,
        legend_placement: Optional[str] = None,
        legend_eng_format: bool = True,
        show_legend: bool = True,
        title: Optional[str] = None,
        save_fig: str = ""
    ) -> None:
        """
        Quickly plots the provided x and y data.

        x and y can be either a single numpy array or a list of numpy arrays.
        This method creates a figure using the plotter and plots the data.

        Args:
            x: x-axis data as a numpy array or a list of numpy arrays.
            y: y-axis data as a numpy array or a list of numpy arrays.
            x_label: Label for the x-axis.
            y_label: Label for the y-axis.
            x_limit: Optional x-axis limits.
            y_limit: Optional y-axis limits.
            x_scale: Optional x-axis scale type.
            y_scale: Optional y-axis scale type.
            x_eng_format: If True, format x-axis labels in engineering units.
            y_eng_format: If True, format y-axis labels in engineering units.
            legend: Optional list of legend entries.
            legend_placement: Position of the legend (e.g., 'best', 'right', 'top', 'bottom').
            legend_location: Manual coordinates for legend placement as (x, y) tuple.
            lengend_eng_format: If True, format legend values in engineering units.
            title: Optional title for the plot.
            save_fig: Optional filename to save the figure.
        """
        self.plotter = Plotter(fig_size=fig_size, show_legend=show_legend)
        _, ax = self.plotter.create_figure(
            title=title or "",
            x_label=x_label,
            y_label=y_label,
            x_lim=x_limit,
            y_lim=y_limit,
            x_scale=x_scale,
            y_scale=y_scale,
            x_eng_format=x_eng_format,
            y_eng_format=y_eng_format
        )
        self.plotter.plot_data(
            ax, x, y,
            legend=legend,
            legend_title=legend_title,
            legend_placement=legend_placement,
            legend_eng_format=legend_eng_format,
            bbox_to_anchor=legend_location,
            save_fig=save_fig,
        )
    # >>>

    # interpolate <<<
    def interpolate(
        self,
        *,
        x_expression: Expression,
        x_value: Union[float, Tuple[float, float], np.ndarray],
        y_expression: Expression,
        y_value: Union[float, Tuple[float, float], np.ndarray],
        z_expression: Union[Expression, List[Expression]],
        fast: bool = False
    ) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Interpolates z values given x and y expressions.

        Args:
            x_expression: Expression for the x-axis.
            x_value: Value(s) for the x-axis interpolation domain.
            y_expression: Expression for the y-axis.
            y_value: Value(s) for the y-axis interpolation domain.
            z_expression: Expression or list of expressions for the z values.
            fast: If True, use KDTree-based interpolation; otherwise, use griddata.

        Returns:
            A single interpolated numpy array if z_expression is a single Expression,
            or a list of interpolated numpy arrays if a list is provided.
        """
        if not fast:
            interpolator = GridInterpolator(self.extracted_table)
        else:
            interpolator = KDTreeInterpolator(self.extracted_table)
        return interpolator.interpolate(x_expression, x_value, y_expression, y_value, z_expression)
    # >>>

    # lookup expression from table <<<
    def lookup_expression_from_table(
        self,
        *,
        length: Union[float, List[float], np.ndarray],
        vbs: Union[float, Tuple[float, float, float]],
        vgs: Union[float, Tuple[float, float, float]],
        vds: Union[float, Tuple[float, float, float]],
        primary: str,
        expression: Union[Expression, List[Expression]]
    ) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Evaluates one or more expressions on the lookup table without interpolation.

        Args:
            length: The MOSFET length to filter the table.
            vbs: The body-source voltage parameter.
            vgs: The gate-source voltage parameter.
            vds: The drain-source voltage parameter.
            primary: The primary sweep variable.
            expression: A single Expression or a list of Expressions to evaluate.

        Returns:
            A numpy array if a single Expression is provided, or a list of numpy arrays if multiple
            Expressions are provided.
        """
        _, _, extracted_table = extract_2d_table(
            lookup_table=self.lookup_table,
            length=length,
            vbs=vbs,
            vgs=vgs,
            vds=vds,
            primary=primary,
        )

        def process_expr(expr: Expression) -> np.ndarray:
            result, _ = evaluate_expression(expr, extracted_table)
            return result

        if isinstance(expression, list):
            return [process_expr(expr) for expr in expression]
        else:
            return process_expr(expression)
    # >>>
