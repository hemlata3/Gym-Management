# Copyright (c) 2024, LATA and contributors
# For license information, please see license.txt

import frappe
# from frappe import _

from frappe import db, _

def execute(filters: dict | None = None):
    """Return columns, data, and chart for the report."""
    columns = get_columns()
    data = get_data(filters)

    # Generate chart only if data exists
    chart = get_chart_data(data) if data else None

    return columns, data, None, chart

def get_columns() -> list[dict]:
    """Return columns for the report."""
    return [
        {
            "label": _("Month"),
            "fieldname": "month",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Total Revenue"),
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]

def get_data(filters: dict | None = None) -> list[dict]:
    """Fetch aggregated revenue data by month with optional month filter."""
    conditions = []
    values = {}

    # Apply month filter if provided
    if filters and filters.get("month"):
        selected_month = filters["month"]
        conditions.append(["DATE_FORMAT(start_date, '%Y-%m')", "=", selected_month])
        frappe.msgprint(_("Filtering data for the month: {month}").format(month=selected_month))

    try:
        # Query data from Gym Membership grouped by month
        data = db.sql(
            """
            SELECT 
                DATE_FORMAT(start_date, '%%Y-%%m') AS month,
                SUM(price) AS total_revenue
            FROM `tabGym Membership`
            {where_clause}
            GROUP BY DATE_FORMAT(start_date, '%%Y-%%m')
            ORDER BY DATE_FORMAT(start_date, '%%Y-%%m') ASC
            """.format(
                where_clause="WHERE " + " AND ".join(["{} {}".format(*c) for c in conditions])
                if conditions
                else ""
            ),
            values=values,
            as_dict=True,
        )

        # Debugging fetched data
        frappe.msgprint(_("Fetched Data: {data}").format(data=data))

        return data

    except Exception as e:
        frappe.log_error(message=str(e), title="Error in Monthly Revenue Report")
        frappe.msgprint(_("An error occurred while fetching data. Check logs for details."))
        return []

def get_chart_data(data: list[dict]) -> dict:
    """Generate bar chart data for revenue grouped by month."""
    labels = [row["month"] for row in data]
    values = [row["total_revenue"] or 0 for row in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}],
        },
        "type": "donut",  # Chart type: bar
        "title": _("Monthly Revenue Distribution"),
    }
