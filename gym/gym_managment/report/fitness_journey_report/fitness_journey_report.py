# Copyright (c) 2024, LATA and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)

	return columns, data, None, chart


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
        {
		    "label": _("Member"),
            "fieldname": "member",
            "fieldtype": "Link",
            "options": "Member",
            "width": 200,
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Weight (kg)"),
            "fieldname": "weight",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": _("Calories (kcal)"),
            "fieldname": "calories",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def get_data(filters: dict | None) -> list[dict]:
    """Fetch fitness data for the report based on the selected customer."""
    if not filters or not filters.get("member"):
        frappe.throw(_("Please select a member to view their fitness journey."))

    member = filters.get("member")
    data = frappe.db.get_all(
        "Fitness",
        filters={"member": member},
        fields=["member", "date", "weight", "calories"],
        order_by="date asc",
    )
    return data


def get_chart(data: list[dict]) -> dict:
    """Generate chart data for tracking weight and calories."""
    dates = [row["date"] for row in data]
    weights = [row["weight"] for row in data]
    calories = [row["calories"] for row in data]

    return {
        "data": {
            "labels": dates,
            "datasets": [
                {
                    "name": _("Weight"),
                    "values": weights,
                },
                {
                    "name": _("Calories"),
                    "values": calories,
                },
            ],
        },
        "type": "line",  # Chart type can be line, bar, etc.
        "axisOptions": {"xIsSeries": True},
    }













# import frappe
# from frappe import _

# def execute(filters: dict | None = None):
#     """Main entry point for the report. Returns columns, data, and chart."""
#     columns = get_columns()
#     data = get_data(filters)
#     chart = generate_chart(data)
#     return columns, data, None, chart

# def get_columns():
#     """Defines the columns for the fitness journey report."""
#     return [
#         {
#             "label": _("Member"),
#             "fieldname": "member",
#             "fieldtype": "Link",
#             "options": "Gym Member",
#             "width": 150,
#         },
#         {
#             "label": _("Date"),
#             "fieldname": "date",
#             "fieldtype": "Date",
#             "width": 120,
#         },
#         {
#             "label": _("Weight (kg)"),
#             "fieldname": "weight",
#             "fieldtype": "Float",
#             "width": 120,
#         },
#         {
#             "label": _("Calories Burned"),
#             "fieldname": "calories_burned",
#             "fieldtype": "Float",
#             "width": 150,
#         },
#     ]

# def get_data(filters):
#     """Fetches data from the Fitness Progress Doctype."""
#     if not filters or not filters.get("member"):
#         frappe.throw(_("Please select a member to view their fitness journey."))

#     # Fetch records from Fitness Progress
#     return frappe.db.get_all(
#         "Fitness Progress",
#         filters={"member": filters.get("member")},
#         fields=["member", "date", "weight", "calories_burned"],
#         order_by="date asc",
#     )

# def generate_chart(data):
#     """Generates chart data for visualizing weight and calories burned."""
#     # Extract data for chart
#     dates = [row["date"] for row in data]
#     weights = [row["weight"] for row in data]
#     calories = [row["calories_burned"] for row in data]

#     return {
#         "data": {
#             "labels": dates,
#             "datasets": [
#                 {"name": _("Weight (kg)"), "values": weights},
#                 {"name": _("Calories Burned"), "values": calories},
#             ],
#         },
#         "type": "line",  # Choose between line, bar, etc.
#         "axisOptions": {"xIsSeries": True},
#     }






