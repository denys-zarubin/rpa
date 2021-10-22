"""Basic module for agregation data."""
import pandas as pd


def merge_data_to_xls(filename, path, data1, data2):
    """Generate xls file from data."""
    writer = pd.ExcelWriter(f"{path}/{filename}.xlsx")
    data1.to_excel(writer, sheet_name='Agencies')
    data2.to_excel(writer, sheet_name='Investments')
    writer.save()
