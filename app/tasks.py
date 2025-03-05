# from celery import shared_task
# import pandas as pd

# @shared_task(bind=True)
# def process_csv_file(self,file_path):
#     """Processes the CSV file and calculates required metrics."""
#     df = pd.read_csv(file_path)
    
#     numeric_cols = df.select_dtypes(include=['number'])
#     result = {
#         'sum': numeric_cols.sum().to_dict(),
#         'average': numeric_cols.mean().to_dict(),
#         'count': numeric_cols.count().to_dict(),
#         'total_revenue': numeric_cols['Sales'].sum() if 'Sales' in numeric_cols else 0,
#         'average_discount': numeric_cols['Discount'].mean() if 'Discount' in numeric_cols else 0,
#         'best_selling_product': df.loc[df['Quantity'].idxmax(), 'Product Name'] if 'Quantity' in df.columns else None,
#         'most_profitable_product': df.loc[df['Profit'].idxmax(), 'Product Name'] if 'Profit' in df.columns else None,
#         'max_discount_product': df.loc[df['Discount'].idxmax(), 'Product Name'] if 'Discount' in df.columns else None,
#     }
#     return result


from celery import shared_task
import pandas as pd

from celery import shared_task
import pandas as pd
import numpy as np

@shared_task(bind=True)
def process_csv_file(self, file_path):
    """Processes the CSV file and calculates required metrics."""
    try:
        df = pd.read_csv(file_path)

        # Select numeric columns
        numeric_cols = df.select_dtypes(include=['number'])

        # Ensure all values are converted to Python-native types
        def convert_to_python(obj):
            """Converts NumPy types to native Python types."""
            if isinstance(obj, (np.integer, np.floating)):
                return obj.item()  # Convert NumPy types to Python native
            return obj

        result = {
            'sum': {k: convert_to_python(v) for k, v in numeric_cols.sum().to_dict().items()},
            'average': {k: convert_to_python(v) for k, v in numeric_cols.mean().to_dict().items()},
            'count': {k: convert_to_python(v) for k, v in numeric_cols.count().to_dict().items()},
            'total_revenue': convert_to_python(numeric_cols.get('Sales', pd.Series()).sum()),
            'average_discount': convert_to_python(numeric_cols.get('Discount', pd.Series()).mean()),
            'best_selling_product': df.loc[df['Quantity'].idxmax(), 'Product Name'] 
                if 'Quantity' in df.columns and not df['Quantity'].isna().all() else None,
            'most_profitable_product': df.loc[df['Profit'].idxmax(), 'Product Name'] 
                if 'Profit' in df.columns and not df['Profit'].isna().all() else None,
            'max_discount_product': df.loc[df['Discount'].idxmax(), 'Product Name'] 
                if 'Discount' in df.columns and not df['Discount'].isna().all() else None,
        }

        print("result is=", result)
        return result

    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise e  # This allows Celery to catch and store the error properly
