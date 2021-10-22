"""Basic module for agregation data."""
import pandas as pd
import numpy as np


def merge_data_to_xls(filename, path, data1, data2):
    """Generate xls file from data."""
    writer = pd.ExcelWriter(f"{path}/{filename}.xlsx")
    data1.to_excel(writer, sheet_name='Agencies')
    data2.to_excel(writer, sheet_name='Investments')
    writer.save()


def merge_investments_dataframe_with_pdfdataframe(investments_dataframe, pdf_dataframe):
    """Merge two dataframes on colum UII."""
    merged_df = investments_dataframe.merge(
        pdf_dataframe, how='left', on='UII')
    merged_df['UII matched'] = np.where(
        merged_df['UII'] == merged_df['UII parsed'], 'True', 'False')
    merged_df['Investment Title matched'] = np.where(
        merged_df['Investment Title'] == merged_df['Investment Title parsed'], 'True', 'False')
    return merged_df
